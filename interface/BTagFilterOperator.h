
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
      bool isdata_;

    // Load BTagSF
      const BTagCalibration calibCSV;
      const BTagCalibration calibCMVA;
      BTagEntry::JetFlavor jf = BTagEntry::FLAV_UDSG;
      BTagEntry::JetFlavor jfPrev = BTagEntry::FLAV_UDSG;
    // BTagSF options
      BTagCalibrationReader btcr = BTagCalibrationReader(BTagEntry::OP_RESHAPING, "central", {});
      std::string BTagSFmode = "iterativefit";
         
      BTagFilterOperator( std::string disc, double d_value, std::size_t min_number , bool isdata,
                          const std::string & data_path ) :
       disc_(disc),
       d_value_(d_value),
       min_number_(min_number),
       isdata_(isdata),
       calibCSV("CSVv2", data_path+ "CSVv2_ichep.csv"),
       calibCMVA("CMVAv2", data_path+"cMVAv2_ichep.csv")
       {
         btcr.load(calibCSV,BTagEntry::FLAV_B,);
         btcr.load(calibCSV,BTagEntry::FLAV_C, BTagSFmode);
         btcr.load(calibCSV,BTagEntry::FLAV_UDSG, BTagSFmode);
       }
      virtual ~BTagFilterOperator() {}

      virtual bool process( EventClass & ev ) {

        // order by discriminator
        order_jets_by_disc(ev.jets_, disc_);

        // btag check
        for (std::size_t i=0; i < min_number_; i++) {
            if(ev.jets_.at(i).disc(disc_) < d_value_) return false;
        }
        // compute BTagSF on all objects in acc - NOTE: needed because we sorted in csv
        float w_btag = 1.0;
        for (std::size_t i=0; i < ev.jets_.size(); i++) {
          if(!isdata_) {
            if (ev.jets_.at(i).hadronFlavour_ == 5)      jf = BTagEntry::FLAV_B;
            else if (ev.jets_.at(i).hadronFlavour_ == 4) jf = BTagEntry::FLAV_C;
            else if (ev.jets_.at(i).hadronFlavour_ == 0) jf = BTagEntry::FLAV_UDSG;
            w_btag *= btcr.eval(jf, ev.jets_.at(i).p4_.Eta(), ev.jets_.at(i).p4_.Pt(), ev.jets_.at(i).disc(disc_));
          }
        }
        // add weight to event info
        ev.eventInfo_.weightPairs_.emplace_back("BTagWeight",w_btag);
        return true;
      }

      virtual std::string get_name() {
        auto name = std::string{"sort_jets_in"+disc_};
        name += "and_min_"+std::to_string(min_number_)+">" + std::to_string(d_value_);  
        return name;
      } 
};

