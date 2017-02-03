
#pragma once

#include <algorithm>

#include "TH1.h"
#include "TH2.h"

#include "BaseOperator.h"

template <class EventClass> class JetPlotterOperator : public BaseOperator<EventClass> {

  public:
 
    std::string disc_;
    std::vector<std::string> weights_;

    std::vector<std::size_t> j_sortInd_;

    TH1D h_jets_pt {"h_jets_pt", "jets pt", 300, 0., 900.};
    TH1D h_jets_eta {"h_jets_eta", "jets eta", 100, -4.0, 4.0};
    TH1D h_jets_csv {"h_jets_csv", "jets csv", 300,  -1., 1.};
    TH1D h_jets_cmva {"h_jets_cmva", "jets cmva", 300,  -1., 1.};

    TH1D h_jet0_cmva {"h_jet0_cmva", "jet0 cmva", 300,  -1., 1.};
    TH1D h_jet1_cmva {"h_jet1_cmva", "jet2 cmva", 300,  -1., 1.};
    TH1D h_jet2_cmva {"h_jet2_cmva", "jet2 cmva", 300,  -1., 1.};
    TH1D h_jet3_cmva {"h_jet3_cmva", "jet3 cmva", 300,  -1., 1.};

    TH1D h_jets_ht {"h_jets_ht", "jets ht", 500, 0., 1500.};
    TH1D h_jets_ht_r {"h_jets_ht_r", "additional jets ht", 500, 0., 1500.};
    TH1D h_jets_n {"h_jets_n", "# jets", 30,  0., 30.};

    TH1D h_jet0_pt {"h_jet0_pt", "jet0 pt", 300, 0., 900.};
    TH1D h_jet0_eta {"h_jet0_eta", "jet0 eta", 100, -4.0, 4.0};
    TH1D h_jet0_csv {"h_jet0_csv", "jet0 csv", 300,  -1., 1.};
    TH1D h_jet1_pt {"h_jet1_pt", "jet1 pt", 300, 0., 900.};
    TH1D h_jet1_eta {"h_jet1_eta", "jet1 eta", 100, -4.0, 4.0};
    TH1D h_jet1_csv {"h_jet1_csv", "jet1 csv", 300, -1., 1.};
    TH1D h_jet2_pt {"h_jet2_pt", "jet2 pt", 300, 0., 900.};
    TH1D h_jet2_eta {"h_jet2_eta", "jet2 eta", 100, -4.0, 4.0};
    TH1D h_jet2_csv {"h_jet2_csv", "jet2 csv", 300,  -1., 1.};
    TH1D h_jet3_pt {"h_jet3_pt", "jet3 pt", 300, 0., 900.};
    TH1D h_jet3_eta {"h_jet3_eta", "jet3 eta", 100, -4.0, 4.0};
    TH1D h_jet3_csv {"h_jet3_csv", "jet3 csv", 300,  -1., 1.};

    //jets sorted in pt
    TH1D h_jet0pt_pt {"h_jet0pt_pt", "jet0pt pt", 300, 0., 900.};
    TH1D h_jet1pt_pt {"h_jet1pt_pt", "jet1pt pt", 300, 0., 900.};
    TH1D h_jet2pt_pt {"h_jet2pt_pt", "jet2pt pt", 300, 0., 900.};
    TH1D h_jet3pt_pt {"h_jet3pt_pt", "jet3pt pt", 300, 0., 900.};

     JetPlotterOperator(std::string disc, const std::vector<std::string> & weights = {}) :
      disc_(disc),
      weights_(weights) {}
    virtual ~JetPlotterOperator() {}

    virtual void init(TDirectory * tdir) {

      h_jets_pt.SetDirectory(tdir);
      h_jets_eta.SetDirectory(tdir);
      h_jets_csv.SetDirectory(tdir);
      h_jets_cmva.SetDirectory(tdir);

      h_jet0_cmva.SetDirectory(tdir);
      h_jet1_cmva.SetDirectory(tdir);
      h_jet2_cmva.SetDirectory(tdir);
      h_jet3_cmva.SetDirectory(tdir);

      h_jets_n.SetDirectory(tdir);
      h_jets_ht.SetDirectory(tdir);
      h_jets_ht_r.SetDirectory(tdir);
      h_jet0_pt.SetDirectory(tdir);
      h_jet0_eta.SetDirectory(tdir);
      h_jet0_csv.SetDirectory(tdir);
      h_jet1_pt.SetDirectory(tdir);
      h_jet1_eta.SetDirectory(tdir);
      h_jet1_csv.SetDirectory(tdir);
      h_jet2_pt.SetDirectory(tdir);
      h_jet2_eta.SetDirectory(tdir);
      h_jet2_csv.SetDirectory(tdir);
      h_jet3_pt.SetDirectory(tdir);
      h_jet3_eta.SetDirectory(tdir);
      h_jet3_csv.SetDirectory(tdir);

      h_jet0pt_pt.SetDirectory(tdir);
      h_jet1pt_pt.SetDirectory(tdir);
      h_jet2pt_pt.SetDirectory(tdir);
      h_jet3pt_pt.SetDirectory(tdir);

      h_jets_pt.Sumw2();
      h_jets_eta.Sumw2();
      h_jets_csv.Sumw2();
      h_jets_cmva.Sumw2();

      h_jet0_cmva.Sumw2();
      h_jet1_cmva.Sumw2();
      h_jet2_cmva.Sumw2();
      h_jet3_cmva.Sumw2();

      h_jets_n.Sumw2();
      h_jets_ht.Sumw2();
      h_jets_ht_r.Sumw2();
      h_jet0_pt.Sumw2();
      h_jet0_eta.Sumw2();
      h_jet0_csv.Sumw2();
      h_jet1_pt.Sumw2();
      h_jet1_eta.Sumw2();
      h_jet1_csv.Sumw2();
      h_jet2_pt.Sumw2();
      h_jet2_eta.Sumw2();
      h_jet2_csv.Sumw2();
      h_jet3_pt.Sumw2();
      h_jet3_eta.Sumw2();
      h_jet3_csv.Sumw2();

      h_jet0pt_pt.Sumw2();
      h_jet1pt_pt.Sumw2();
      h_jet2pt_pt.Sumw2();
      h_jet3pt_pt.Sumw2();
   }


    virtual bool process( EventClass & ev ) {
      float w = 1.0;
      w*=ev.eventInfo_.eventWeight(weights_);

      // get pt sorting
      std::string d_ = "pt";
      get_sortIndex_jets(j_sortInd_, ev.jets_, d_);
      h_jet0pt_pt.Fill(ev.jets_.at(j_sortInd_.at(0)).pt(), w);
      h_jet1pt_pt.Fill(ev.jets_.at(j_sortInd_.at(1)).pt(), w);
      h_jet2pt_pt.Fill(ev.jets_.at(j_sortInd_.at(2)).pt(), w);
      h_jet3pt_pt.Fill(ev.jets_.at(j_sortInd_.at(3)).pt(), w);

      // get index of ordering by discriminator - do not change ev.jets_ sorting.
      get_sortIndex_jets(j_sortInd_, ev.jets_, disc_);

      auto ht = get_jets_ht(ev.jets_);
      auto ht_r = ht -(ev.jets_.at(j_sortInd_.at(0)).pt() + ev.jets_.at(j_sortInd_.at(1)).pt() +
                       ev.jets_.at(j_sortInd_.at(2)).pt() + ev.jets_.at(j_sortInd_.at(3)).pt() ) ; 

      for (const auto & jet : ev.jets_) {
        h_jets_pt.Fill(jet.pt(), w);
        h_jets_eta.Fill(jet.eta(), w);
        h_jets_csv.Fill(jet.CSV(), w);
        h_jets_cmva.Fill(jet.CMVA(), w);
      }

      h_jet0_cmva.Fill(ev.jets_.at(j_sortInd_.at(0)).CMVA(), w);
      h_jet1_cmva.Fill(ev.jets_.at(j_sortInd_.at(1)).CMVA(), w);
      h_jet2_cmva.Fill(ev.jets_.at(j_sortInd_.at(2)).CMVA(), w);
      h_jet3_cmva.Fill(ev.jets_.at(j_sortInd_.at(3)).CMVA(), w);

      h_jets_n.Fill(ev.jets_.size(), w);
      h_jets_ht.Fill(ht, w);
      h_jets_ht_r.Fill(ht_r, w);
      h_jet0_pt.Fill(ev.jets_.at(j_sortInd_.at(0)).pt(), w);
      h_jet0_eta.Fill(ev.jets_.at(j_sortInd_.at(0)).eta(), w);
      h_jet0_csv.Fill(ev.jets_.at(j_sortInd_.at(0)).CSV(), w);
      h_jet1_pt.Fill(ev.jets_.at(j_sortInd_.at(1)).pt(), w);
      h_jet1_eta.Fill(ev.jets_.at(j_sortInd_.at(1)).eta(), w);
      h_jet1_csv.Fill(ev.jets_.at(j_sortInd_.at(1)).CSV(), w);
      h_jet2_pt.Fill(ev.jets_.at(j_sortInd_.at(2)).pt(), w);
      h_jet2_eta.Fill(ev.jets_.at(j_sortInd_.at(2)).eta(), w);
      h_jet2_csv.Fill(ev.jets_.at(j_sortInd_.at(2)).CSV(), w);
      h_jet3_pt.Fill(ev.jets_.at(j_sortInd_.at(3)).pt(), w);
      h_jet3_eta.Fill(ev.jets_.at(j_sortInd_.at(3)).eta(), w);
      h_jet3_csv.Fill(ev.jets_.at(j_sortInd_.at(3)).CSV(), w);

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
