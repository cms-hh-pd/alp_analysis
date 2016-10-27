
#pragma once

#include <algorithm>

#include "TH1.h"
#include "TH2.h"

#include "BaseOperator.h"

template <class EventClass> class MiscellPlotterOperator : public BaseOperator<EventClass> {

  public:
 
    std::string disc_;
    std::vector<std::string> weights_;
    std::vector<std::size_t> j_sortInd_;

    TH1D h_met_pt {"h_met_pt", "", 120,  0., 120.};
    TH1D h_mu_pt {"h_mu_pt", "", 150,  0., 150.};
    TH1D h_mu_iso03 {"h_mu_iso03", "", 50,  0., 0.3};


     MiscellPlotterOperator(const std::vector<std::string> & weights = {}) :
      weights_(weights) {}
    virtual ~MiscellPlotterOperator() {}

    virtual void init(TDirectory * tdir) {

      h_met_pt.SetDirectory(tdir);
      h_mu_pt.SetDirectory(tdir);
      h_mu_iso03.SetDirectory(tdir);

      h_met_pt.Sumw2();
      h_mu_pt.Sumw2();
      h_mu_iso03.Sumw2();
   }


    virtual bool process( EventClass & ev ) {

      float w = 1.0;
      float w_unc_sq = 1.0;      

      h_met_pt.Fill(ev.met_.pt(), w);
      for(std::size_t i=0; i< ev.muons_.size(); ++i){
        h_mu_pt.Fill(ev.muons_.at(i).pt(), w);
        h_mu_iso03.Fill(ev.muons_.at(i).iso03(), w);
      }

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
