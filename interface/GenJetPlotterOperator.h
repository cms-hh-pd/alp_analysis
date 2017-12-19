
#pragma once

#include <algorithm>

#include "TH1.h"
#include "TH2.h"

#include "BaseOperator.h"

template <class EventClass> class GenJetPlotterOperator : public BaseOperator<EventClass> {

  public:
 
    std::string disc_;
    std::vector<std::string> weights_;

    std::vector<std::size_t> j_sortInd_;

    TH1D h_gjets_pt {"h_gjets_pt", "gen jets pt", 300, 0., 900.};
    TH1D h_gjets_eta {"h_gjets_eta", "gen jets eta", 100, -4.0, 4.0};

    TH1D h_gjets_ht {"h_gjets_ht", "gen jets ht", 500, 0., 1500.};
    TH1D h_gjets_n {"h_gjets_n", "# gen jets", 30,  0., 30.};

    TH1D h_gjet0_pt {"h_gjet0_pt", "gen jet0 pt", 300, 0., 900.};
    TH1D h_gjet0_eta {"h_gjet0_eta", "gen jet0 eta", 100, -4.0, 4.0};
    TH1D h_gjet1_pt {"h_gjet1_pt", "gen jet1 pt", 300, 0., 900.};
    TH1D h_gjet1_eta {"h_gjet1_eta", "gen jet1 eta", 100, -4.0, 4.0};
    TH1D h_gjet2_pt {"h_gjet2_pt", "gen jet2 pt", 300, 0., 900.};
    TH1D h_gjet2_eta {"h_gjet2_eta", "gen jet2 eta", 100, -4.0, 4.0};
    TH1D h_gjet3_pt {"h_gjet3_pt", "gen jet3 pt", 300, 0., 900.};
    TH1D h_gjet3_eta {"h_gjet3_eta", "gen jet3 eta", 100, -4.0, 4.0};

    //jets sorted in pt
    TH1D h_gjet0pt_pt {"h_gjet0pt_pt", "gen jet0pt pt", 300, 0., 900.};
    TH1D h_gjet1pt_pt {"h_gjet1pt_pt", "gen jet1pt pt", 300, 0., 900.};
    TH1D h_gjet2pt_pt {"h_gjet2pt_pt", "gen jet2pt pt", 300, 0., 900.};
    TH1D h_gjet3pt_pt {"h_gjet3pt_pt", "gen jet3pt pt", 300, 0., 900.};

    //new
    TH1D h_gjetspt_eta0 {"h_gjetspt_eta0", "gen jets pt", 10, 0., 100.};
    TH1D h_gjetspt_eta1 {"h_gjetspt_eta1", "gen jets pt", 10, 0., 100.};
    TH1D h_gjetspt_eta2 {"h_gjetspt_eta2", "gen jets pt", 10, 0., 100.};
    TH1D h_gjetspt {"h_gjetspt", "gen jets pt", 10, 0., 100.};
    
    GenJetPlotterOperator(std::string disc) :
      disc_(disc) {}
    virtual ~GenJetPlotterOperator() {}

    virtual void init(TDirectory * tdir) {

      h_gjets_pt.SetDirectory(tdir);
      h_gjets_eta.SetDirectory(tdir);

      h_gjets_n.SetDirectory(tdir);
      h_gjets_ht.SetDirectory(tdir);
      h_gjet0_pt.SetDirectory(tdir);
      h_gjet0_eta.SetDirectory(tdir);
      h_gjet1_pt.SetDirectory(tdir);
      h_gjet1_eta.SetDirectory(tdir);
      h_gjet2_pt.SetDirectory(tdir);
      h_gjet2_eta.SetDirectory(tdir);
      h_gjet3_pt.SetDirectory(tdir);
      h_gjet3_eta.SetDirectory(tdir);

      h_gjet0pt_pt.SetDirectory(tdir);
      h_gjet1pt_pt.SetDirectory(tdir);
      h_gjet2pt_pt.SetDirectory(tdir);
      h_gjet3pt_pt.SetDirectory(tdir);

      h_gjetspt_eta0.SetDirectory(tdir);
      h_gjetspt_eta1.SetDirectory(tdir);
      h_gjetspt_eta2.SetDirectory(tdir);
      h_gjetspt.SetDirectory(tdir);

      h_gjets_pt.Sumw2();
      h_gjets_eta.Sumw2();

      h_gjets_n.Sumw2();
      h_gjets_ht.Sumw2();
      h_gjet0_pt.Sumw2();
      h_gjet0_eta.Sumw2();
      h_gjet1_pt.Sumw2();
      h_gjet1_eta.Sumw2();
      h_gjet2_pt.Sumw2();
      h_gjet2_eta.Sumw2();
      h_gjet3_pt.Sumw2();
      h_gjet3_eta.Sumw2();

      h_gjet0pt_pt.Sumw2();
      h_gjet1pt_pt.Sumw2();
      h_gjet2pt_pt.Sumw2();
      h_gjet3pt_pt.Sumw2();

      h_gjetspt_eta0.Sumw2();
      h_gjetspt_eta1.Sumw2();
      h_gjetspt_eta2.Sumw2();
      h_gjetspt.Sumw2();

   }


    virtual bool process( EventClass & ev ) {


      float_t w = 1.;
      int siz = ev.genbfromhs_.size();

      for (const auto & jet : ev.genbfromhs_) {
        h_gjets_pt.Fill(jet.pt(), w);
        h_gjets_eta.Fill(jet.eta(), w);
      }

      h_gjets_n.Fill(siz, w);
      if(siz < 1) return false;
      if(siz >= 1){
        h_gjet0_pt.Fill(ev.genbfromhs_.at(0).pt(), w);
        h_gjet0_eta.Fill(ev.genbfromhs_.at(0).eta(), w); }
      if(siz >= 2){
        h_gjet1_pt.Fill(ev.genbfromhs_.at(1).pt(), w);
        h_gjet1_eta.Fill(ev.genbfromhs_.at(1).eta(), w); }
      if(siz >= 3){
        h_gjet2_pt.Fill(ev.genbfromhs_.at(2).pt(), w);
        h_gjet2_eta.Fill(ev.genbfromhs_.at(2).eta(), w); }
      if(siz >= 4){
        h_gjet3_pt.Fill(ev.genbfromhs_.at(3).pt(), w);
        h_gjet3_eta.Fill(ev.genbfromhs_.at(3).eta(), w); }

      /*
      // get pt sorting
      std::string d_ = "pt";
      get_sortIndex_jets(j_sortInd_, ev.genbfromhs_, d_);
      h_gjet0pt_pt.Fill(ev.genbfromhs_.at(j_sortInd_.at(0)).pt(), w);
      h_gjet1pt_pt.Fill(ev.genbfromhs_.at(j_sortInd_.at(1)).pt(), w);
      h_gjet2pt_pt.Fill(ev.genbfromhs_.at(j_sortInd_.at(2)).pt(), w);
      h_gjet3pt_pt.Fill(ev.genbfromhs_.at(j_sortInd_.at(3)).pt(), w);
      int i=0;
      h_gjetspt.Fill(ev.genbfromhs_.at(0).pt());
      h_gjetspt.Fill(ev.genbfromhs_.at(1).pt());
      h_gjetspt.Fill(ev.genbfromhs_.at(2).pt());
      h_gjetspt.Fill(ev.genbfromhs_.at(3).pt());

      if(ev.genbfromhs_.at(0).eta()<2.5 && ev.genbfromhs_.at(1).eta()<2.5
           && ev.genbfromhs_.at(2).eta()<2.5 && ev.genbfromhs_.at(3).eta()<2.5) {
           h_gjetspt_eta0.Fill(ev.genbfromhs_.at(0).pt());
           h_gjetspt_eta0.Fill(ev.genbfromhs_.at(1).pt());
           h_gjetspt_eta0.Fill(ev.genbfromhs_.at(2).pt());
           h_gjetspt_eta0.Fill(ev.genbfromhs_.at(3).pt());
       }
      if(ev.genbfromhs_.at(0).eta()<3. && ev.genbfromhs_.at(1).eta()<3.
           && ev.genbfromhs_.at(2).eta()<3. && ev.genbfromhs_.at(3).eta()<3.) {
           h_gjetspt_eta1.Fill(ev.genbfromhs_.at(0).pt());
           h_gjetspt_eta1.Fill(ev.genbfromhs_.at(1).pt());
           h_gjetspt_eta1.Fill(ev.genbfromhs_.at(2).pt());
           h_gjetspt_eta1.Fill(ev.genbfromhs_.at(3).pt());
       }
      if(ev.genbfromhs_.at(0).eta()<4. && ev.genbfromhs_.at(1).eta()<4.
           && ev.genbfromhs_.at(2).eta()<4. && ev.genbfromhs_.at(3).eta()<4.) {
           h_gjetspt_eta2.Fill(ev.genbfromhs_.at(0).pt());
           h_gjetspt_eta2.Fill(ev.genbfromhs_.at(1).pt());
           h_gjetspt_eta2.Fill(ev.genbfromhs_.at(2).pt());
           h_gjetspt_eta2.Fill(ev.genbfromhs_.at(3).pt());
       }*/

      return true;
    }

    virtual bool output( TFile * tfile) {
      return true;

    }

};
