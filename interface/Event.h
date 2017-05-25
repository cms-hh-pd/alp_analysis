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
      std::vector<alp::DiObject> dijets_;
      std::vector<alp::DiObject> dihiggs_;
      std::vector<alp::Lepton> muons_;
      std::vector<alp::Lepton> electrons_;
      alp::Candidate met_;
      std::vector<alp::Candidate> genbfromhs_;
      std::vector<alp::Candidate> genhs_;
      std::vector<alp::Candidate> tl_genbfromhs_;
      std::vector<alp::Candidate> tl_genhs_;
      std::vector<alp::DiObject>  tl_genhh_;
      float_t evtWeight_;
      // TTreeReaderValue/Array pointers (so they are nullable) to get the data 
      TTreeReaderValue<alp::EventInfo> * eventInfo_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Jet>> * jets_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::DiObject>> * dijets_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::DiObject>> * dihiggs_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Lepton>> * muons_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Lepton>> * electrons_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Candidate>> * genbfromhs_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Candidate>> * genhs_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Candidate>> * tl_genbfromhs_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::Candidate>> * tl_genhs_reader_ = nullptr;
      TTreeReaderValue<std::vector<alp::DiObject>> * tl_genhh_reader_ = nullptr;
      TTreeReaderValue<alp::Candidate> * met_reader_ = nullptr;
      TTreeReaderValue<float_t> * evtWeight_reader_ = nullptr;

      // additional stuff that might be created during the processing 
     // std::vector<alp::PtEtaPhiEVector> dijets_;
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
        // load dijet collection
        if (config.find("dijets_branch_name") != config.end()) {
            dijets_reader_ = new TTreeReaderValue<std::vector<alp::DiObject>>(reader, 
                config.at("dijets_branch_name").get_ref<const std::string &>().c_str());
        }
        // load dijet collection
        if (config.find("dihiggs_branch_name") != config.end()) {
            dihiggs_reader_ = new TTreeReaderValue<std::vector<alp::DiObject>>(reader,
                config.at("dihiggs_branch_name").get_ref<const std::string &>().c_str());
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
        // load GenBFromHs
        if (config.find("genbfromhs_branch_name") != config.end()) {
            genbfromhs_reader_ = new TTreeReaderValue<std::vector<alp::Candidate>>(reader, 
                config.at("genbfromhs_branch_name").get_ref<const std::string &>().c_str());      
        }                                                                               
        // load GenHs 
        if (config.find("genhs_branch_name") != config.end()) {
            genhs_reader_ = new TTreeReaderValue<std::vector<alp::Candidate>>(reader, 
                config.at("genhs_branch_name").get_ref<const std::string &>().c_str());      
        }
        // load GenBFromHs
        if (config.find("tl_genbfromhs_branch_name") != config.end()) {
            tl_genbfromhs_reader_ = new TTreeReaderValue<std::vector<alp::Candidate>>(reader,
                config.at("tl_genbfromhs_branch_name").get_ref<const std::string &>().c_str());
        }      
        // load GenHs for re-weighting
        if (config.find("tl_genhs_branch_name") != config.end()) {
            tl_genhs_reader_ = new TTreeReaderValue<std::vector<alp::Candidate>>(reader,
                config.at("tl_genhs_branch_name").get_ref<const std::string &>().c_str());
        }      
        // load GenHH for re-weighting
        if (config.find("tl_genhh_branch_name") != config.end()) {
            tl_genhh_reader_ = new TTreeReaderValue<std::vector<alp::DiObject>>(reader,
                config.at("tl_genhh_branch_name").get_ref<const std::string &>().c_str());
        }
        if (config.find("evt_weight_name") != config.end()) {
            evtWeight_reader_ = new TTreeReaderValue<float_t>(reader,
                config.at("evt_weight_name").get_ref<const std::string &>().c_str());
        }
        
      }
      virtual ~Event() {
        delete eventInfo_reader_;
        delete jets_reader_;
        delete dijets_reader_;
        delete dihiggs_reader_;
        delete muons_reader_;
        delete electrons_reader_;
        delete met_reader_;
        delete genbfromhs_reader_;
        delete genhs_reader_;
        delete tl_genbfromhs_reader_;
        delete tl_genhs_reader_;
        delete tl_genhh_reader_;
        delete evtWeight_reader_;
      }

      virtual void update() {

        // small copy overhead, only update if pointer not null
        if (eventInfo_reader_) eventInfo_ = **eventInfo_reader_;
        if (jets_reader_) jets_ = **jets_reader_;
        if (dijets_reader_) dijets_ = **dijets_reader_;
        if (dihiggs_reader_) dihiggs_ = **dihiggs_reader_;
        if (muons_reader_) muons_ = **muons_reader_;
        if (electrons_reader_) electrons_ = **electrons_reader_;
        if (met_reader_) met_ = **met_reader_;
        if (genbfromhs_reader_) genbfromhs_ = **genbfromhs_reader_;
        if (genhs_reader_) genhs_ = **genhs_reader_;
        if (tl_genbfromhs_reader_) tl_genbfromhs_ = **tl_genbfromhs_reader_;
        if (tl_genhs_reader_) tl_genhs_ = **tl_genhs_reader_;
        if (tl_genhh_reader_) tl_genhh_ = **tl_genhh_reader_;
        if (evtWeight_reader_) evtWeight_ = **evtWeight_reader_;

        free_is_.clear();
        hems_.clear();
        best_match_hems_.clear();
        thrust_phi_ = -10;

      }
  
  };

}
