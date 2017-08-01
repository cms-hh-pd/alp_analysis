
#pragma once

#include <algorithm>
#include <math.h>

#include "Math/GenVector/VectorUtil.h"

#include "BaseOperator.h"
#include "Hemisphere.h"

template <class EventClass> class HemisphereProducerOperator : public BaseOperator<EventClass> {

  public:

    HemisphereProducerOperator() {}
    virtual ~HemisphereProducerOperator() {}

    virtual bool process( EventClass & ev ) {

      // get thrust phi
      const auto & t_phi = ev.thrust_phi_;
      auto p_phi = t_phi-M_PI/2.;
     
      // clear old vector and add two hemispheres
      auto & hems = ev.hems_;
      hems.clear();
      hems.emplace_back(p_phi, false);
      hems.emplace_back(p_phi, true);

      // loop over all jets and push to hemispheres
      for (std::size_t i = 0; i < ev.jets_.size(); i++ ) {     
        const auto & jet = ev.jets_.at(i);
        auto d_phi = ROOT::Math::VectorUtil::Phi_mpi_pi(jet.p4_.Phi() - p_phi);
        // fill and rotate (swap phi if negative)
        if (d_phi < 0) {  
          hems.at(1).jets_.emplace_back(jet);   
          hems.at(1).jets_.back().p4_.SetPhi(-d_phi);
        } else {
          hems.at(0).jets_.emplace_back(jet);   
          hems.at(0).jets_.back().p4_.SetPhi(d_phi);
        }
      }
      
      // invert eta if sumPz < 0 (symmetry)
      for (auto & hem : hems) {
        if (hem.sumPz() < 0) {
          hem.sumPz_inv_ = true; // so can be reverted 
          for (auto & j : hem.jets_) {
            j.p4_.SetEta(-j.p4_.Eta());
          }
        }
      }

      return true;
    }

};
