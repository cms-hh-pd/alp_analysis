
#pragma once
// ROOT includes
#include <TTreeReader.h>
#include <TTreeReaderArray.h>
// other CMSSW modules includes
#include "Analysis/ALPHA/interface/alp_objects.h"
// includes from this repositoty
#include "json.hpp"

// for convenience
using json = nlohmann::json;

namespace alp { 

  class Event { 
  
    public:
  
      // objects which will be read from TTree before first operator
      std::vector<std::pair<std::string, bool>> hlt_bits_;
      std::vector<alp::Jet> jets_;

      // required muon and trigger information for trigger studies
      // NOTE: might load objects in the future instead 
      std::vector<float> muons_pt_;
      std::vector<float> muons_pfiso03_;
      float met_pt_;
      float w_btag_ = 1.; //btag event weight (computed in alp)
      float w_pu_ = 1.;

      // additional stuff that might be created during the processing 
      std::vector<PtEtaPhiEVector> dijets_;
      std::vector<std::size_t> free_is_;
  
      // TTreeReaderValue/Array pointers (so they are nullable) to get the data 
      TTreeReaderValue<std::vector<alp::Jet>> * jets_reader_ = nullptr;
      std::vector<std::unique_ptr<TTreeReaderValue<bool>>> hlt_bits_reader_; 
      TTreeReaderArray<float> * muons_pt_reader_ = nullptr;
      TTreeReaderArray<float> * muons_pfiso03_reader_ = nullptr;
      TTreeReaderValue<float> * met_pt_reader_ = nullptr;
      TTreeReaderValue<float> * w_pu_reader_ = nullptr;
  
      Event() {}
      Event(TTreeReader & reader, const json & config = {}) {
        // load jet collection
        if (config.find("jets_branch_name") != config.end()) {
            jets_reader_ = new TTreeReaderValue<std::vector<alp::Jet>>(reader, 
                config.at("jets_branch_name").get_ref<const std::string &>().c_str());
        }
        // load trigger bits
        if (config.find("hlt_names") != config.end()) {
          for (const auto & hlt_name : config.at("hlt_names")) {
            const std::string & hlt_name_s = hlt_name.get_ref<const std::string &>(); 
            hlt_bits_.emplace_back(hlt_name_s, false);
            hlt_bits_reader_.emplace_back(new TTreeReaderValue<bool>(reader,
                hlt_name_s.c_str()));
          }
        }

        // muon and met information required for trigger
        muons_pt_reader_ = new TTreeReaderArray<float>(reader, "Muons.pt");
        muons_pfiso03_reader_ = new TTreeReaderArray<float>(reader, "Muons.pfIso03");
        met_pt_reader_ = new TTreeReaderValue<float>(reader, "MEt.pt");
        w_pu_reader_ = new TTreeReaderValue<float>(reader, "PUWeight");

      }
  
      virtual ~Event() {
        delete jets_reader_;
        delete muons_pt_reader_;
        delete muons_pfiso03_reader_;      
        delete met_pt_reader_;
        delete w_pu_reader_;
      }

      virtual void update() {

        // small copy overhead
        if (jets_reader_) jets_ = **jets_reader_;

        // update hlt_bits vector from reader
        for (std::size_t i=0; i<hlt_bits_reader_.size(); i++) {
          hlt_bits_.at(i).second = **(hlt_bits_reader_.at(i));
        }

        // muon information
        muons_pt_.clear();
        muons_pfiso03_.clear();
        for (std::size_t i=0; i<muons_pt_reader_->GetSize(); i++) {
          muons_pt_.emplace_back(muons_pt_reader_->At(i));
          muons_pfiso03_.emplace_back(muons_pfiso03_reader_->At(i));
        }

        // met information
        met_pt_ = **met_pt_reader_;
        w_pu_ = **w_pu_reader_;

        w_btag_ = 1.;

      }
  
  };

}

