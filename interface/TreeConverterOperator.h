
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"
#include "json.hpp"

// for convenience
using json = nlohmann::json;

template <class EventClass> class TreeConverterOperator : public BaseOperator<EventClass> {

  public:
 
    // variables to save in branches
    float_t jet0_pt = 0.;
    float_t jet0_eta = 0.;
    float_t jet0_csv = 0.;

    float_t dijet0_pt = 0.;
    float_t dijet0_eta = 0.;
    float_t dijet0_phi = 0.;
    float_t dijet0_energy = 0.;

    float_t dijet1_pt = 0.;
    float_t dijet1_eta = 0.;
    float_t dijet1_phi = 0.;
    float_t dijet1_energy = 0.;

    std::vector<std::string> weights_;

    TTree tree_{"tree","Tree using  dataformats"};

    json config_ = {};

    TreeConverterOperator(const std::vector<std::string> & weights = {}) :
      weights_(weights) {}

    virtual ~TreeConverterOperator() {}

    virtual void init(TDirectory * tdir) {

      tree_.Branch("jet0_pt", &jet0_pt, "jet0_pt/F");
      tree_.Branch("jet0_eta", &jet0_eta, "jet0_eta/F");
      tree_.Branch("jet0_csv", &jet0_csv, "jet0_csv/F");

      tree_.Branch("dijet0_pt",   &dijet0_pt,   "dijet0_pt/F");
      tree_.Branch("dijet0_eta",  &dijet0_eta,  "dijet0_eta/F");
      tree_.Branch("dijet0_phi",  &dijet0_phi,  "dijet0_phi/F");
      tree_.Branch("dijet0_energy",    &dijet0_energy, "dijet0_energy/F");

      tree_.Branch("dijet1_pt",   &dijet1_pt,   "dijet1_pt/F");
      tree_.Branch("dijet1_eta",  &dijet1_eta,  "dijet1_eta/F");
      tree_.Branch("dijet1_phi",  &dijet1_phi,  "dijet1_phi/F");
      tree_.Branch("dijet1_energy",    &dijet1_energy, "dijet1_energy/F");

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {
      
      jet0_pt  =  ev.jets_.at(0).pt();
      jet0_eta =  ev.jets_.at(0).eta();
      jet0_csv =  ev.jets_.at(0).CSV();

      dijet0_pt =  ev.dijets_.at(0).pt();
      dijet0_eta =  ev.dijets_.at(0).eta();
      dijet0_phi =  ev.dijets_.at(0).phi();
    //  dijet0_energy =  ev.dijets_.at(0).energy();

      dijet1_pt =  ev.dijets_.at(1).pt();
      dijet1_eta =  ev.dijets_.at(1).eta();
      dijet1_phi =  ev.dijets_.at(1).phi();
    //  dijet1_energy =  ev.dijets_.at(1).energy();

      tree_.Fill();

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
