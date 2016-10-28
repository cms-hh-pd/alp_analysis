
#pragma once

#include <algorithm>

#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"

#include "../interface/BaseOperator.h"

template <class EventClass> class LiveOperator : public BaseOperator<EventClass> {

  public:
 
    // member are all data (e.g. histograms, vectors that
    // have to be kept and filled for each event)
    
    TH1D h_jets_pt {"h_jets_pt", "", 300, 0., 900.};

     LiveOperator() {}
    virtual ~LiveOperator() {}

    // done before processing any event
    virtual void init(TDirectory * tdir) {

      // this is required so histograms are saved in
      // the output file
      h_jets_pt.SetDirectory(tdir);

      h_jets_pt.Sumw2();

    }

    // done for each event (passed as a reference)
    virtual bool process( EventClass & ev ) {

      for (const auto & jet : ev.jets_) {
        h_jets_pt.Fill(jet.pt());
      }

      return true;
    }

    // done at the end (e.g. save output or create/draw canvas) 
    virtual bool output( TFile * tfile) {

      TCanvas c1("c1");
      c1.cd();
      h_jets_pt.Draw();
      c1.Write();

      return true;
    }

};
