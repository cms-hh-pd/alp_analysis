
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class IsoMuFilterOperator : public BaseOperator<EventClass> {

  public:

    double Iso03_min_;
    double pt_max_;
    std::size_t min_number_;

    IsoMuFilterOperator( double Iso03_min, double pt_max , std::size_t min_number ) :
    Iso03_min_(Iso03_min),
    pt_max_(pt_max),
    min_number_(min_number) {}
    virtual ~IsoMuFilterOperator() {}

    virtual bool process( EventClass & ev ) {

     //FIXME
     /* // remove  muons outside limits
      auto iter = remove_if(ev.muons_.begin(),ev.muons_.end(),   
          [&] (const ... & muon) { 
             return (muon.pfIso03()) > Iso03_min_ ) || 
                    (muon.pt() > pt_max_ ); });
      ev.muons_.erase(iter, ev.muons_.end());  

      // pass selection if more than min_number jet in region
      if (ev.muons_.size() < min_number_ ) return false;*/
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "isomu_selection_min_"+std::to_string(min_number_);
      name+= "mu_pt<"+std::to_string(pt_max_);
      name+= "iso03>"+std::to_string(Iso03_min_);
      return name;
    }

};
