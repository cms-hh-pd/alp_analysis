
#pragma once

#include <algorithm>

#include "ComposableSelector.h"
#include "BaseOperator.h"
#include "Event.h"
#include "Utils.h"

  template <class EventClass> class ReWeightingOperator : public BaseOperator<EventClass> {

    public:

      std::string filew_name_;
      std::string osample_;
      std::vector<std::string> sam_list_;
      TFile filew_;
      TH1F hw_;      

      ReWeightingOperator(std::string filew_name, std::string osample) :
      filew_name_(filew_name),
      osample_(osample)
      {           
        sam_list_ = {"SM","BM2","BM3","BM4","BM5","BM6",
                    "BM7","BM8","BM9","BM10","BM11","BM12","BM13","BMbox"};

        //get histogram related to sample
        std::string hanme = osample; //DEBUG
        filew_ = TFile::Open(filew_name.c_str());
        hw_ = (TH1F*)filew_.Get(hanme.c_str());

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

        for (const auto & sam : sam_list_) {

            //example on how to call ev variables
            float costh = ev.tl_genhh_.at(0).costhst();
            float mhh = ev.tl_genhh_.at(0).mass();

            //code to get weight
            float weight = 1.;
            float mergecostSum = 0;
           // for ii in range(1,11) : mergecostSum+= sumHBenchBin.GetBinContent(bmhh,ii)  DEBUG
            if (mergecostSum >0) {
                weight = (hw_.GetBinContent(mhh,costh) / mergecostSum);
            }
            weight_map.at("ReWeighting_"+sam) *= weight;           
        }

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
