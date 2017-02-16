
#pragma once

#include "BaseOperator.h"

template <class EventClass> class CounterOperator : public BaseOperator<EventClass> {

  public:

    TH1D h_nevts {"h_nevts", "number of events", 1, 0., 1.};

    std::vector<std::string> weights_;
    long n_sel_ev_ = 0; 
    std::string dirname_;

    CounterOperator(const std::vector<std::string> & weights = {}) :
      weights_(weights) {}
    virtual ~CounterOperator() {}

    virtual void init(TDirectory * tdir) {
      h_nevts.SetDirectory(tdir);
      h_nevts.Sumw2();
      dirname_ = tdir->GetPath(); //debug - improve
    }

    virtual bool process( EventClass & ev ) {
      float w = 1.0;
      w*=ev.eventInfo_.eventWeight(weights_);

      h_nevts.Fill(0.5, w);
      
      n_sel_ev_++;
      return true;
    }

    virtual bool output ( std::ostream & os ) {
      os << "  " << dirname_ << std::endl;
      os << "    " << n_sel_ev_ << std::endl ;
      os << "    " << h_nevts.GetBinContent(1) << "    " << h_nevts.GetBinError(1) << std::endl;        
      return true;
    }

};
