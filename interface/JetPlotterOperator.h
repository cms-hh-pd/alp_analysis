
#pragma once

#include <algorithm>

#include "TH1.h"
#include "TH2.h"

#include "BaseOperator.h"

template <class EventClass> class JetPlotterOperator : public BaseOperator<EventClass> {

  public:
 
    std::string disc_;
    std::vector<std::string> weights_;
    bool root_;
    std::string dir_;

    TH1D h_jets_ht {"h_jets_ht", "", 300, 0., 900.};
    TH1D h_jet3_csv {"h_jet3_csv", "", 300, -12., 1.};
    TH1D h_jet3_csv_unc_sq {"h_jet3_csv_unc_sq", "", 300,  -12., 1.};
    TH1D h_jet3_pt {"h_jet3_pt", "", 300, 0., 900.};
    TH1D h_jet3_pt_unc_sq {"h_jet3_pt_unc_sq", "", 300, 0., 900.};
    TH1D h_jet3_eta {"h_jet3_eta", "", 100, -4.0, 4.0};
    TH1D h_jet3_eta_unc_sq {"h_jet3_eta_unc_sq", "", 100, -4.0, 4.0};
    TH1D h_jet4_csv {"h_jet4_csv", "", 300,  -12., 1.};
    TH1D h_jet4_csv_unc_sq {"h_jet4_csv_unc_sq", "", 300,  -12., 1.};
    TH1D h_jet4_pt {"h_jet4_pt", "", 300, 0., 900.};
    TH1D h_jet4_pt_unc_sq {"h_jet4_pt_unc_sq", "", 300, 0., 900.};
    TH1D h_jet4_eta {"h_jet4_eta", "", 100, -4.0, 4.0};
    TH1D h_jet4_eta_unc_sq {"h_jet4_eta_unc_sq", "", 100, -4.0, 4.0};

     JetPlotterOperator(std::string disc, const std::vector<std::string> & weights = {}, bool root = false, std::string dir = ""  ) :
      disc_(disc),
      weights_(weights),
      root_(root),
      dir_(dir) {}
    virtual ~JetPlotterOperator() {}

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
      h_jets_ht.SetDirectory(tdir);
      h_jet3_csv.SetDirectory(tdir);
      h_jet3_pt.SetDirectory(tdir);
      h_jet3_eta.SetDirectory(tdir);
      h_jet4_csv.SetDirectory(tdir);
      h_jet4_pt.SetDirectory(tdir);
      h_jet4_eta.SetDirectory(tdir);
      h_jet3_csv_unc_sq.SetDirectory(tdir);
      h_jet3_pt_unc_sq.SetDirectory(tdir);
      h_jet3_eta_unc_sq.SetDirectory(tdir);
      h_jet4_csv_unc_sq.SetDirectory(tdir);
      h_jet4_pt_unc_sq.SetDirectory(tdir);
      h_jet4_eta_unc_sq.SetDirectory(tdir);
      h_jets_ht.Sumw2();
      h_jet3_csv.Sumw2();
      h_jet3_pt.Sumw2();
      h_jet3_eta.Sumw2();
      h_jet4_csv.Sumw2();
      h_jet4_pt.Sumw2();
      h_jet4_eta.Sumw2();
      h_jet3_csv_unc_sq.Sumw2();
      h_jet3_pt_unc_sq.Sumw2();
      h_jet3_eta_unc_sq.Sumw2();
      h_jet4_csv_unc_sq.Sumw2();
      h_jet4_pt_unc_sq.Sumw2();
      h_jet4_eta_unc_sq.Sumw2();
   }


    virtual bool process( EventClass & ev ) {

      float w = 1.0;
      float w_unc_sq = 1.0;

      // order by discriminator
      order_jets_by_disc(ev.jets_, disc_);

      float ht = 0.;
      for(auto iter= ev.jets_.begin(); iter != ev.jets_.end(); iter++){
        ht += (*iter).pt();
      }      
      h_jets_ht.Fill(ht, w);

     // h_jet3_csv.Fill(ev.jets_.at(0).csv(), w);
      h_jet3_pt.Fill(ev.jets_.at(2).pt(), w);
      h_jet3_eta.Fill(ev.jets_.at(2).eta(), w);
      h_jet3_csv.Fill(ev.jets_.at(2).CSV(), w);
     //h_jet4_csv.Fill(ev.jets_.at(1).csv(), w);
      h_jet4_pt.Fill(ev.jets_.at(3).pt(), w);
      h_jet4_eta.Fill(ev.jets_.at(3).eta(), w);
      h_jet4_csv.Fill(ev.jets_.at(3).CSV(), w);

    /*  h_jet3_csv_unc_sq.Fill(ev.jets_.at(0).csv(), w_unc_sq);
      h_jet3_pt_unc_sq.Fill(ev.jets_.at(0).pt(), w_unc_sq);
      h_jet3_eta_unc_sq.Fill(ev.jets_.at(0).eta(), w_unc_sq);
      h_jet4_csv_unc_sq.Fill(ev.jets_.at(1).csv(), w_unc_sq);
      h_jet4_pt_unc_sq.Fill(ev.jets_.at(1).pt(), w_unc_sq);
      h_jet4_eta_unc_sq.Fill(ev.jets_.at(1).eta(), w_unc_sq);*/

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
