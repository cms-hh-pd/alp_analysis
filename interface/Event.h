
#pragma once
// ROOT includes
#include <TTreeReader.h>
#include <TTreeReaderArray.h>
// other CMSSW modules includes
#include "Analysis/ALPHA/interface/alp_objects.h"
// includes from this repositoty
#include "json.hpp"
#include "Hemisphere.h"

// for convenience
using json = nlohmann::json;

namespace alp { 

  class Event { 
  
    public:
  
      // objects which will be read from TTree before first operator
      alp::EventInfo eventInfo_;
      std::vector<alp::Jet> jets_;
      std::vector<alp::Lepton> muons_;
      std::vector<alp::Lepton> electrons_;
      alp::Candidate met_;
      // TTreeReaderValue/Array pointers (so they are nullable) to get the data 
      TTreeReaderValue<alp::EventInfo> * eventInfo_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Jet>> * jets_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Lepton>> * muons_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Lepton>> * electrons_reader_ = nullptr;
      TTreeReaderValue<alp::Candidate> * met_reader_ = nullptr;


      // additional stuff that might be created during the processing 
      std::vector<PtEtaPhiEVector> dijets_;
      std::vector<std::size_t> free_is_;
      // to save the hemispheres (rotated and pz positive)
      std::vector<alp::Hemisphere> hems_; 
      // best matching hemispheres ( [first/second][proximity])
      std::vector<std::vector<alp::Hemisphere>> best_match_hems_; 
      // to keep the tranverse thrust axis phi
      double thrust_phi_ = -10.;
  
      Event() {}
      Event(TTreeReader & reader, const json & config = {}) {

        // NOTE : if there is not branch_name key in the json those
        // branches will not be read

        // load event information 
        if (config.find("eventInfo_branch_name") != config.end()) {
            eventInfo_reader_ = new TTreeReaderValue<alp::EventInfo>(reader, 
                config.at("eventInfo_branch_name").get_ref<const std::string &>().c_str());
        }
        // load jet collection
        if (config.find("jets_branch_name") != config.end()) {
            jets_reader_ = new TTreeReaderValue<std::vector<alp::Jet>>(reader, 
                config.at("jets_branch_name").get_ref<const std::string &>().c_str());
        }
        // load muon collection
        if (config.find("muons_branch_name") != config.end()) {
            muons_reader_ = new TTreeReaderValue<std::vector<alp::Lepton>>(reader, 
                config.at("muons_branch_name").get_ref<const std::string &>().c_str());      
        }                                                                               
        // load electron collection
        if (config.find("electrons_branch_name") != config.end()) {
            electrons_reader_ = new TTreeReaderValue<std::vector<alp::Lepton>>(reader, 
                config.at("electrons_branch_name").get_ref<const std::string &>().c_str());      
        }                                                                               
        // load MET 
        if (config.find("met_branch_name") != config.end()) {
            met_reader_ = new TTreeReaderValue<alp::Candidate>(reader, 
                config.at("met_branch_name").get_ref<const std::string &>().c_str());      
        }                                                                               

      }
      virtual ~Event() {
        delete eventInfo_reader_;
        delete jets_reader_;
        delete muons_reader_;
        delete electrons_reader_;
        delete met_reader_;
      }

      virtual void update() {

        // small copy overhead, only update if pointer not null
        if (eventInfo_reader_) eventInfo_ = **eventInfo_reader_;
        if (jets_reader_) jets_ = **jets_reader_;
        if (muons_reader_) muons_ = **muons_reader_;
        if (electrons_reader_) electrons_ = **electrons_reader_;
        if (met_reader_) met_ = **met_reader_;


        dijets_.clear();
        free_is_.clear();
        hems_.clear();
        best_match_hems_.clear();
        thrust_phi_ = -10;

      }
  
  };

}

