
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"
#include "BTagFilterOperator.h"
#include "JetPairingOperator.h"
#include "Hemisphere.h"

#include "Event.h"


template <class EventClass> class MixedEventWriterOperator : public BaseOperator<EventClass> {

  public:
 
    std::string btagAlgo_;
    double btagCut_;

    // variables to save in branches
    std::vector<alp::Jet> mix_jets_;
    std::vector<alp::Hemisphere> fhems_;
    std::vector<alp::Hemisphere> orhems_;

    // a pointer to avoid undeclared label
    std::vector<alp::Jet> * mix_jets_ptr_;
    std::vector<alp::Hemisphere> * fhems_ptr_;
    std::vector<alp::Hemisphere> * orhems_ptr_;

    // hemisphere combinations to save
    std::vector<std::vector<std::size_t>> combs_; 

    TTree tree_{"mix_tree","Tree wth mixed events"};

     MixedEventWriterOperator(std::string btagAlgo, double btagCut, std::vector<std::vector<std::size_t>> combs = {{1,1}}) :
      mix_jets_ptr_(&mix_jets_),  
      fhems_ptr_(&fhems_),  
      orhems_ptr_(&orhems_),  
      btagAlgo_(btagAlgo),
      btagCut_(btagCut),
      combs_(combs) {}

    virtual ~MixedEventWriterOperator() {}

    virtual void init(TDirectory * tdir) {

      tree_.Branch("Jets","std::vector<alp::Jet>",
                   &mix_jets_ptr_, 64000, 1);
      tree_.Branch("Hems","std::vector<alp::Hemisphere>",
                   &fhems_ptr_, 64000, 1);
      tree_.Branch("OrHems","std::vector<alp::Hemisphere>",
                   &orhems_ptr_, 64000, 1);

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }

    virtual bool process( EventClass & ev ) {

      const auto & bm_hems = ev.best_match_hems_;
    //  const auto & dists = ev.hems_dist_;

      for (const auto & comb : combs_) {
 
        auto h_i = comb.at(0); 
        auto h_j = comb.at(1); 

        // clear vectors
        mix_jets_.clear();
        fhems_.clear();
        orhems_.clear();

        // references for easy access
        const auto jets_i = bm_hems.at(0).at(h_i).jets_;
        const auto jets_j = bm_hems.at(1).at(h_j).jets_;
        mix_jets_.insert(mix_jets_.end(), jets_i.begin(), jets_i.end());
        mix_jets_.insert(mix_jets_.end(), jets_j.begin(), jets_j.end());
     
        auto hems_i = bm_hems.at(0).at(h_i);
        auto hems_j = bm_hems.at(1).at(h_j);
        //const auto dist_i = dists.at(0).at(h_i);
//        const auto dist_j = dists.at(1).at(h_j);
  //      hems_i.dist_ = dist_i;
    //    hems_j.dist_ = dist_j;
        fhems_.emplace_back(hems_i);
        fhems_.emplace_back(hems_j);

        const auto orhems_i = bm_hems.at(0).at(0);
        const auto orhems_j = bm_hems.at(1).at(0);
        orhems_.emplace_back(orhems_i);
        orhems_.emplace_back(orhems_j);

        // fill tree with combination
        tree_.Fill();
      }

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
