
#pragma once

#include <algorithm>


//#include "CondTools/BTau/interface/BTagCalibrationReader.h"
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

  // Load btag SF
    const BTagCalibration calibCSV = BTagCalibration("CSVv2", "CSVv2_ichep.csv");
    const BTagCalibration calibCMVA = BTagCalibration("CMVAv2", "cMVAv2_ichep.csv");
    BTagEntry::JetFlavor jf = BTagEntry::FLAV_UDSG;
    BTagEntry::JetFlavor jfPrev = BTagEntry::FLAV_UDSG;

    BTagCalibrationReader btcr = BTagCalibrationReader(BTagEntry::OP_RESHAPING, "central", {});  //debug - error if it is outside for..  MEDIUM
       
    BTagFilterOperator( std::string disc, double d_value, std::size_t min_number , bool isdata) :
     disc_(disc),
     d_value_(d_value),
     min_number_(min_number),
     isdata_(isdata) {
       btcr.load(calibCSV,BTagEntry::FLAV_B,"iterativefit");
       btcr.load(calibCSV,BTagEntry::FLAV_C,"iterativefit");
       btcr.load(calibCSV,BTagEntry::FLAV_UDSG,"iterativefit");
     }
    virtual ~BTagFilterOperator() {}

    virtual bool process( EventClass & ev ) {

      // order by discriminator
      order_jets_by_disc(ev.jets_, disc_);

      // check that min_number jet pass d_value    
      for (std::size_t i=0; i < min_number_; i++) {
        if (ev.jets_.at(i).disc(disc_) < d_value_) return false;
      }

      // get event weight from btag SF
      ev.w_btag_ = 1.0; 
      if(!isdata_) { //weight 1 for data
        for (std::size_t i=0; i < ev.jets_.size() ; i++) { // ev.jets_.size() min_number_
          if (ev.jets_.at(i).hadronFlavour_ == 5) jf = BTagEntry::FLAV_B;
          else if (ev.jets_.at(i).hadronFlavour_ == 4) jf = BTagEntry::FLAV_C;
          else if (ev.jets_.at(i).hadronFlavour_ == 0) jf = BTagEntry::FLAV_UDSG;
          ev.w_btag_ *= btcr.eval(jf, ev.jets_.at(i).p4_.Eta(), ev.jets_.at(i).p4_.Pt(), ev.jets_.at(i).disc("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
        }
      }

      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{"sort_jets_in"+disc_};
      name += "and_min_"+std::to_string(min_number_)+">" + std::to_string(d_value_); 
      return name;
    } 

};

