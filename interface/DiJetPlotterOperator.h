
#pragma once

#include <algorithm>

#include "TH1.h"
#include "TH2.h"

#include "BaseOperator.h"
#include "Utils.h"

template <class EventClass> class DiJetPlotterOperator : public BaseOperator<EventClass> {

  public:
 
    std::vector<std::string> weights_;
 
    TH1D h_H0_mass   {"h_H0_mass",   "leading di-jet mass"    , 300, 0., 900.};
    TH1D h_H0_pt     {"h_H0_pt"  ,   "leading di-jet pt"      , 300, 0., 900.};
    TH1D h_H0_eta    {"h_H0_eta" ,   "leading di-jet eta"     , 100, -4.0, 4.0};
    TH1D h_H0_csthst0_a {"h_H0_csthst0_a", "jet0 - leading di-jet |costh*|"  , 100, 0., 1.};
    TH1D h_H0_csthst1_a {"h_H0_csthst1_a", "jet1 - leading di-jet |costh*|"  , 100, 0., 1.};
    TH1D h_H0_dr     {"h_H0_dr"   ,  "leading di-jet deltaR"  , 100, 0., 7.};
    TH1D h_H0_deta   {"h_H0_deta" ,  "leading di-jet deltaEta", 100, -4.0, 4.0};
    TH1D h_H0_dphi   {"h_H0_dphi" ,  "leading di-jet deltaPhi", 100, -4.0, 4.0};
    TH1D h_H0_deta_a {"h_H0_deta_a", "leading di-jet deltaEta", 100, 0., 4.0};
    TH1D h_H0_dphi_a {"h_H0_dphi_a", "leading di-jet deltaPhi", 100, 0., 4.0};

    TH1D h_H1_mass   {"h_H1_mass",   "trailing di-jet mass"    ,300, 0., 900.};
    TH1D h_H1_pt     {"h_H1_pt"  ,   "trailing di-jet pt"      ,300, 0., 900.};
    TH1D h_H1_eta    {"h_H1_eta" ,   "trailing di-jet eta"     ,100, -4.0, 4.0};
    TH1D h_H1_csthst2_a {"h_H1_csthst2_a", "jet2 - trailing di-jet |costh*|"  ,100, 0., 1.};
    TH1D h_H1_csthst3_a {"h_H1_csthst3_a", "jet3 - trailing di-jet |costh*|"  ,100, 0., 1.};
    TH1D h_H1_dr     {"h_H1_dr"   ,  "trailing di-jet deltaR"  ,100, 0., 7.};
    TH1D h_H1_deta   {"h_H1_deta" ,  "trailing di-jet deltaEta",100, -4.0, 4.0};
    TH1D h_H1_dphi   {"h_H1_dphi" ,  "trailing di-jet deltaPhi",100, -4.0, 4.0};
    TH1D h_H1_deta_a {"h_H1_deta_a", "trailing di-jet deltaEta",100, 0., 4.0};
    TH1D h_H1_dphi_a {"h_H1_dphi_a", "trailing di-jet deltaPhi",100, 0., 4.0};

    TH1D h_H0H1_mass {"h_H0H1_mass", "four-body mass"    , 300, 0., 1200.};
    TH1D h_X_mass {"h_X_mass", "X mass"    , 300, 0., 1200.};
    TH1D h_H0H1_pt   {"h_H0H1_pt"  , "four-body pt"      , 300, 0., 900.};
    TH1D h_H0H1_eta  {"h_H0H1_eta" , "four-body eta"     , 100, -6.0, 6.0};
    TH1D h_H0H1_csthst0_a {"h_H0H1_csthst0_a", "dijet0 - four-body |costh*|"  ,100, 0., 1.};
    TH1D h_H0H1_csthst1_a {"h_H0H1_csthst1_a", "dijet1 - four-body |costh*|"  ,100, 0., 1.};
    TH1D h_H0H1_dr   {"h_H0H1_dr"  , "four-body deltaR"  , 100, 0., 7.};
    TH1D h_H0H1_deta {"h_H0H1_deta", "four-body deltaEta", 100, -4.0, 4.0};
    TH1D h_H0H1_dphi {"h_H0H1_dphi", "four-body deltaPhi", 100, -4.0, 4.0};
    TH1D h_H0H1_deta_a {"h_H0H1_deta_a", "four-body deltaEta", 100, 0., 4.0};
    TH1D h_H0H1_dphi_a {"h_H0H1_dphi_a", "four-body deltaPhi", 100, 0., 4.0};

    TH2D h_H0_H1_mass {"h_H0_H1_mass","", 300, 0., 600., 300, 0., 600.};  

     DiJetPlotterOperator(const std::vector<std::string> & weights = {}) :
      weights_(weights) {}
    virtual ~DiJetPlotterOperator() {}

    virtual void init(TDirectory * tdir) {

      h_H0_mass.SetDirectory(tdir);
      h_H0_pt.SetDirectory(tdir);
      h_H0_eta.SetDirectory(tdir);
      h_H0_csthst0_a.SetDirectory(tdir);
      h_H0_csthst1_a.SetDirectory(tdir);
      h_H0_dr.SetDirectory(tdir);
      h_H0_deta.SetDirectory(tdir);
      h_H0_dphi.SetDirectory(tdir);
      h_H0_deta_a.SetDirectory(tdir);
      h_H0_dphi_a.SetDirectory(tdir);
      h_H1_mass.SetDirectory(tdir);
      h_H1_pt.SetDirectory(tdir);
      h_H1_eta.SetDirectory(tdir);
      h_H1_csthst2_a.SetDirectory(tdir);
      h_H1_csthst3_a.SetDirectory(tdir);
      h_H1_dr.SetDirectory(tdir);
      h_H1_deta.SetDirectory(tdir);
      h_H1_dphi.SetDirectory(tdir);
      h_H1_deta_a.SetDirectory(tdir);
      h_H1_dphi_a.SetDirectory(tdir);
      h_H0H1_mass.SetDirectory(tdir);
      h_X_mass.SetDirectory(tdir);
      h_H0H1_pt.SetDirectory(tdir);
      h_H0H1_eta.SetDirectory(tdir);
      h_H0H1_csthst0_a.SetDirectory(tdir);
      h_H0H1_csthst1_a.SetDirectory(tdir);
      h_H0H1_dr.SetDirectory(tdir);
      h_H0H1_deta.SetDirectory(tdir);
      h_H0H1_dphi.SetDirectory(tdir);
      h_H0H1_deta_a.SetDirectory(tdir);
      h_H0H1_dphi_a.SetDirectory(tdir);
      h_H0_H1_mass.SetDirectory(tdir);
      h_H0_mass.Sumw2();
      h_X_mass.Sumw2();
      h_H0_pt.Sumw2();
      h_H0_eta.Sumw2();
      h_H0_csthst0_a.Sumw2();
      h_H0_csthst1_a.Sumw2();
      h_H0_dr.Sumw2();
      h_H0_deta.Sumw2();
      h_H0_dphi.Sumw2();
      h_H0_deta_a.Sumw2();
      h_H0_dphi_a.Sumw2();
      h_H1_mass.Sumw2();
      h_H1_pt.Sumw2();
      h_H1_eta.Sumw2();
      h_H1_csthst2_a.Sumw2();
      h_H1_csthst3_a.Sumw2();
      h_H1_dr.Sumw2();
      h_H1_deta.Sumw2();
      h_H1_dphi.Sumw2();
      h_H1_deta_a.Sumw2();
      h_H1_dphi_a.Sumw2();
      h_H0H1_mass.Sumw2();
      h_H0H1_pt.Sumw2();
      h_H0H1_eta.Sumw2();
      h_H0H1_csthst0_a.Sumw2();
      h_H0H1_csthst1_a.Sumw2();
      h_H0H1_dr.Sumw2();
      h_H0H1_deta.Sumw2();
      h_H0H1_dphi.Sumw2();
      h_H0H1_deta_a.Sumw2();
      h_H0H1_dphi_a.Sumw2();

      h_H0_H1_mass.Sumw2();
   }


    virtual bool process( EventClass & ev ) {

      float w = 1.;
      if(weights_.size()>0) w *= ev.eventInfo_.eventWeight(weights_); //multiplied all weights from cfg
      else w *= ev.evtWeight_;

     // debug - jets already sorted accordingly to pairing
      h_H0_mass.Fill(ev.dijets_.at(0).mass(), w);
      h_H0_pt.Fill(ev.dijets_.at(0).pt(), w);
      h_H0_eta.Fill(ev.dijets_.at(0).eta(), w);
      h_H0_csthst0_a.Fill(ev.dijets_.at(0).costhst(), w);
      h_H0_csthst1_a.Fill(ev.dijets_.at(0).costhst1(), w); //computed using second jet
      h_H0_dr.Fill(ev.dijets_.at(0).dr(), w);
      h_H0_deta.Fill(ev.dijets_.at(0).deta(), w);
      h_H0_dphi.Fill(ev.dijets_.at(0).dphi(), w);
      h_H0_deta_a.Fill(ev.dijets_.at(0).detaabs(), w);
      h_H0_dphi_a.Fill(ev.dijets_.at(0).dphiabs(), w);

      h_H1_mass.Fill(ev.dijets_.at(1).mass(), w);
      h_H1_pt.Fill(ev.dijets_.at(1).pt(), w);
      h_H1_eta.Fill(ev.dijets_.at(1).eta(), w);
      h_H1_csthst2_a.Fill(ev.dijets_.at(1).costhst(), w);
      h_H1_csthst3_a.Fill(ev.dijets_.at(1).costhst1(), w); //computed using second jet
      h_H1_dr.Fill(ev.dijets_.at(1).dr(), w);
      h_H1_deta.Fill(ev.dijets_.at(1).deta(), w);
      h_H1_dphi.Fill(ev.dijets_.at(1).dphi(), w);
      h_H1_deta_a.Fill(ev.dijets_.at(1).detaabs(), w);
      h_H1_dphi_a.Fill(ev.dijets_.at(1).dphiabs(), w);

      h_H0H1_mass.Fill(ev.dihiggs_.at(0).mass(), w);
      h_X_mass.Fill(ev.dihiggs_.at(0).mass()-ev.dijets_.at(0).mass()-ev.dijets_.at(1).mass()+2*125., w);
      h_H0H1_pt.Fill(ev.dihiggs_.at(0).pt(), w);
      h_H0H1_eta.Fill(ev.dihiggs_.at(0).eta(), w);
      h_H0H1_csthst0_a.Fill(ev.dihiggs_.at(0).costhst(), w);
      h_H0H1_csthst1_a.Fill(ev.dihiggs_.at(0).costhst1(), w); //computed using second dijet
      h_H0H1_dr.Fill(ev.dihiggs_.at(0).dr(), w);
      h_H0H1_deta.Fill(ev.dihiggs_.at(0).deta(), w);
      h_H0H1_dphi.Fill(ev.dihiggs_.at(0).dphi(), w);
      h_H0H1_deta_a.Fill(ev.dihiggs_.at(0).detaabs(), w);
      h_H0H1_dphi_a.Fill(ev.dihiggs_.at(0).dphiabs(), w);

      h_H0_H1_mass.Fill(ev.dijets_.at(0).mass(), ev.dijets_.at(1).mass(), w);

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
