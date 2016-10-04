
#pragma once

#include <algorithm>

#include "TH1.h"
#include "TH2.h"

#include "BaseOperator.h"

template <class EventClass> class DiJetPlotterOperator : public BaseOperator<EventClass> {

  public:
 
    std::vector<std::string> weights_;
    bool root_;
    std::string dir_;

    TH1D h_H0_mass {"h_H0_mass", "", 300, 0., 900.};
    TH1D h_H0_mass_unc_sq {"h_H0_mass_unc_sq", "", 300, 0., 900.};
    TH1D h_H0_pt {"h_H0_pt", "", 300, 0., 900.};
    TH1D h_H0_pt_unc_sq {"h_H0_pt_unc_sq", "", 300, 0., 900.};
    TH1D h_H0_eta {"h_H0_eta", "", 100, -4.0, 4.0};
    TH1D h_H0_eta_unc_sq {"h_H0_eta_unc_sq", "", 100, -4.0, 4.0};
    TH1D h_H1_mass {"h_H1_mass", "", 300, 0., 900.};
    TH1D h_H1_mass_unc_sq {"h_H1_mass_unc_sq", "", 300, 0., 900.};
    TH1D h_H1_pt {"h_H1_pt", "", 300, 0., 900.};
    TH1D h_H1_pt_unc_sq {"h_H1_pt_unc_sq", "", 300, 0., 900.};
    TH1D h_H1_eta {"h_H1_eta", "", 100, -4.0, 4.0};
    TH1D h_H1_eta_unc_sq {"h_H1_eta_unc_sq", "", 100, -4.0, 4.0};
    TH2D h_H0_H1_mass {"h_H0_H1_mass","", 300, 0., 600., 300, 0., 600.};  
    TH2D h_H0_H1_mass_unc_sq {"h_H0_H1_mass_unc_sq","", 300, 0., 600., 300, 0., 600.};  
    TH1D h_H0H1_mass {"h_H0H1_mass", "", 300, 0., 900.};
    TH1D h_H0H1_mass_unc_sq {"h_H0H1_mass_unc_sq", "", 300, 0., 900.};

     DiJetPlotterOperator(const std::vector<std::string> & weights = {}, bool root = false, std::string dir = ""  ) :
      weights_(weights),
      root_(root),
      dir_(dir) {}
    virtual ~DiJetPlotterOperator() {}

    virtual void init(TDirectory * tdir) {
      if (root_) {
        tdir = tdir->GetFile();
        auto ndir = tdir->mkdir(dir_.c_str());
        if (ndir == 0) {
          tdir = tdir->GetDirectory(dir_.c_str());
        } else {
          tdir = ndir;
        }
      }
      h_H0_mass.SetDirectory(tdir);
      h_H0_pt.SetDirectory(tdir);
      h_H0_eta.SetDirectory(tdir);
      h_H1_mass.SetDirectory(tdir);
      h_H1_pt.SetDirectory(tdir);
      h_H1_eta.SetDirectory(tdir);
      h_H0_H1_mass.SetDirectory(tdir);
      h_H0H1_mass.SetDirectory(tdir);
      h_H0_mass_unc_sq.SetDirectory(tdir);
      h_H0_pt_unc_sq.SetDirectory(tdir);
      h_H0_eta_unc_sq.SetDirectory(tdir);
      h_H1_mass_unc_sq.SetDirectory(tdir);
      h_H1_pt_unc_sq.SetDirectory(tdir);
      h_H1_eta_unc_sq.SetDirectory(tdir);
      h_H0_H1_mass_unc_sq.SetDirectory(tdir);
      h_H0H1_mass_unc_sq.SetDirectory(tdir);
      h_H0_mass.Sumw2();
      h_H0_pt.Sumw2();
      h_H0_eta.Sumw2();
      h_H1_mass.Sumw2();
      h_H1_pt.Sumw2();
      h_H1_eta.Sumw2();
      h_H0_H1_mass.Sumw2();
      h_H0H1_mass.Sumw2();
      h_H0_mass_unc_sq.Sumw2();
      h_H0_pt_unc_sq.Sumw2();
      h_H0_eta_unc_sq.Sumw2();
      h_H1_mass_unc_sq.Sumw2();
      h_H1_pt_unc_sq.Sumw2();
      h_H1_eta_unc_sq.Sumw2();
      h_H0_H1_mass_unc_sq.Sumw2();
      h_H0H1_mass_unc_sq.Sumw2();
   }


    virtual bool process( EventClass & ev ) {

      float w = 1.0;
      float w_unc_sq = 1.0;

      h_H0_mass.Fill(ev.dijets_.at(0).mass(), w);
      h_H0_pt.Fill(ev.dijets_.at(0).pt(), w);
      h_H0_eta.Fill(ev.dijets_.at(0).eta(), w);
      h_H1_mass.Fill(ev.dijets_.at(1).mass(), w);
      h_H1_pt.Fill(ev.dijets_.at(1).pt(), w);
      h_H1_eta.Fill(ev.dijets_.at(1).eta(), w);
      h_H0_H1_mass.Fill(ev.dijets_.at(0).mass(), ev.dijets_.at(1).mass(), w);
      h_H0H1_mass.Fill((ev.dijets_.at(0)+ev.dijets_.at(1)).mass(), w);

      h_H0_mass_unc_sq.Fill(ev.dijets_.at(0).mass(), w_unc_sq);
      h_H0_pt_unc_sq.Fill(ev.dijets_.at(0).pt(), w_unc_sq);
      h_H0_eta_unc_sq.Fill(ev.dijets_.at(0).eta(), w_unc_sq);
      h_H1_mass_unc_sq.Fill(ev.dijets_.at(1).mass(), w_unc_sq);
      h_H1_pt_unc_sq.Fill(ev.dijets_.at(1).pt(), w_unc_sq);
      h_H1_eta_unc_sq.Fill(ev.dijets_.at(1).eta(), w_unc_sq);
      h_H0_H1_mass_unc_sq.Fill(ev.dijets_.at(0).mass(), ev.dijets_.at(1).mass(), w_unc_sq);
      h_H0H1_mass_unc_sq.Fill((ev.dijets_.at(0)+ev.dijets_.at(1)).mass(), w_unc_sq);

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
