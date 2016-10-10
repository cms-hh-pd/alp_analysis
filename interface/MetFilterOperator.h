
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class MetFilterOperator : public BaseOperator<EventClass> {

  public:

    double pt_max_;

    MetFilterOperator( double pt_max ) :
    pt_max_(pt_max){}
    virtual ~MetFilterOperator() {}

    virtual bool process( EventClass & ev ) {

      return true; // FIXME (met.pt() < pt_max_ );

    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "met_pt<"+std::to_string(pt_max_);
      return name;
    }

};
