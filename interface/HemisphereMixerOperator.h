
#pragma once

#include <algorithm>
#include <functional>
#include <math.h>
#include <cmath>

#include "TChain.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TEntryList.h"

#include "BaseOperator.h"
#include "Hemisphere.h"
#include "nanoflann.hpp"
#include "prettyprint.hpp"

// class to hold variables for NN search
class HemisphereLibrary {

  public:

    typedef std::function<double(const alp::Hemisphere &)> FuncD;
    typedef std::vector<std::function<double(const alp::Hemisphere &)>> FuncDVec;
    typedef std::vector<alp::Hemisphere> HemVec;

    std::size_t n_vars_;
    std::size_t n_points_;
    std::vector<std::vector<double>> vars_v_;
    std::vector<double> sum_;
    std::vector<double> sumsq_;
    std::vector<double> var_stds_; 

    HemisphereLibrary(const HemVec & hem_v, const FuncDVec & funcDVec) :
      n_vars_(funcDVec.size()),
      n_points_(hem_v.size()),
      sum_(n_vars_, 0.0),
      sumsq_(n_vars_, 0.0) {
      for (auto hem : hem_v) {
        vars_v_.emplace_back(n_vars_, 0.0); // add n_vars elements
        for (std::size_t i=0; i < n_vars_; i++) {
          const auto & funcD = funcDVec.at(i);
          vars_v_.back().at(i) = funcD(hem);
          sum_.at(i) =  vars_v_.back().at(i);
          sumsq_.at(i) = std::pow(vars_v_.back().at(i),2);
        }
      }
    }

    virtual ~HemisphereLibrary() {}

    std::vector<double> & get_sum() { return sum_;}
    std::vector<double> & get_sumsq() { return sumsq_;}
    std::size_t get_n_points() { return n_points_;}

    void scale_vars_by_subset_stds() {

      for (std::size_t i=0; i < n_vars_; i++) {
        double mu = sum_.at(i)/n_points_;
	double x2 = sumsq_.at(i)/n_points_;
        double var = x2-mu*mu;
        for (std::size_t p = 0; p < n_points_; p++) {
          var_stds_.emplace_back(std::sqrt(var)); 
        }
      }
      scale_vars_by_stds(var_stds_);
    }

    void scale_vars_by_stds(const std::vector<double> var_stds) {
      for (std::size_t i=0; i < n_vars_; i++) {
        for (std::size_t p = 0; p < n_points_; p++) {
          vars_v_.at(p).at(i) /= var_stds.at(i); //divide by std
        }
      }
    }

    // Must return the number of data points
    inline size_t kdtree_get_point_count() const { return n_points_; }

    // L2 distance between p1 and and point with index idx_p2 
    inline double kdtree_distance(const double *p1,
                                  const size_t idx_p2,size_t /*size*/) const {
      double distance = 0.0;
      for (std::size_t i=0; i < n_vars_; i++) {
        distance += std::pow(p1[i] - vars_v_[idx_p2][i], 2);
      }
      return distance;
    }

    // Returns the dim'th component of the idx'th point 
    inline double kdtree_get_pt(const size_t idx, int dim) const {
      return vars_v_[idx][dim];
    }

    template <class BBOX>
    bool kdtree_get_bbox(BBOX& /*bb*/) const { return false; }

};

enum class Scaling {none, subset, set};

template <class EventClass> class HemisphereMixerOperator : public BaseOperator<EventClass> {

  public:

    typedef std::function<int(const alp::Hemisphere &, std::string , double )> FuncI;
    typedef std::vector<std::function<int(const alp::Hemisphere &, std::string , double)>> FuncIVec;
    typedef std::function<double(const alp::Hemisphere &)> FuncD;
    typedef std::vector<std::function<double(const alp::Hemisphere &)>> FuncDVec;
    typedef std::vector<alp::Hemisphere> HemVec;
    typedef std::vector<int> IntVec;
    typedef std::map<std::string,std::function<double(const alp::Hemisphere &)>> FuncDMap;
    // construct a kd-tree index:
    typedef nanoflann::KDTreeSingleIndexAdaptor<
      nanoflann::L2_Simple_Adaptor<double, HemisphereLibrary>,
      HemisphereLibrary > my_kd_tree_t;

    std::string btagAlgo_;
    double btagCut_;
    // map of vectors of hemipsheres (key is integer category) 
    std::map<IntVec, HemVec> hem_m_; 
    std::map<IntVec, HemisphereLibrary> hem_lib_; 
    // vector of functions  to compute distances 
    FuncIVec funcIVec_;
    FuncDVec funcDVec_;
    // map of kd-trees
    std::map<IntVec, std::unique_ptr<my_kd_tree_t>> index_m_;
    // scaling mode
    Scaling scaling_;
    // variances (global)
    std::vector<double> var_stds_;
    // number of neighbours to keep for each hemisphere
    std::size_t knn_;

    HemisphereMixerOperator( TChain * tc_hm,
      std::string btagAlgo, double btagCut,
      std::vector<std::string> nn_vars = { "thrustMayor","thrustMinor",
                                           "sumPz","invMass"},  
      std::size_t knn = 10,
      Scaling scaling = Scaling::set) :
      btagAlgo_(btagAlgo),
      btagCut_(btagCut),
      scaling_(scaling),
      var_stds_(nn_vars.size(), 0.0),
      knn_(knn)
      {

        funcIVec_ = { FuncI( [] (const alp::Hemisphere & hem, std::string disc, double cut) {
                       int nJets = alp::Hemisphere::NJets(hem);
                       return ( nJets > 3 ? 4 : nJets);
                  }),
                    FuncI( [] (const alp::Hemisphere & hem, std::string disc, double cut) {
                       int nTags = alp::Hemisphere::NTags(hem, disc, cut);
                       return ( nTags > 3 ? 4 : nTags);
                  })};
        
     	FuncDMap funcDMap = {{"thrustMayor", FuncD(&alp::Hemisphere::ThrustMayor)},
                             {"thrustMinor",FuncD(&alp::Hemisphere::ThrustMinor)},
                             {"sumPz", FuncD(&alp::Hemisphere::SumPz)},
                             {"invMass", FuncD(&alp::Hemisphere::InvMass)},
                             {"ptMaxBtag", FuncD( [&btagAlgo] (const alp::Hemisphere & hem){
                                return alp::Hemisphere::PtMaxBtag(hem, btagAlgo); })},
                             {"minPtBtag", FuncD( [&btagAlgo, &btagCut] (const alp::Hemisphere & hem){
                                return alp::Hemisphere::MinPtBtag(hem, btagAlgo, btagCut); })},
                             {"htBtag", FuncD( [&btagAlgo, &btagCut] (const alp::Hemisphere & hem){
                                return alp::Hemisphere::HtBtag(hem, btagAlgo, btagCut); })},
                             {"ht", FuncD(&alp::Hemisphere::Ht)},
                             {"pt1Btag", FuncD( [&btagAlgo, &btagCut] (const alp::Hemisphere & hem){
                                return alp::Hemisphere::Pt1Btag(hem, btagAlgo, btagCut); })},
                             {"pt2Btag", FuncD( [&btagAlgo, &btagCut] (const alp::Hemisphere & hem){
                                return alp::Hemisphere::Pt2Btag(hem, btagAlgo, btagCut); })},
                             {"pt3Btag", FuncD( [&btagAlgo, &btagCut] (const alp::Hemisphere & hem){
                                return alp::Hemisphere::Pt3Btag(hem, btagAlgo, btagCut); })},
                             {"pt4Btag", FuncD( [&btagAlgo, &btagCut] (const alp::Hemisphere & hem){
                                return alp::Hemisphere::Pt4Btag(hem, btagAlgo, btagCut); })},
                            };

        for (const auto & nn_var : nn_vars) {
          if (funcDMap.count(nn_var) < 1) {
            std::cout << nn_var << " not present in function map, skipping " << std::endl; 
          } else {
            funcDVec_.emplace_back(funcDMap.at(nn_var));
          } 
        }

        // setup readers  
        TTreeReader hem_reader(tc_hm);
        TTreeReaderValue<std::vector<alp::Hemisphere>> hems(hem_reader, "hems");
        auto elist = tc_hm->GetEntryList();
        if (elist != nullptr) {
          // iterate over all events in event list
          std::size_t list_entries = elist->GetN();
          int treenum = 0;
          for (std::size_t l_e=0; l_e < list_entries; l_e++) {
            auto treeEntry = elist->GetEntryAndTree(l_e,treenum);
            auto chainEntry = treeEntry+tc_hm->GetTreeOffset()[treenum];
            hem_reader.SetEntry(chainEntry);
            for (const auto & hem : *hems) {
              IntVec cat;
              for (const auto & funcI : funcIVec_) cat.emplace_back(funcI(hem, btagAlgo_, btagCut_));
              if (hem_m_.count(cat) < 1) hem_m_[cat] = {};
              hem_m_.at(cat).emplace_back(hem);
            }
          }
        } else {  
          // read whole tree and push hemispheres to map categories  
          while (hem_reader.Next()) {
            for (const auto & hem : *hems) {
              IntVec cat;
              for (const auto & funcI : funcIVec_) cat.emplace_back(funcI(hem, btagAlgo_, btagCut_));
              if (hem_m_.count(cat) < 1) hem_m_[cat] = {};
              hem_m_.at(cat).emplace_back(hem);
            }
          }
        }

        std::size_t n_points(0);
        std::vector<double> sum(funcDVec_.size(), 0.0);
        std::vector<double> sumsq(funcDVec_.size(), 0.0);
        for (const auto &kv : hem_m_) {
          auto it_bool = hem_lib_.emplace(kv.first, HemisphereLibrary{kv.second,funcDVec_});
          auto it = it_bool.first; // get iterator to inserted element
 	  if (scaling_ == Scaling::subset) { 
	    it->second.scale_vars_by_subset_stds();
          } else if (scaling_ == Scaling::set) {
            n_points += it->second.get_n_points();
            auto & sum_subset = it->second.get_sum();
            auto & sumsq_subset = it->second.get_sumsq();
            for (std::size_t i=0; i < funcDVec_.size(); i++) {
              sum.at(i) += sum_subset.at(i);
              sumsq.at(i) += sumsq_subset.at(i);
            }
          }
        }

        // scale by global variances if required 
        if (scaling_ == Scaling::set) {
        for (std::size_t i=0; i < var_stds_.size(); i++) {
          double mu = sum.at(i)/n_points;
          double x2 = sumsq.at(i)/n_points;
          double var = x2-mu*mu;
          for (std::size_t p = 0; p < n_points; p++) {
            var_stds_.at(i) = std::sqrt(var); // fill std vector
          }
        }
        for (auto & kv : hem_lib_) kv.second.scale_vars_by_stds(var_stds_);
      }

      // build kd-trees indexes
      for (const auto & kv : hem_lib_)  {
        auto it_bool = index_m_.emplace(kv.first,
                       	std::unique_ptr<my_kd_tree_t>(
                          new my_kd_tree_t(int(funcDVec_.size()),
                          kv.second,
                          nanoflann::KDTreeSingleIndexAdaptorParams(1000000)))); //work-around to get linear search - time consuming
        auto it = it_bool.first; // get iterator to inserted element
        it->second->buildIndex();
			}
      }

    virtual ~HemisphereMixerOperator() {}

    virtual bool process( EventClass & ev ) {

      ev.best_match_hems_.clear(); // clear matched hemispheres

      // for each original hemisphere
      for (std::size_t h_i=0; h_i<ev.hems_.size(); h_i++) {

        const auto & h = ev.hems_.at(h_i); // original event hemisphere
        ev.best_match_hems_.emplace_back(); // emplace empty vector<alp::Hemisphere>
        auto & b_hs = ev.best_match_hems_.back(); // reference to vector

        // get integer category
        std::vector<int> h_cat;  
        for (const auto & funcI : funcIVec_) h_cat.emplace_back(funcI(h, btagAlgo_, btagCut_));
        if (index_m_.count(h_cat) < 1) { 
          std::cout << "No index for category: " << h_cat << std::endl;
          return false; // remove event
        }
        // get matching variables vector
        std::vector<double> h_vars;  
        for (const auto & funcD : funcDVec_) h_vars.emplace_back(funcD(h));
        // rescale if required
	if (scaling_ == Scaling::set) {
          for (std::size_t v=0;v<h_vars.size();v++) 
            h_vars.at(v) /= var_stds_.at(v);
        } else if (scaling_ == Scaling::subset) {
          for (std::size_t v=0;v<h_vars.size();v++) 
            h_vars.at(v) /= hem_lib_.at(h_cat).var_stds_.at(v);
        }

        std::vector<std::size_t> index_nns(knn_);
        std::vector<double> dist_nns(knn_);
        // query kdtree
        index_m_.at(h_cat)->knnSearch(&h_vars[0], knn_, &index_nns[0], &dist_nns[0]);

        // vector of hemispheres corresponding to category 
        const auto & hem_v = hem_m_.at(h_cat); 

        for (std::size_t h_f = 0; h_f < knn_; h_f++) { 
          b_hs.emplace_back(hem_v.at(index_nns.at(h_f)));
          b_hs.at(h_f).dist_ = dist_nns.at(h_f);

          auto & sel_hem_jets = b_hs.back().jets_;
          for (auto & j : sel_hem_jets) { 
            if (h.d_phi_inv_)  j.p4_.SetPhi(-j.p4_.Phi()); 
            auto n_phi = ROOT::Math::VectorUtil::Phi_mpi_pi(j.p4_.Phi() + h.p_phi_);
            j.p4_.SetPhi(n_phi);
            if (h.sumPz_inv_)  j.p4_.SetEta(-j.p4_.Eta()); 
          }
        }

      }

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;
    }

};

