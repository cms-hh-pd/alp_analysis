
#pragma once

#include "BaseOperator.h"

template <class EventClass> class CounterOperator : public BaseOperator<EventClass> {

  public:

    long n_sel_ev_ = 0; 
    float n_sel_ev_w_ = 0;
//    TH1D h_sel {"h_sel", "cut flow", 500, 0., 1500.};

    CounterOperator() //: //bool fillH = false
//     fillH_(fillH), 
    {}
    virtual ~CounterOperator() {}

    virtual bool process( EventClass & ev ) {
      n_sel_ev_++;
     // n_sel_ev_w_ += ev.w_btag_ * ev.w_pu_;
      return true;
    }

    virtual bool output ( std::ostream & os ) {
      os << " n_sel_ev " << n_sel_ev_ << std::endl ;
     // if(fillH_) h_jets_ht.Fill(ht, w);
       
      return true;
    }

};
