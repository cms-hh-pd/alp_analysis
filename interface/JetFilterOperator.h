
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class JetFilterOperator : public BaseOperator<EventClass> {

  public:

    double abs_eta_max_;
    double pt_min_;
    std::size_t min_number_;


    JetFilterOperator( double abs_eta_max, double pt_min , std::size_t min_number ) :
    abs_eta_max_(abs_eta_max),
    pt_min_(pt_min),
    min_number_(min_number) {}
    virtual ~JetFilterOperator() {}

    virtual bool process( EventClass & ev ) {

      // remove  jets outside limits
      auto iter = remove_if(ev.jets_.begin(),ev.jets_.end(),   
          [&] (const alp::Jet & jet) { 
             return (std::abs(jet.eta()) > abs_eta_max_ ) || 
                    (jet.pt() < pt_min_ ); });
      ev.jets_.erase(iter, ev.jets_.end());  

      // pass selection if more than min_number jet in region
      if (ev.jets_.size() < min_number_ ) return false;
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "jet_selection_min_"+std::to_string(min_number_);
      name+= "jets_pt>"+std::to_string(pt_min_);
      name+= "_|eta|<"+std::to_string(abs_eta_max_);
      return name;
    }

};
