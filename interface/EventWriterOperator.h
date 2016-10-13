
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"

template <class EventClass> class EventWriterOperator : public BaseOperator<EventClass> {

  public:
 
    bool root_;
    std::string dir_;
    long n_ev_ = 0; 

    //count histos
    TH1D h_nevts {"h_nevts", "number of events", 1, 0., 1.};

    // variables to save in branches
    std::vector<alp::Jet> * jets_ptr = nullptr;
    std::vector<alp::PtEtaPhiEVector> * dijets_ptr = nullptr;
    std::vector<float> * muons_pt_ptr = nullptr;
    std::vector<float> * muons_pfiso03_ptr = nullptr;
    float met_pt = 0.;
    bool hlt0 = false;
    bool hlt1 = false;
    bool hlt2 = false;
    bool hlt3 = false;

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
      h_nevts.SetDirectory(tdir);

      tree_.Branch("Jets","std::vector<alp::Jet>",&jets_ptr, 64000, 2);
      tree_.Branch("DiJets","std::vector<alp::PtEtaPhiEVector>", &dijets_ptr, 64000, 2);

      tree_.Branch("muons.pt","std::vector<float>", &muons_pt_ptr, 64000, 2);
      tree_.Branch("muons.pfiso03","std::vector<float>", &muons_pfiso03_ptr, 64000, 2);
      tree_.Branch("met_pt",&met_pt,"met_pt/F");
      tree_.Branch("hlt_0",&hlt0,"hlt_0/O");
      tree_.Branch("hlt_1",&hlt1,"hlt_1/O");
      tree_.Branch("hlt_2",&hlt2,"hlt_2/O");
      tree_.Branch("hlt_3",&hlt3,"hlt_3/O"); //DEBUG -- not fix number!

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {

      n_ev_++;

      // to fill tree redirect pointers
      jets_ptr = dynamic_cast<std::vector<alp::Jet> *>(&ev.jets_); 
      dijets_ptr = dynamic_cast<std::vector<alp::PtEtaPhiEVector> *>(&ev.dijets_); 
      //additional variables - to be changed to objects
      muons_pt_ptr = dynamic_cast<std::vector<float> *>(&ev.muons_pt_); 
      muons_pfiso03_ptr = dynamic_cast<std::vector<float> *>(&ev.muons_pfiso03_); 
      met_pt = ev.met_pt_; //note: to be checked

      hlt0 = ev.hlt_bits_.at(0).second; //DEBUG 
      hlt1 = ev.hlt_bits_.at(1).second; //DEBUG 
      hlt2 = ev.hlt_bits_.at(2).second; //DEBUG 
      hlt3 = hlt0 + hlt1; //DEBUG        

      tree_.Fill();

      return true;
    }

    virtual bool output( TFile * tfile) {

     // tree_.Write("",TObject::kWriteDelete); // it does not solve double tree issue
      h_nevts.SetBinContent(1, n_ev_);

      return true;

    }

};
