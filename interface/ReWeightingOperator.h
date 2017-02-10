
#pragma once

#include <algorithm>

#include "ComposableSelector.h"
#include "BaseOperator.h"
#include "Event.h"
#include "Utils.h"

  template <class EventClass> class ReWeightingOperator : public BaseOperator<EventClass> {

    public:

      int a_;
      std::vector<std::string> sam_list;        

      ReWeightingOperator( int a) :
      a_(a)
      { 
        sam_list = {"SM","BM2","BM3","BM4","BM5","BM6",
                    "BM7","BM8","BM9","BM10","BM11","BM12","BM13","BMbox"};
      }

      virtual ~ReWeightingOperator() {}

      virtual bool process( EventClass & ev ) {

        // weight_map to save event weights for each sample
        std::map<std::string, float> weight_map;

        // inititialize all weights to 1.0 - safety
        for (const auto & sam : sam_list) {
          // at(syst) would return exception when no element exists
          weight_map["ReWeighting_"+sam] = 1.0;
        }

        for (const auto & sam : sam_list) {

            //example on how to call ev variables
            float costh = ev.dihiggs_.at(0).costhst();
            float mhh = ev.dihiggs_.at(0).mass();

            //code to get weight
            //...........
            float weight = 1.;
            //code to get weight

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
