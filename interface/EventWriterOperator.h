
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"
#include "json.hpp"

// for convenience
using json = nlohmann::json;

template <class EventClass> class EventWriterOperator : public BaseOperator<EventClass> {

  public:
 
    // save in branches what was read
    alp::EventInfo * eventInfo_ptr = nullptr;

    std::vector<std::string> weights_;
    bool doGenHH_;

    // variables to save in branches
    float_t evtWeight = 1.;
    //std::vector<alp::EventInfo> * eventinfo_ptr = nullptr;
    std::vector<alp::Jet> * jets_ptr = nullptr;
    std::vector<alp::Lepton> * muons_ptr = nullptr;
    std::vector<alp::Lepton> * electrons_ptr = nullptr;
    alp::Candidate * met_ptr = nullptr;
    std::vector<alp::Candidate> * genbfromhs_ptr = nullptr;
    std::vector<alp::Candidate> * genhs_ptr = nullptr;
    std::vector<alp::Candidate> * tl_genbfromhs_ptr = nullptr;
    std::vector<alp::Candidate> * tl_genhs_ptr = nullptr;
    std::vector<alp::DiObject> * tl_genhh_ptr = nullptr;
    std::vector<alp::DiObject> * dijets_ptr = nullptr;
    std::vector<alp::DiObject> * dihiggs_ptr = nullptr;
    std::vector<alp::Hemisphere> * fhems_ptr = nullptr;
    std::vector<alp::Hemisphere> * orhems_ptr = nullptr;
    float_t classifier = 99.;

    TTree tree_{"tree","Tree using simplified alp dataformats"};

    json config_ = {};

    EventWriterOperator(const std::string & config_s, const std::vector<std::string> & weights = {}) :
      config_(json::parse(config_s)), 
      weights_(weights) {
	    if(config_.at("isSignal") && config_.find("tl_genhh_branch_name")== config_.end()) doGenHH_ = true;
      	else doGenHH_ = false;
      }

    virtual ~EventWriterOperator() {}

    virtual void init(TDirectory * tdir) {
   
      tree_.Branch("evtWeight", &evtWeight, "evtWeight/F");

      if (config_.find("eventInfo_branch_name") != config_.end()) {
        tree_.Branch(config_.at("eventInfo_branch_name").template get<std::string>().c_str(),
                     "alp::EventInfo", &eventInfo_ptr, 64000, 2);
      }
      if (config_.find("jets_branch_name") != config_.end()) {
        tree_.Branch(config_.at("jets_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::Jet>",&jets_ptr, 64000, 2);
      }
      // load muon collection
      if (config_.find("muons_branch_name") != config_.end()) {
        tree_.Branch(config_.at("muons_branch_name").template get<std::string>().c_str(),      
                     "std::vector<alp::Lepton>",&muons_ptr, 64000, 2);
      }                                                                               
      // load electron collection
      if (config_.find("electrons_branch_name") != config_.end()) {
        tree_.Branch(config_.at("electrons_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::Lepton>",&electrons_ptr, 64000, 2);
      }                                                                               
      // load MET 
      if (config_.find("met_branch_name") != config_.end()) {
        tree_.Branch(config_.at("met_branch_name").template get<std::string>().c_str(),
                     "alp::Candidate",&met_ptr, 64000, 2);
      }                          
      // load GenBFromHs
      if (config_.find("genbfromhs_branch_name") != config_.end()) {
        tree_.Branch(config_.at("genbfromhs_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::Candidate>",&genbfromhs_ptr, 64000, 2);
      }                                                                               
      // load GenHs 
      if (config_.find("genhs_branch_name") != config_.end()) {
        tree_.Branch(config_.at("genhs_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::Candidate>",&genhs_ptr, 64000, 2);
      }                                                         
      // load GenHs for re-weigthing
      if (config_.find("tl_genbfromhs_branch_name") != config_.end()) {
         tree_.Branch(config_.at("tl_genbfromhs_branch_name").template get<std::string>().c_str(),
                    "std::vector<alp::Candidate>",&tl_genbfromhs_ptr, 64000, 2);
      }                                   
      // load GenHs for re-weigthing
      if (config_.find("tl_genhs_branch_name") != config_.end()) {
        tree_.Branch(config_.at("tl_genhs_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::Candidate>",&tl_genhs_ptr, 64000, 2);
      }
      if (config_.find("tl_genhh_branch_name") != config_.end()) {
        tree_.Branch(config_.at("tl_genhh_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::DiObject>",&tl_genhh_ptr, 64000, 2);
      }
      else tree_.Branch("TL_GenHH","std::vector<alp::DiObject>", &tl_genhh_ptr, 64000, 2);

      if (config_.find("dijets_branch_name") != config_.end()) {
        tree_.Branch(config_.at("dijets_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::DiObject>",&dijets_ptr, 64000, 2);
      }
      else tree_.Branch("DiJets","std::vector<alp::DiObject>", &dijets_ptr, 64000, 2);

      if (config_.find("dihiggs_branch_name") != config_.end()) {
        tree_.Branch(config_.at("dihiggs_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::DiObject>",&dihiggs_ptr, 64000, 2);
      }
      else tree_.Branch("DiHiggs","std::vector<alp::DiObject>", &dihiggs_ptr, 64000, 2);

      if (config_.find("fhems_branch_name") != config_.end()) {
        tree_.Branch(config_.at("fhems_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::Hemisphere>",&fhems_ptr, 64000, 2);
      }
      if (config_.find("orhems_branch_name") != config_.end()) {
        tree_.Branch(config_.at("orhems_branch_name").template get<std::string>().c_str(),
                     "std::vector<alp::Hemisphere>",&orhems_ptr, 64000, 2);
      }
      if (config_.find("classifier_branch_name") != config_.end()) {
        tree_.Branch(config_.at("classifier_branch_name").template get<std::string>().c_str(),
                     &classifier, "classifier/F");
      }

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }

    virtual bool process( EventClass & ev ) {

      // to fill tree redirect pointers that where read
      evtWeight = 1.;
      if(weights_.size()>0) evtWeight *= ev.eventInfo_.eventWeight(weights_); //multiplied all weights from cfg
      else evtWeight *= ev.evtWeight_;

      if(doGenHH_) {
        ev.tl_genhh_.clear();
        if(ev.tl_genhs_.size()==2) ev.tl_genhh_.emplace_back(ev.tl_genhs_.at(0).p4_, ev.tl_genhs_.at(1).p4_);
        else {
          std::cout<< "EventWriterOperator: WARNING, tl_genhs size not equal 2 for signal" << std::endl;
          doGenHH_=false;
        }
      }

      eventInfo_ptr = dynamic_cast<alp::EventInfo *>(&ev.eventInfo_); 
      jets_ptr = dynamic_cast<std::vector<alp::Jet> *>(&ev.jets_); 
      muons_ptr = dynamic_cast<std::vector<alp::Lepton> *>(&ev.muons_); 
      electrons_ptr = dynamic_cast<std::vector<alp::Lepton> *>(&ev.electrons_); 
      met_ptr = dynamic_cast<alp::Candidate *>(&ev.met_); 
      genbfromhs_ptr = dynamic_cast<std::vector<alp::Candidate> *>(&ev.genbfromhs_); 
      genhs_ptr = dynamic_cast<std::vector<alp::Candidate> *>(&ev.genhs_); 
      tl_genbfromhs_ptr = dynamic_cast<std::vector<alp::Candidate> *>(&ev.tl_genbfromhs_);
      tl_genhs_ptr = dynamic_cast<std::vector<alp::Candidate> *>(&ev.tl_genhs_);     
      tl_genhh_ptr = dynamic_cast<std::vector<alp::DiObject> *>(&ev.tl_genhh_);
      dijets_ptr = dynamic_cast<std::vector<alp::DiObject> *>(&ev.dijets_); 
      dihiggs_ptr = dynamic_cast<std::vector<alp::DiObject> *>(&ev.dihiggs_); 
      fhems_ptr = dynamic_cast<std::vector<alp::Hemisphere> *>(&ev.fhems_); 
      orhems_ptr = dynamic_cast<std::vector<alp::Hemisphere> *>(&ev.orhems_); 
      classifier = ev.classifier_; 

      tree_.Fill();
    
      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

      virtual std::string get_name() {
        auto name = "eventWeight";
        return name;
      }

};
