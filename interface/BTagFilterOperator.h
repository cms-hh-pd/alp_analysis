
#pragma once

#include <algorithm>

#include "BTagCalibrationStandalone.h"
#include "ComposableSelector.h"
#include "BaseOperator.h"
#include "Event.h"
#include "Utils.h"

  template <class EventClass> class BTagFilterOperator : public BaseOperator<EventClass> {

    public:

      std::string disc_;
      double d_value_;
      std::size_t min_number_;
      std::size_t antitag_pos_;
      bool isdata_;
      bool per_jet_sf_;


      // get short disc name
      std::map < std::string, std::string> s_name_map; 
      // get flavour from hadronFlavour
      std::map < int , BTagEntry::JetFlavor > flavour_map; 
      // systematics to take into account per flavour
      std::map< BTagEntry::JetFlavor, std::vector<std::string>> syst_map; 
      // Load BTagSF
      BTagCalibration btcalib;
      // BTagSF options
      std::map<std::string, BTagCalibrationReader> cr_map;
      std::string sf_mode = "iterativefit";

      BTagFilterOperator( std::string disc, double d_value,
                          std::size_t min_number , std::size_t antitag_pos, bool isdata,
                          std::string data_path, bool per_jet_sf = true ) :
       disc_(disc),
       d_value_(d_value),
       min_number_(min_number),
       antitag_pos_(antitag_pos),
       isdata_(isdata),
       per_jet_sf_(per_jet_sf)
       {

         s_name_map = {{"pfCombinedInclusiveSecondaryVertexV2BJetTags", "CSVv2"},
                       {"pfCombinedMVAV2BJetTags", "cMVAv2"}};
       
         flavour_map = {{5, BTagEntry::FLAV_B},
                        {4, BTagEntry::FLAV_C},
                        {0, BTagEntry::FLAV_UDSG}};

         syst_map = {{BTagEntry::FLAV_B, {"up_jes","down_jes",
                                          "up_lf","down_lf",
                                          "up_hfstats1", "down_hfstats1",
                                          "up_hfstats2", "down_hfstats2"}},
                    {BTagEntry::FLAV_C, {"up_cferr1","down_cferr1",
                                         "up_cferr2", "down_cferr2"}},
                    {BTagEntry::FLAV_UDSG, {"up_jes","down_jes",
                                            "up_hf","down_hf",
                                            "up_lfstats1", "down_lfstats1",
                                            "up_lfstats2", "down_lfstats2"}}};

         btcalib = BTagCalibration(s_name_map.at(disc), data_path+s_name_map.at(disc)+"_Moriond17_B_H.csv"); //_ichep.csv

         cr_map.emplace("central",
                        BTagCalibrationReader{BTagEntry::OP_RESHAPING,
                                              "central", {}});
         for (const auto & kv : flavour_map) 
           cr_map.at("central").load(btcalib,kv.second, sf_mode);
         // for every flavour
         for (const auto & kv : syst_map) {
           auto & syst_vector = kv.second;
           // for every systematic relevant per flavour
           for (const auto & syst : syst_vector) {
             auto it = cr_map.find(syst);
             if (it ==cr_map.end()) {
               // return iterator as firt pair element
               it = cr_map.emplace(syst,
                                   BTagCalibrationReader{BTagEntry::OP_RESHAPING,
                                                         syst, {}})
                                  .first;
             }
             // load calibration for this flavour and reader
             it->second.load(btcalib,kv.first, sf_mode);
           }
        }
      }

      virtual ~BTagFilterOperator() {}

      virtual bool process( EventClass & ev ) {

        // order by discriminator
        order_jets_by_disc(ev.jets_, disc_);

        // btag check
        for (std::size_t i=0; i < min_number_; i++) {
            if (i != antitag_pos_) {
                if(ev.jets_.at(i).disc(disc_) < d_value_) return false; }
            else {
                if(ev.jets_.at(i).disc(disc_) >= d_value_) return false; }
        }       

        // weight_map to save event weights BTagSF on
        std::map<std::string, float> weight_map;
        // inititialize all weights to 1.0
        weight_map["BTagWeight"] = 1.0;
        for (const auto & kv : syst_map) {
           for (const auto & syst : kv.second) {
             // at(syst) would return exception when no element exists
             weight_map["BTagWeight_"+syst] = 1.0;
           }
        }


        if(!isdata_) {
          for (auto & jet : ev.jets_) {
            auto jet_flavour = flavour_map.at(jet.hadronFlavour());
            auto jet_eta = jet.eta();
            auto jet_pt = jet.pt();
            auto jet_disc = jet.disc(disc_);
             
            
            auto central_sf = cr_map.at("central")
                                    .eval(jet_flavour, jet_eta,
                                          jet_pt, jet_disc);

            // range checks to avoid sf = 0
            if (std::abs(jet_eta) > 2.4) central_sf = 1.0;
            if (jet_pt < 20) central_sf = 1.0;
            if (jet_pt > 1000) central_sf = 1.0;

            weight_map.at("BTagWeight") *= central_sf;            
            if (per_jet_sf_) jet.discs_.emplace_back("BTagWeight",central_sf);

            for (const auto & syst : syst_map.at(jet_flavour)) {
              auto syst_sf = cr_map.at(syst)
                                   .eval(jet_flavour, jet_eta,
                                         jet_pt, jet_disc);

              // range checks to avoid sf = 0
              if (std::abs(jet_eta) > 2.4) syst_sf = 1.0;
              if (jet_pt < 20) syst_sf = 1.0;
              if (jet_pt > 1000) syst_sf = 1.0;

              weight_map.at("BTagWeight_"+syst) *= syst_sf;
              if (per_jet_sf_) jet.discs_.emplace_back("BTagWeight_"+syst,central_sf);
            }
          }
        }

        // add weights to event info
        for (const auto & weight_pair : weight_map) {
          ev.eventInfo_.weightPairs_.emplace_back(weight_pair);
        }

        return true;
      }

      virtual std::string get_name() {
        auto name = std::string{"sort_jets_in"+disc_};
        name += "and_min_"+std::to_string(min_number_)+">" + std::to_string(d_value_);  
        return name;
      } 
};

