
#pragma once

#include <algorithm>
#include <math.h>

#include "Math/GenVector/VectorUtil.h"

#include "BaseOperator.h"
#include "Hemisphere.h"

template <class EventClass> class HemisphereWriterOperator : public BaseOperator<EventClass> {

  public:
 
    // pointer to event hemispheres
    std::vector<alp::Hemisphere> * hems;

    TTree hem_tree_{"hem_tree","Hemisphere tree"};

     HemisphereWriterOperator() {}
    virtual ~HemisphereWriterOperator() {}

    virtual void init(TDirectory * tdir) {

      hem_tree_.Branch("hems","std::vector<alp::Hemisphere>",
                        &hems, 64000, 1);
      hem_tree_.SetDirectory(tdir);
      hem_tree_.AutoSave();

   }


    virtual bool process( EventClass & ev ) {

      hems = &ev.hems_;
      hem_tree_.Fill();

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
