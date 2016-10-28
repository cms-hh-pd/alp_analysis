
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class MetFilterOperator : public BaseOperator<EventClass> {

  public:

    double pt_min_;

    MetFilterOperator( double pt_min ) :
    pt_min_(pt_min){}
    virtual ~MetFilterOperator() {}

    virtual bool process( EventClass & ev ) {

      return (ev.met_pt_ < pt_min_ );

    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "met_pt<"+std::to_string(pt_min_);
      return name;
    }

};
