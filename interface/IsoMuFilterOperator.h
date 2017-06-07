
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class IsoMuFilterOperator : public BaseOperator<EventClass> {

  public:

    double iso04_max_;
    double pt_min_;
    std::size_t min_number_;

    IsoMuFilterOperator( double iso04_max, double pt_min , std::size_t min_number ) :
      iso04_max_(iso04_max),
      pt_min_(pt_min),
      min_number_(min_number) {}
    virtual ~IsoMuFilterOperator() {}

    virtual bool process( EventClass & ev ) {

      //check and remove muons out from selection
      auto iter = remove_if(ev.muons_.begin(),ev.muons_.end(),   
          [&] (const alp::Lepton & muon) { 
             return ( muon.iso04() > iso04_max_  || muon.pt() < pt_min_ ) ; });
      ev.muons_.erase(iter, ev.muons_.end());  

      //pass selection if at least min_number_ muons in region
      if (ev.muons_.size() < min_number_) return false;
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "isomu_selection_min_"+std::to_string(min_number_);
      name+= "mu_pt_min_"+std::to_string(pt_min_);
      name+= "iso04_max_"+std::to_string(iso04_max_);
      return name;
    }

};
