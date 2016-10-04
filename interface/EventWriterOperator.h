
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"

#include "mut_framework/mut_dataformats/interface/EventInfo.h"
#include "mut_framework/mut_dataformats/interface/Jet.h"
#include "mut_framework/mut_dataformats/interface/MET.h"

template <class EventClass> class EventWriterOperator : public BaseOperator<EventClass> {

  public:
 
    bool root_;
    std::string dir_;

    // variables to save in branches
    std::vector<alp::Jet> * jets_ptr = nullptr;
    std::vector<alp::PtEtaPhiEVector> * dijets_ptr = nullptr;


    TTree tree_{"tree","Tree using simplified mut::dataformats"};

     EventWriterOperator(bool root = false, std::string dir = "") :
      root_(root),
      dir_(dir) {}
    virtual ~EventWriterOperator() {}

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
      tree_.Branch("Jets","std::vector<alp::Jet>",&jets_ptr, 64000, 2);
      tree_.Branch("DiJets","std::vector<alp::PtEtaPhiEVector>", &dijets_ptr, 64000, 2);


      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {


      // to fill tree redirect pointers
      jets_ptr = dynamic_cast<std::vector<alp::Jet> *>(&ev.jets_); 
      dijets_ptr = dynamic_cast<std::vector<alp::PtEtaPhiEVector> *>(&ev.dijets_); 

      tree_.Fill();

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
