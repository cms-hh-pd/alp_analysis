
#pragma once

#define _USE_MATH_DEFINES

#include "Analysis/alp_analysis/interface/Event.h"

#include "Math/GenVector/VectorUtil.h"

namespace alp { 
  class Hemisphere { 
    public:
  
      std::vector<alp::Jet> jets_;
  
      double p_phi_ = 0.;
      bool sumPz_inv_ = false;
      bool d_phi_inv_ = false;
  
      Hemisphere() {}
      Hemisphere(double p_phi, bool d_phi_inv ) : 
        p_phi_(p_phi),
        d_phi_inv_(d_phi_inv) {}
  
      virtual ~Hemisphere() {}                   
  
  
      static double sumPz(const Hemisphere & hem) {
        double sumPz = 0.0;
        for (const auto & j : hem.jets_) {
          sumPz += j.p4_.Pz();
        }
        return sumPz;
      }
  
      static double thrustMayor(const Hemisphere & hem) {
        double thrustMayor = 0.0;
        for (const auto & j : hem.jets_) {
          double d_phi = ROOT::Math::VectorUtil::Phi_mpi_pi(j.p4_.Phi()-M_PI/2.);
          thrustMayor += std::abs(j.p4_.Pt()* std::cos(d_phi));
        }
        return thrustMayor;
      }
  
      static double thrustMinor(const Hemisphere & hem) {
        double thrustMinor = 0.0;
        for (const auto & j : hem.jets_) {
          double d_phi = ROOT::Math::VectorUtil::Phi_mpi_pi(j.p4_.Phi()-M_PI/2.);
          thrustMinor += std::abs(j.p4_.Pt()* std::sin(d_phi));
        }
        return thrustMinor;
      }
  
      static double invMass(const Hemisphere & hem) {
        alp::PtEtaPhiEVector sum_v; // init null?
        for (const auto & j : hem.jets_) {
          sum_v += j.p4_;
        }
        return sum_v.M();
      }
  
      static int nJets(const Hemisphere & hem) {
        return int(hem.jets_.size());
      }
  
      static int nTags(const Hemisphere & hem,
                       std::string disc = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
                       float wp = 0.8) {
        int nTags = 0;
        for (const auto & j : hem.jets_) {
          if (j.disc(disc) > wp) nTags++;
        }
        return nTags;
      }
  
  
      double getSumPz() {
        return sumPz(*this);
      }
  
      double getThrustMayor() {
        return thrustMayor(*this);
      }
     
      double getThrustMinor() {
        return thrustMinor(*this);
      }
  
      double getInvMass() {
        return invMass(*this);
      }
  
      int getNJets() {
        return nJets(*this);
      }
  
      int getNTags(std::string disc = "pfCombinedInclusiveSecondaryVertexV2BJetTags", float wp = 0.8) {
        return nTags(*this,disc,wp);
      }
  
  };

}
