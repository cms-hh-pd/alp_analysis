
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class JERShifterOperator : public BaseOperator<EventClass> {

  public:

    int shift_;

    JERShifterOperator(int shift) :
    shift_(shift) {
        if(shift_ != 1 && shift_ != -1) std::cout << "JERShifterOperator: no JER shift applied" << std::endl;
    }
    virtual ~JERShifterOperator() {}

    virtual bool process( EventClass & ev ) {

      //get corrected pt and shift by uncertainty
      for (auto it = ev.jets_.begin(); it!=ev.jets_.end(); ++it) {    
        if(shift_ == 1 || shift_ == -1) {
          (*it).p4_ *= (1./(*it).JERunc()); //NOTE: to restore default pT
          if (shift_==1) (*it).p4_ *= ((*it).JERuncUp()); 
          else if (shift_==-1) (*it).p4_ *= ((*it).JERuncDown());         
        }
        else break;
      };
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "JER"+std::to_string(shift_);
      return name;
    }

};
