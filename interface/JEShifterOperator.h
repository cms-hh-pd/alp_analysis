
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class JEShifterOperator : public BaseOperator<EventClass> {

  public:

    double shift_;

    JEShifterOperator(double shift = 0.) :
    shift_(shift) {}
    virtual ~JEShifterOperator() {}

    virtual bool process( EventClass & ev ) {

      //get corrected pt and shift by uncertainty
      for (auto it = ev.jets_.begin(); it!=ev.jets_.end(); ++it) {
        // PAS method - wrong:
        //double pt_corr_shifted = (*it).pt()*(1+shift_*(*it).JESunc());
        //(*it).p4_.SetPt(pt_corr_shifted) ;
        
        (*it).p4_ *= (1+shift_*(*it).JESunc()); //NOTE: need to scale the entire PtEtaPhiEVector!        
      };       
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "JES_"+std::to_string(shift_);
      return name;
    }

};
