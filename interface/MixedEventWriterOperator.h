
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"
#include "BTagFilterOperator.h"
#include "JetPairingOperator.h"

#include "Event.h"


template <class EventClass> class MixedEventWriterOperator : public BaseOperator<EventClass> {

  public:
 
    // variables to save in branches
    std::vector<alp::Jet> mix_jets_;
    // a pointer to avoid undeclared label
    std::vector<alp::Jet> * mix_jets_ptr_;

    // hemisphere combinations to save
    std::vector<std::vector<std::size_t>> combs_; 

    TTree tree_{"mix_tree","Tree wth mixed events"};

     MixedEventWriterOperator(std::vector<std::vector<std::size_t>> combs = {{1,1}}) :
      mix_jets_ptr_(&mix_jets_),  
      combs_(combs) {}

    virtual ~MixedEventWriterOperator() {}

    virtual void init(TDirectory * tdir) {

      tree_.Branch("Jets","std::vector<alp::Jet>",
                   &mix_jets_ptr_, 64000, 1);

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {


      const auto & bm_hems = ev.best_match_hems_;

      for (const auto & comb : combs_) {

        auto h_i = comb.at(0); 
        auto h_j = comb.at(1); 

        // clear jet collection
        mix_jets_.clear();

        // references for easy access
        const auto jets_i = bm_hems.at(0).at(h_i).jets_;
        const auto jets_j = bm_hems.at(1).at(h_j).jets_;
        mix_jets_.insert(mix_jets_.end(), jets_i.begin(), jets_i.end());
        mix_jets_.insert(mix_jets_.end(), jets_j.begin(), jets_j.end());

        // fill tree with combination
        tree_.Fill();
      }

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
