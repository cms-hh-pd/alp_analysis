
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class IsoMuFilterOperator : public BaseOperator<EventClass> {

  public:

    double iso03_min_;
    double pt_max_;
    std::size_t min_number_;

    IsoMuFilterOperator( double iso03_min, double pt_max , std::size_t min_number ) :
    iso03_min_(iso03_min),
    pt_max_(pt_max),
    min_number_(min_number) {}
    virtual ~IsoMuFilterOperator() {}

    virtual bool process( EventClass & ev ) {

      std::size_t nIsoMu = 0;
      for(std::size_t i=0; i< ev.muons_.size(); ++i){
          if ((ev.muons_.at(i).iso03() >= iso03_min_ ) && (ev.muons_.at(i).pt() <= pt_max_ )) nIsoMu++ ;
      }

      //pass selection if at least min_number_ muons in region
      if (nIsoMu < min_number_) return false;
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "isomu_selection_min_"+std::to_string(min_number_);
      name+= "mu_pt<"+std::to_string(pt_max_);
      name+= "iso03>"+std::to_string(iso03_min_);
      return name;
    }

};
