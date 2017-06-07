
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

    TH1D h_all_ht {"h_all_ht", "ht mu+met+jets", 500,  0., 1500.};
    TH1D h_met_pt {"h_met_pt", "met pt", 250,  0., 500.};
    TH1D h_mu_n   {"h_mu_n", "# muons", 20,  0., 20.};
    TH1D h_mu_pt  {"h_mu_pt", "muons pt", 250,  0., 500.};
    TH1D h_mu_iso03 {"h_mu_iso03", "muons iso03", 50,  0., 0.3};
    TH1D h_mu_iso04 {"h_mu_iso04", "muons iso04", 50,  0., 0.3};
    TH1D h_mu0_pt {"h_mu0_pt", "muon0 pt", 250,  0., 500.};
    TH1D h_mu0_iso03 {"h_mu0_iso03", "muon0 iso03", 50,  0., 0.3};
    TH1D h_mu0_iso04 {"h_mu0_iso04", "muon0 iso04", 50,  0., 0.3};

     MiscellPlotterOperator(const std::vector<std::string> & weights = {}) :
      weights_(weights) {}
    virtual ~MiscellPlotterOperator() {}

    virtual void init(TDirectory * tdir) {

      h_all_ht.SetDirectory(tdir);
      h_met_pt.SetDirectory(tdir);
      h_mu_n.SetDirectory(tdir);
      h_mu_pt.SetDirectory(tdir);
      h_mu_iso03.SetDirectory(tdir);
      h_mu_iso04.SetDirectory(tdir);
      h_mu0_pt.SetDirectory(tdir);
      h_mu0_iso03.SetDirectory(tdir);
      h_mu0_iso04.SetDirectory(tdir);

      h_all_ht.Sumw2();
      h_met_pt.Sumw2();
      h_mu_n.Sumw2();
      h_mu_pt.Sumw2();
      h_mu_iso03.Sumw2();
      h_mu_iso04.Sumw2();
      h_mu0_pt.Sumw2();
      h_mu0_iso03.Sumw2();
      h_mu0_iso04.Sumw2();

   }


    virtual bool process( EventClass & ev ) {

      float w = 1.0;
      w *= ev.eventInfo_.eventWeight(weights_); 

      h_mu_n.Fill(ev.muons_.size(), w);
      h_met_pt.Fill(ev.met_.pt(), w);

      float mpt = 0.;
      for(std::size_t i=0; i< ev.muons_.size(); ++i){
        if (i==0) { 
          h_mu0_pt.Fill(ev.muons_.at(i).pt(), w);
          h_mu0_iso03.Fill(ev.muons_.at(i).iso03(), w);
          h_mu0_iso04.Fill(ev.muons_.at(i).iso04(), w);
        }
        h_mu_pt.Fill(ev.muons_.at(i).pt(), w);
        h_mu_iso03.Fill(ev.muons_.at(i).iso03(), w);
        h_mu_iso04.Fill(ev.muons_.at(i).iso04(), w);
        mpt += ev.muons_.at(i).pt();
      }
      auto jpt = get_jets_ht(ev.jets_);
      h_all_ht.Fill(jpt+mpt+ev.met_.pt(), w);

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
