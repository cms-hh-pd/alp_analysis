
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"
#include "json.hpp"

// for convenience
using json = nlohmann::json;

template <class EventClass> class TreeConverterOperator : public BaseOperator<EventClass> {

  public:
 
    std::vector<std::string> weights_;

    // variables to save in branches
    float_t evtWeight = 1.;
    std::vector<float_t>   jets_pt;
    std::vector<float_t> jets_eta;
    std::vector<float_t> jets_cmva;
    std::vector<float_t> jets_csv;
    std::vector<float_t> jets_phi;
    std::vector<float_t> jets_mass;

    std::vector<float_t> dijets_pt;
    std::vector<float_t> dijets_eta;
    std::vector<float_t> dijets_phi;
    std::vector<float_t> dijets_mass;

    std::vector<float_t>   dihiggs_pt;
    std::vector<float_t> dihiggs_eta;
    std::vector<float_t> dihiggs_phi;
    std::vector<float_t> dihiggs_mass;

    std::vector<float_t> muons_pt;
    std::vector<float_t> muons_eta;
    std::vector<float_t> muons_phi;
    std::vector<float_t> muons_mass;
    std::vector<float_t> muons_iso03;

    std::vector<float_t> elecs_pt;
    std::vector<float_t> elecs_eta;
    std::vector<float_t> elecs_phi;
    std::vector<float_t> elecs_mass;

    std::vector<float_t> genJets_pt;
    std::vector<float_t> genJets_eta;
    std::vector<float_t> genJets_phi;
    std::vector<float_t> genJets_mass;

    std::vector<float_t> genBfromH_px;
    std::vector<float_t> genBfromH_py;
    std::vector<float_t> genBfromH_pz;
    std::vector<float_t> genBfromH_E;
    std::vector<float_t> genBfromH_pt;
    std::vector<float_t> genBfromH_eta;
    std::vector<float_t> genBfromH_phi;
    std::vector<float_t> genBfromH_mass;

    std::vector<float_t> genhs_pt;
    std::vector<float_t> genhs_eta;
    std::vector<float_t> genhs_phi;
    std::vector<float_t> genhs_mass;

    std::vector<float_t> tl_genbfromhs_pt;
    std::vector<float_t> tl_genbfromhs_eta;
    std::vector<float_t> tl_genbfromhs_phi;
    std::vector<float_t> tl_genbfromhs_mass;

    std::vector<float_t> tl_genhs_pt;
    std::vector<float_t> tl_genhs_eta;
    std::vector<float_t> tl_genhs_phi;
    std::vector<float_t> tl_genhs_mass;

    std::vector<float_t> tl_genhh_pt;
    std::vector<float_t> tl_genhh_eta;
    std::vector<float_t> tl_genhh_phi;
    std::vector<float_t> tl_genhh_mass;

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

        tree_.Branch("genJets_pt","std::vector<float>",&genJets_pt, 64000, 2);
        tree_.Branch("genJets_eta","std::vector<float>",&genJets_eta, 64000, 2);
        tree_.Branch("genJets_phi","std::vector<float>",&genJets_phi, 64000, 2);
        tree_.Branch("genJets_mass","std::vector<float>",&genJets_mass, 64000, 2);
      }
      if (config_.find("dijets_branch_name") != config_.end()) {
        tree_.Branch("dijets_pt","std::vector<float>",&dijets_pt, 64000, 2);
        tree_.Branch("dijets_eta","std::vector<float>",&dijets_eta, 64000, 2);
        tree_.Branch("dijets_phi","std::vector<float>",&dijets_phi, 64000, 2);
        tree_.Branch("dijets_mass","std::vector<float>",&dijets_mass, 64000, 2);
     }

      if (config_.find("dihiggs_branch_name") != config_.end()) {
        tree_.Branch("dihiggs_pt","std::vector<float>",&dihiggs_pt, 64000, 2);
        tree_.Branch("dihiggs_eta","std::vector<float>",&dihiggs_eta, 64000, 2);
        tree_.Branch("dihiggs_phi","std::vector<float>",&dihiggs_phi, 64000, 2);
        tree_.Branch("dihiggs_mass","std::vector<float>",&dihiggs_mass, 64000, 2);
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
        tree_.Branch("genBfromH_px","std::vector<float>",&genBfromH_px, 64000, 2);
        tree_.Branch("genBfromH_py","std::vector<float>",&genBfromH_py, 64000, 2);
        tree_.Branch("genBfromH_pz","std::vector<float>",&genBfromH_pz, 64000, 2);
        tree_.Branch("genBfromH_E","std::vector<float>",&genBfromH_E, 64000, 2);
        tree_.Branch("genBfromH_pt","std::vector<float>",&genBfromH_pt, 64000, 2);
        tree_.Branch("genBfromH_eta","std::vector<float>",&genBfromH_eta, 64000, 2);
        tree_.Branch("genBfromH_phi","std::vector<float>",&genBfromH_phi, 64000, 2);
        tree_.Branch("genBfromH_mass","std::vector<float>",&genBfromH_mass, 64000, 2);
     }

      if (config_.find("genhs_branch_name") != config_.end()) {
        tree_.Branch("genHs_pt","std::vector<float>",&genhs_pt, 64000, 2);
        tree_.Branch("genHs_eta","std::vector<float>",&genhs_eta, 64000, 2);
        tree_.Branch("genHs_phi","std::vector<float>",&genhs_phi, 64000, 2);
        tree_.Branch("genHs_mass","std::vector<float>",&genhs_mass, 64000, 2);
     }

      if (config_.find("tl_genbfromhs_branch_name") != config_.end()) {
        tree_.Branch("TL_GenBfromH_pt","std::vector<float>",&tl_genbfromhs_pt, 64000, 2);
        tree_.Branch("TL_GenBfromH_eta","std::vector<float>",&tl_genbfromhs_eta, 64000, 2);
        tree_.Branch("TL_GenBfromH_phi","std::vector<float>",&tl_genbfromhs_phi, 64000, 2);
        tree_.Branch("TL_GenBfromH_mass","std::vector<float>",&tl_genbfromhs_mass, 64000, 2);
     }

      if (config_.find("tl_genhs_branch_name") != config_.end()) {
        tree_.Branch("TL_GenHs_pt","std::vector<float>",&tl_genhs_pt, 64000, 2);
        tree_.Branch("TL_GenHs_eta","std::vector<float>",&tl_genhs_eta, 64000, 2);
        tree_.Branch("TL_GenHs_phi","std::vector<float>",&tl_genhs_phi, 64000, 2);
        tree_.Branch("TL_GenHs_mass","std::vector<float>",&tl_genhs_mass, 64000, 2);
     }

      if (config_.find("tl_genhh_branch_name") != config_.end()) {
        tree_.Branch("TL_GenHH_pt","std::vector<float>",&tl_genhh_pt, 64000, 2);
        tree_.Branch("TL_GenHH_eta","std::vector<float>",&tl_genhh_eta, 64000, 2);
        tree_.Branch("TL_GenHH_phi","std::vector<float>",&tl_genhh_phi, 64000, 2);
        tree_.Branch("TL_GenHH_mass","std::vector<float>",&tl_genhh_mass, 64000, 2);
     }

      if (config_.find("met_branch_name") != config_.end()) {
        tree_.Branch("met_pt", &met_pt, "met_pt/F");
        tree_.Branch("met_phi", &met_phi, "met_phi/F");
     }
  //   tree_.Branch("trigger", &trigger, "trigger/F");
      tree_.Branch("evtWeight", &evtWeight, "evtWeight/F");

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {

    // to fill tree redirect pointers that where read
      evtWeight = 1.;
      if(weights_.size()>0) evtWeight *= ev.eventInfo_.eventWeight(weights_); //multiplied all weights from cfg
      else evtWeight *= ev.evtWeight_;

      jets_pt.clear();
      jets_eta.clear();
      jets_cmva.clear();
      jets_csv.clear();
      jets_phi.clear();
      jets_mass.clear();

      dijets_pt.clear();
      dijets_eta.clear();
      dijets_phi.clear();
      dijets_mass.clear();

      dihiggs_pt.clear();
      dihiggs_eta.clear();
      dihiggs_phi.clear();
      dihiggs_mass.clear();

      muons_pt.clear();
      muons_eta.clear();
      muons_phi.clear();
      muons_mass.clear();
      muons_iso03.clear();

      elecs_pt.clear();
      elecs_eta.clear();
      elecs_phi.clear();
      elecs_mass.clear();

      genJets_pt.clear();
      genJets_eta.clear();
      genJets_phi.clear();
      genJets_mass.clear();

      genBfromH_px.clear();
      genBfromH_py.clear();
      genBfromH_pz.clear();
      genBfromH_E.clear();
      genBfromH_pt.clear();
      genBfromH_eta.clear();
      genBfromH_phi.clear();
      genBfromH_mass.clear();

      genhs_pt.clear();
      genhs_eta.clear();
      genhs_phi.clear();
      genhs_mass.clear();

      tl_genbfromhs_pt.clear();
      tl_genbfromhs_eta.clear();
      tl_genbfromhs_phi.clear();
      tl_genbfromhs_mass.clear();

      tl_genhs_pt.clear();
      tl_genhs_eta.clear();
      tl_genhs_phi.clear();
      tl_genhs_mass.clear();

      tl_genhh_pt.clear();
      tl_genhh_eta.clear();
      tl_genhh_phi.clear();
      tl_genhh_mass.clear();

      for (std::size_t i = 0; i < ev.jets_.size(); i++ ) {
        jets_pt.push_back(ev.jets_.at(i).pt());
        jets_eta.push_back(ev.jets_.at(i).eta());
        jets_phi.push_back(ev.jets_.at(i).phi());
        jets_mass.push_back(ev.jets_.at(i).mass());
        jets_csv.push_back(ev.jets_.at(i).disc("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
        jets_cmva.push_back(ev.jets_.at(i).disc("pfCombinedMVAV2BJetTags"));
        
        if(ev.jets_.at(i).genJets_.size()>0){
            genJets_pt.push_back(ev.jets_.at(i).genJets_.at(0).Pt());
            genJets_eta.push_back(ev.jets_.at(i).genJets_.at(0).Eta());
            genJets_phi.push_back(ev.jets_.at(i).genJets_.at(0).Phi());
            genJets_mass.push_back(ev.jets_.at(i).genJets_.at(0).M());
        }
     }

      for (std::size_t i = 0; i < ev.dijets_.size(); i++ ) {
        dijets_pt.push_back(ev.dijets_.at(i).pt());
        dijets_eta.push_back(ev.dijets_.at(i).eta());
        dijets_phi.push_back(ev.dijets_.at(i).phi());
        dijets_mass.push_back(ev.dijets_.at(i).mass());
    }

      for (std::size_t i = 0; i < ev.dihiggs_.size(); i++ ) {
        dihiggs_pt.push_back(ev.dihiggs_.at(i).pt());
        dihiggs_eta.push_back(ev.dihiggs_.at(i).eta());
        dihiggs_phi.push_back(ev.dihiggs_.at(i).phi());
        dihiggs_mass.push_back(ev.dihiggs_.at(i).mass());
    }

/*      for (std::size_t i = 0; i < ev.elecs_.size(); i++ ) {
        elecs_pt.push_back(ev.elecs_.at(i).pt());
        elecs_eta.push_back(ev.elecs_.at(i).eta());
        elecs_phi.push_back(ev.elecs_.at(i).phi());
        elecs_mass.push_back(ev.elecs_.at(i).mass());
      }*/

      for (std::size_t i = 0; i < ev.genbfromhs_.size(); i++ ) {
        genBfromH_px.push_back(ev.genbfromhs_.at(i).p4_.Px());
        genBfromH_py.push_back(ev.genbfromhs_.at(i).p4_.Py());
        genBfromH_pz.push_back(ev.genbfromhs_.at(i).p4_.Pz());
        genBfromH_E.push_back(ev.genbfromhs_.at(i).p4_.energy());
        genBfromH_pt.push_back(ev.genbfromhs_.at(i).pt());
        genBfromH_eta.push_back(ev.genbfromhs_.at(i).eta());
        genBfromH_phi.push_back(ev.genbfromhs_.at(i).phi());
        genBfromH_mass.push_back(ev.genbfromhs_.at(i).mass());
     }

      for (std::size_t i = 0; i < ev.genhs_.size(); i++ ) {
        genhs_pt.push_back(ev.genhs_.at(i).pt());
        genhs_eta.push_back(ev.genhs_.at(i).eta());
        genhs_phi.push_back(ev.genhs_.at(i).phi());
        genhs_mass.push_back(ev.genhs_.at(i).mass());
     }

      for (std::size_t i = 0; i < ev.tl_genbfromhs_.size(); i++ ) {
        tl_genbfromhs_pt.push_back(ev.tl_genbfromhs_.at(i).pt());
        tl_genbfromhs_eta.push_back(ev.tl_genbfromhs_.at(i).eta());
        tl_genbfromhs_phi.push_back(ev.tl_genbfromhs_.at(i).phi());
        tl_genbfromhs_mass.push_back(ev.tl_genbfromhs_.at(i).mass());
     }

      for (std::size_t i = 0; i < ev.tl_genhs_.size(); i++ ) {
        tl_genhs_pt.push_back(ev.tl_genhs_.at(i).pt());
        tl_genhs_eta.push_back(ev.tl_genhs_.at(i).eta());
        tl_genhs_phi.push_back(ev.tl_genhs_.at(i).phi());
        tl_genhs_mass.push_back(ev.tl_genhs_.at(i).mass());
     }

      for (std::size_t i = 0; i < ev.tl_genhh_.size(); i++ ) {
        tl_genhh_pt.push_back(ev.tl_genhh_.at(i).pt());
        tl_genhh_eta.push_back(ev.tl_genhh_.at(i).eta());
        tl_genhh_phi.push_back(ev.tl_genhh_.at(i).phi());
        tl_genhh_mass.push_back(ev.tl_genhh_.at(i).mass());
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
