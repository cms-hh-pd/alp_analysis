
#pragma once

#include <algorithm>

#include "ComposableSelector.h"
#include "BaseOperator.h"
#include "Event.h"
#include "Utils.h"

template <class EventClass> class ReWeightingOperator : public BaseOperator<EventClass> {

    public:

      std::string w_fname_SM_;
      std::string w_fname_BM_; 
      std::string w_fname_HH_;
      std::vector<std::string> sam_list_;
      std::vector<std::string> hist_list_;
      TFile wfile_SM_;
      TFile wfile_BM_;
      TFile wfile_HH_;
      std::vector<TH2D> hw_;
      TH2D normAnalitical_, normBench_;      

      ReWeightingOperator(std::string rw_fname_SM, std::string rw_fname_BM, std::string rw_fname_HH) :
      w_fname_SM_(w_fname_SM_),
      w_fname_BM_(w_fname_BM_),
      w_fname_HH_(w_fname_HH_)
      {           
    

      }
      virtual ~ReWeightingOperator() {}

      virtual bool process( EventClass & ev ) {

        // weight_map to save event weights for each sample
        std::map<std::string, float> weight_map;

        // inititialize all weights to 1.0 - safety
        for (const auto & sam : sam_list_) {
          // at(syst) would return exception when no element exists
          weight_map["ReWeighting_"+sam] = 1.0;
        }
        weight_map["Norm_Analytical"] = 1.0;

        // get variables and bins value
        float costh = ev.tl_genhh_.at(0).costhst();
        float mhh = ev.tl_genhh_.at(0).mass();
        int bin   = normBench_.GetBin(mhh,costh);
        int bin_a = normAnalitical_.GetBin(mhh,costh);

        //code to get weight
        for (unsigned int i=0; i<sam_list_.size(); i++) {
            float weight = 1.;
            float mergecostSum = 0;
            for (unsigned int icost=1; icost< 11; icost++){ //debug -- SM not considered?
              mergecostSum+= normBench_.GetBinContent(bin); }// flat in costS //DEBUG!!
              if (mergecostSum>0) {
                weight = (hw_.at(i).GetBinContent(bin) / mergecostSum); //debug!
            }
            weight_map.at("ReWeighting_"+sam_list_.at(i)) *= weight;  //DEBUG - weight 1 for SM         
        }
        weight_map.at("Norm_Analytical") *= normAnalitical_.GetBinContent(bin_a);

        // add weights to event info
        for (const auto & weight_pair : weight_map) {
          ev.eventInfo_.weightPairs_.emplace_back(weight_pair);
        }

        return true;
      }

      virtual std::string get_name() {
        auto name = "reweighting";
        return name;
      } 
};
