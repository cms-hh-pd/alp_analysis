
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

    // variables to save in branches
    std::vector<alp::Jet> * jets_ptr = nullptr;
    std::vector<alp::Lepton> * muons_ptr = nullptr;
    std::vector<alp::Lepton> * electrons_ptr = nullptr;
    alp::Candidate * met_ptr = nullptr;

    // additional stuff to save
    std::vector<alp::PtEtaPhiEVector> * dijets_ptr = nullptr;

    TTree tree_{"tree","Tree using simplified alp dataformats"};

    json config_ = {};

    EventWriterOperator(const std::string & config_s, const std::vector<std::string> & weights = {}) :
      config_(json::parse(config_s)), 
      weights_(weights) {}

    virtual ~EventWriterOperator() {}

    virtual void init(TDirectory * tdir) {

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

      tree_.Branch("DiJets","std::vector<alp::PtEtaPhiEVector>", &dijets_ptr, 64000, 2);

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {

      // to fill tree redirect pointers that where read
      eventInfo_ptr = dynamic_cast<alp::EventInfo *>(&ev.eventInfo_); 
      jets_ptr = dynamic_cast<std::vector<alp::Jet> *>(&ev.jets_); 
      muons_ptr = dynamic_cast<std::vector<alp::Lepton> *>(&ev.muons_); 
      electrons_ptr = dynamic_cast<std::vector<alp::Lepton> *>(&ev.electrons_); 
      met_ptr = dynamic_cast<alp::Candidate *>(&ev.met_); 

      // also other event stuff
      dijets_ptr = dynamic_cast<std::vector<alp::PtEtaPhiEVector> *>(&ev.dijets_); 

      tree_.Fill();

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
