
#pragma once

#include <algorithm>


//#include "CondFormats/BTauObjects/interface/BTagEntry.h"
//#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
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

  // Load btag SF
    const BTagCalibration * calibCSV = new BTagCalibration("CSVv2", "CSVv2_ichep.csv");
    const BTagCalibration * calibCMVA = new BTagCalibration("CMVAv2", "cMVAv2_ichep.csv");
    BTagEntry::JetFlavor jf = BTagEntry::FLAV_UDSG;
    BTagEntry::JetFlavor jfPrev = BTagEntry::FLAV_UDSG;
       
    BTagFilterOperator( std::string disc, double d_value, std::size_t min_number ) :
     disc_(disc),
     d_value_(d_value),
     min_number_(min_number) {}
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
      for (std::size_t i=0; i < min_number_; i++) {
        if (ev.jets_.at(i).hadronFlavour_ == 5) jf = BTagEntry::FLAV_B;
        else if (ev.jets_.at(i).hadronFlavour_ == 4) jf = BTagEntry::FLAV_C;
        else if (ev.jets_.at(i).hadronFlavour_ == 0) jf = BTagEntry::FLAV_UDSG;
        //only for medium CSV       
        BTagCalibrationReader * btcr = new BTagCalibrationReader(BTagEntry::OP_MEDIUM, "central", {"up", "down"});  //debug - error if it is outside for..
        btcr->load(*calibCSV,jf,"mujets"); //debug - 'iterativefit' if reshape
        ev.w_btag_ *= btcr->eval(jf, ev.jets_.at(i).p4_.Eta(), ev.jets_.at(i).p4_.Pt(), ev.jets_.at(i).disc("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
      }

      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{"sort_jets_in"+disc_};
      name += "and_min_"+std::to_string(min_number_)+">" + std::to_string(d_value_); 
      return name;
    } 

};
