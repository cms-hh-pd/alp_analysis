
#pragma once
// ROOT includes
#include <TTreeReader.h>
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
      // additional stuff that might be created during the processing 
      std::vector<PtEtaPhiEVector> dijets_;
      std::vector<std::size_t> free_is_;
  
      // TTreeReaderValue/Array pointers (so they are nullable) to get the data 
      TTreeReaderValue<std::vector<alp::Jet>> * jets_reader_ = nullptr;
      std::vector<std::unique_ptr<TTreeReaderValue<bool>>> hlt_bits_reader_; 
  
      Event() {}
      Event(TTreeReader & reader, const json & config = {}) {
        if (config.find("jets_branch_name") != config.end()) {
            jets_reader_ = new TTreeReaderValue<std::vector<alp::Jet>>(reader, 
                config.at("jets_branch_name").get_ref<const std::string &>().c_str());
        }
        if (config.find("hlt_names") != config.end()) {
          for (const auto & hlt_name : config.at("hlt_names")) {
            const std::string & hlt_name_s = hlt_name.get_ref<const std::string &>(); 
            hlt_bits_.emplace_back(hlt_name_s, false);
            hlt_bits_reader_.emplace_back(new TTreeReaderValue<bool>(reader,
                hlt_name_s.c_str()));
          }
        }
      }
  
      virtual ~Event() {
        delete jets_reader_;
      }

      virtual void update() {

        // small copy overhead
        if (jets_reader_) jets_ = **jets_reader_;

        // update hlt_bits vector from reader
        for (std::size_t i=0; i<hlt_bits_reader_.size(); i++) {
          hlt_bits_.at(i).second = **(hlt_bits_reader_.at(i));
        }

      }
  
  };

}

