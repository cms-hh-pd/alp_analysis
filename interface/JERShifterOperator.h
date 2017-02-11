
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class JERShifterOperator : public BaseOperator<EventClass> {

  public:

    bool shiftUp_;

    JERShifterOperator(bool shiftUp) :
    shiftUp_(shiftUp) {}
    virtual ~JERShifterOperator() {}

    virtual bool process( EventClass & ev ) {

      //get corrected pt and shift by uncertainty
      for (auto it = ev.jets_.begin(); it!=ev.jets_.end(); ++it) {    
        (*it).p4_ *= (1./(*it).JERunc()); //NOTE: to restore default pT
        if (shiftUp_) (*it).p4_ *= ((*it).JERuncUp()); 
        else (*it).p4_ *= ((*it).JERuncDown());         
      };
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "JER"+std::to_string(shiftUp_);
      return name;
    }

};
