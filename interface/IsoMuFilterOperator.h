
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class IsoMuFilterOperator : public BaseOperator<EventClass> {

  public:

    double iso03_max_;
    double pt_min_;
    std::size_t min_number_;

    IsoMuFilterOperator( double iso03_max, double pt_min , std::size_t min_number ) :
    iso03_max_(iso03_max),
    pt_min_(pt_min),
    min_number_(min_number) {}
    virtual ~IsoMuFilterOperator() {}

    virtual bool process( EventClass & ev ) {

      std::size_t nIsoMu = 0;
      for(std::size_t i=0; i< ev.muons_.size(); ++i){
          if ((ev.muons_.at(i).iso03() <= iso03_max_ ) && (ev.muons_.at(i).pt() >= pt_min_ )) nIsoMu++ ;
      }

      //pass selection if at least min_number_ muons in region
      if (nIsoMu < min_number_) return false;
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "isomu_selection_min_"+std::to_string(min_number_);
      name+= "mu_pt_min_"+std::to_string(pt_min_);
      name+= "iso03_max_"+std::to_string(iso03_max_);
      return name;
    }

};
