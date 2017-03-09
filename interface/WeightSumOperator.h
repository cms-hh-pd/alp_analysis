
#pragma once

#include "BaseOperator.h"

template <class EventClass> class WeightSumOperator : public BaseOperator<EventClass> {

  public:

    TH1D h_wsum {"h_wsum", "number of events", 1, 0., 1.};

    std::vector<std::string> weights_;
    double w_sum_ = 0.; 
    std::string dirname_;

    WeightSumOperator(const std::vector<std::string> & weights = {}) :
      weights_(weights) {}
    virtual ~WeightSumOperator() {}

    virtual void init(TDirectory * tdir) {
      h_wsum.SetDirectory(tdir);
      h_wsum.Sumw2();
      dirname_ = tdir->GetPath(); //debug - improve
    }

    virtual bool process( EventClass & ev ) {
      float w = 1.0;
      w*=ev.eventInfo_.eventWeight(weights_);

      h_wsum.Fill(0.5, w);      

      w_sum_+= w;

      return true;
    }

    virtual bool output ( std::ostream & os ) {
      os << "  " << dirname_ << std::endl;
      os << "  w_sum:" << w_sum_ << std::endl ;
      os << "  w_sum_h:" << h_wsum.GetBinContent(1);        
      return true;
    }

};
