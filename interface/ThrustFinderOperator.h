
#pragma once

#define _USE_MATH_DEFINES

#include <algorithm>

#include "Math/GenVector/VectorUtil.h"
#include "Math/Functor.h"
#include "Math/GSLMinimizer1D.h"

#include "BaseOperator.h"

// operator that finds the tranverse thrust axis
// of the jet of an event
template <class EventClass> class ThrustFinderOperator : public BaseOperator<EventClass> {

  public:

    std::size_t n_steps_phi_scan_;
    std::size_t fancyMinimizer_;

    ThrustFinderOperator(std::size_t n_steps_phi_scan = 361,
                     bool fancyMinimizer = false) : 
      n_steps_phi_scan_(n_steps_phi_scan),
      fancyMinimizer_(fancyMinimizer) {}
    virtual ~ThrustFinderOperator() {}

    virtual bool process( EventClass & ev ) {

      const auto & reco_jets = ev.jets_;

      // lambda to compute negative thrust for a given phi
      auto neg_thrust_f = [&reco_jets](double t_phi) {
        double neg_thrust = 0;
        for (auto & j : reco_jets ) {
          // deltaPhi wanted in [-PI,PI)
          neg_thrust -= j.p4_.Pt()*std::abs(
                        std::cos(ROOT::Math::VectorUtil::Phi_mpi_pi(j.p4_.Phi() - t_phi))
                        );
        }
        return neg_thrust;
      };


      // first need to get an initial value for phi with a simple scan
      double best_t_phi = 0;
      double min_neg_thrust = 0; // will be negative
      double phi_step = M_PI/(n_steps_phi_scan_-1);
      for (std::size_t i=0; i < n_steps_phi_scan_; i++ ) {
        double phi = i*phi_step;
        double neg_thrust = neg_thrust_f(phi);    
        if (neg_thrust < min_neg_thrust) {
          best_t_phi = phi;
          min_neg_thrust = neg_thrust;
        } 
      }

      if (fancyMinimizer_) {

        ROOT::Math::Functor1D neg_thrust_fc(neg_thrust_f); 

        ROOT::Math::GSLMinimizer1D minzr;
        // minization only around scan min
        minzr.SetFunction(neg_thrust_fc, best_t_phi,
                          best_t_phi - phi_step, best_t_phi + phi_step);
        // max number of f calls, abs tol or rel_tol
        minzr.Minimize(500,1e-5*M_PI, 0.);
      }


      // only get phi in [0,PI] (two minima in [-PI,PI])
      if (best_t_phi < 0.) {
        best_t_phi += M_PI;
      } else if (best_t_phi > M_PI) {
        best_t_phi -= M_PI;
      }

      ev.thrust_phi_ = best_t_phi;

      return true;
    }

};

