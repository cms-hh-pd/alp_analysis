
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
    float * jet0_pt_ptr = nullptr;
//    std::vector<float> * jet0_pt_ptr = nullptr;

    std::vector<std::string> weights_;

    TTree tree_{"tree","Tree using  dataformats"};

    json config_ = {};

    TreeConverterOperator(const std::vector<std::string> & weights = {}) :
      weights_(weights) {}

    virtual ~TreeConverterOperator() {}

    virtual void init(TDirectory * tdir) {

      tree_.Branch("jet0_pt", "float", &jet0_pt_ptr, 64000, 2);

      tree_.SetDirectory(tdir);
      tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {
      
      jet0_pt_ptr =  dynamic_cast<float *> ( & ev.jets_.at(0).pt() );


      tree_.Fill();

      return true;
    }

    virtual bool output( TFile * tfile) {


      return true;

    }

};
