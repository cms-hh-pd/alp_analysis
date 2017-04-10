
#pragma once

#include "BaseOperator.h"

template <class EventClass> class CounterOperator : public BaseOperator<EventClass> {

  public:

    TH1D h_nevts {"h_nevts", "number of events - weighted", 1, 0., 1.};
    TH1D h_eff {"h_eff", "efficiency", 1, 0., 1.};

    std::vector<std::string> weights_;
    long n_sel_ev_ = 0; 
    std::string dirname_;
    double ngenev_ = 0;

    CounterOperator(double ngenev, const std::vector<std::string> & weights = {}) :
      ngenev_(ngenev),
      weights_(weights) {}
    virtual ~CounterOperator() {}

    virtual void init(TDirectory * tdir) {
      h_nevts.SetDirectory(tdir);
      h_nevts.Sumw2();
      h_eff.SetDirectory(tdir);
      h_eff.Sumw2();
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

      h_eff.Fill(h_nevts.GetBinContent(1)/1.);   
      os << "  " << n_sel_ev_ << std::endl;
      os << "  " << h_nevts.GetBinContent(1) << std::endl; //<< "    " << h_nevts.GetBinError(1) << std::endl;        
      os << "eff: " << h_nevts.GetBinContent(1)/ngenev_ << std::endl; 
      return true;
    }

};
