
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
    std::size_t n_h_mix_;
    std::size_t n_h_skip_;

    // to order jets after mixing
    std::string disc_ = "pfCombinedInclusiveSecondaryVertexV2BJetTags";
    std::size_t n_fix_jets_ = 4;

    bool root_;
    std::string dir_;


    TTree tree_{"mix_tree","Tree wth mixed events"};

     MixedEventWriterOperator(std::size_t n_h_mix = 1, std::size_t n_h_skip = 1) :
      mix_jets_ptr_(&mix_jets_),  
      n_h_mix_(n_h_mix),
      n_h_skip_(n_h_skip) {}

    virtual ~MixedEventWriterOperator() {}

    virtual void init(TDirectory * tdir) {

      tree_.Branch("Jets","std::vector<alp::Jet>",
                   &mix_jets_ptr_, 64000, 1);


      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {


      const auto & bm_hems = ev.best_match_hems_;

      // for each hemisphere i
      for (std::size_t h_i=n_h_skip_; h_i<(n_h_skip_+n_h_mix_); h_i++) {
        // for each hemisphere j
        for (std::size_t h_j=n_h_skip_; h_j<(n_h_skip_+n_h_mix_); h_j++) {

          // clear jet collection
          mix_jets_.clear();

          // references for easy access
          const auto jets_i = bm_hems.at(0).at(h_i).jets_;
          const auto jets_j = bm_hems.at(1).at(h_j).jets_;
          mix_jets_.insert(mix_jets_.end(), jets_i.begin(), jets_i.end());
          mix_jets_.insert(mix_jets_.end(), jets_j.begin(), jets_j.end());


          // order by b-tagging disc
          order_jets_by_disc(mix_jets_, disc_);
          // pair with min mass
          dijet_pairing_simple(mix_jets_, n_fix_jets_);        

          // fill tree with combination
          tree_.Fill();
        }
      }



      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
