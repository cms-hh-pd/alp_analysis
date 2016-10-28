
#pragma once

#include <algorithm>
#include <math.h>

#include "Math/GenVector/VectorUtil.h"

#include "BaseOperator.h"
#include "Hemisphere.h"

template <class EventClass> class HemisphereWriterOperator : public BaseOperator<EventClass> {

  public:
 
    bool root_;
    std::string dir_;
    // pointer to event hemispheres
    std::vector<Hemisphere> * hems;

    TTree hem_tree_{"hem_tree","Hemisphere tree"};

     HemisphereWriterOperator(bool root = false, std::string dir = "") :
      root_(root),
      dir_(dir) {}
    virtual ~HemisphereWriterOperator() {}

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

      hem_tree_.Branch("hems","std::vector<Hemisphere>",
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
