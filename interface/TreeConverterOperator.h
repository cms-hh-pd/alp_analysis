
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"
#include "json.hpp"

// for convenience
using json = nlohmann::json;

template <class EventClass> class TreeConverterOperator : public BaseOperator<EventClass> {

  public:
 
    // variables to save in branches
    float_t weight = 0.;
    std::vector<std::string> weights_;

    std::vector<float_t>   jets_pt;
    std::vector<float_t> jets_eta;
    std::vector<float_t> jets_cmva;
    std::vector<float_t> jets_csv;
    std::vector<float_t> jets_phi;
    std::vector<float_t> jets_mass;

    std::vector<float_t> muons_pt;
    std::vector<float_t> muons_eta;
    std::vector<float_t> muons_phi;
    std::vector<float_t> muons_mass;
    std::vector<float_t> muons_iso03;

    std::vector<float_t> elecs_pt;
    std::vector<float_t> elecs_eta;
    std::vector<float_t> elecs_phi;
    std::vector<float_t> elecs_mass;

    std::vector<float_t> genBfromH_pt;
    std::vector<float_t> genBfromH_eta;
    std::vector<float_t> genBfromH_phi;
    std::vector<float_t> genBfromH_mass;

    float_t met_pt;
    float_t met_phi;

    json config_ = {};

    TTree tree_{"tree","Tree using  dataformats"};

    TreeConverterOperator(const std::string & config_s, const std::vector<std::string> & weights = {}) :
      config_(json::parse(config_s)), 
      weights_(weights) {}
    virtual ~TreeConverterOperator() {}

    virtual void init(TDirectory * tdir) {
      if (config_.find("jets_branch_name") != config_.end()) {
        tree_.Branch("jets_pt","std::vector<float>",&jets_pt, 64000, 2);
        tree_.Branch("jets_eta","std::vector<float>",&jets_eta, 64000, 2);
        tree_.Branch("jets_phi","std::vector<float>",&jets_phi, 64000, 2);
        tree_.Branch("jets_mass","std::vector<float>",&jets_mass, 64000, 2);
        tree_.Branch("jets_csv","std::vector<float>",&jets_csv, 64000, 2);
        tree_.Branch("jets_cmva","std::vector<float>",&jets_cmva, 64000, 2);
      }

      if (config_.find("muons_branch_name") != config_.end()) {
        tree_.Branch("muons_pt","std::vector<float>",&muons_pt, 64000, 2);
        tree_.Branch("muons_eta","std::vector<float>",&muons_eta, 64000, 2);
        tree_.Branch("muons_phi","std::vector<float>",&muons_phi, 64000, 2);
        tree_.Branch("muons_mass","std::vector<float>",&muons_mass, 64000, 2);
        tree_.Branch("muons_iso03","std::vector<float>",&muons_iso03, 64000, 2);
     }

      if (config_.find("electrons_branch_name") != config_.end()) {
        tree_.Branch("elecs_pt","std::vector<float>",&elecs_pt, 64000, 2);
        tree_.Branch("elecs_eta","std::vector<float>",&elecs_eta, 64000, 2);
        tree_.Branch("elecs_phi","std::vector<float>",&elecs_phi, 64000, 2);
        tree_.Branch("elecs_mass","std::vector<float>",&elecs_mass, 64000, 2);
     }

      if (config_.find("genbfromhs_branch_name") != config_.end()) {
        tree_.Branch("genBfromH_pt","std::vector<float>",&genBfromH_pt, 64000, 2);
        tree_.Branch("genBfromH_eta","std::vector<float>",&genBfromH_eta, 64000, 2);
        tree_.Branch("genBfromH_phi","std::vector<float>",&genBfromH_phi, 64000, 2);
        tree_.Branch("genBfromH_mass","std::vector<float>",&genBfromH_mass, 64000, 2);
     }

      if (config_.find("met_branch_name") != config_.end()) {
        tree_.Branch("met_pt", &met_pt, "met_pt/F");
        tree_.Branch("met_phi", &met_phi, "met_phi/F");
     }
  //   tree_.Branch("trigger", &trigger, "trigger/F");
      tree_.Branch("weight", &weight, "weight/F");

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {

      jets_pt.clear();
      jets_eta.clear();
      jets_cmva.clear();
      jets_csv.clear();
      jets_phi.clear();
      jets_mass.clear();

      muons_pt.clear();
      muons_eta.clear();
      muons_phi.clear();
      muons_mass.clear();
      muons_iso03.clear();

      elecs_pt.clear();
      elecs_eta.clear();
      elecs_phi.clear();
      elecs_mass.clear();

      genBfromH_pt.clear();
      genBfromH_eta.clear();
      genBfromH_phi.clear();
      genBfromH_mass.clear();


      float w = 1.0;
      w*=ev.eventInfo_.eventWeight(weights_);
      weight = w;

      for (std::size_t i = 0; i < ev.jets_.size(); i++ ) {
        jets_pt.push_back(ev.jets_.at(i).pt());
        jets_eta.push_back(ev.jets_.at(i).eta());
        jets_phi.push_back(ev.jets_.at(i).phi());
        jets_mass.push_back(ev.jets_.at(i).mass());
        jets_csv.push_back(ev.jets_.at(i).disc("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
        jets_cmva.push_back(ev.jets_.at(i).disc("pfCombinedMVAV2BJetTags"));
     }

/*      for (std::size_t i = 0; i < ev.elecs_.size(); i++ ) {
        elecs_pt.push_back(ev.elecs_.at(i).pt());
        elecs_eta.push_back(ev.elecs_.at(i).eta());
        elecs_phi.push_back(ev.elecs_.at(i).phi());
        elecs_mass.push_back(ev.elecs_.at(i).mass());
        elecs_csv.push_back(ev.elecs_.at(i).csv());
        elecs_cmva.push_back(ev.elecs_.at(i).cmva());
      }*/

      for (std::size_t i = 0; i < ev.genbfromhs_.size(); i++ ) {
        genBfromH_pt.push_back(ev.genbfromhs_.at(i).pt());
        genBfromH_eta.push_back(ev.genbfromhs_.at(i).eta());
        genBfromH_phi.push_back(ev.genbfromhs_.at(i).phi());
        genBfromH_mass.push_back(ev.genbfromhs_.at(i).mass());
     }

      for (std::size_t i = 0; i < ev.muons_.size(); i++ ) {
        muons_pt.push_back(ev.muons_.at(i).pt());
        muons_eta.push_back(ev.muons_.at(i).eta());
        muons_phi.push_back(ev.muons_.at(i).phi());
        muons_mass.push_back(ev.muons_.at(i).mass());
        muons_iso03.push_back(ev.muons_.at(i).iso03());
      }

      met_pt = ev.met_.pt();
      met_phi = ev.met_.phi();

      tree_.Fill();

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
