
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
      double dist_ = -99.;
  
      Hemisphere() {}
      Hemisphere(double p_phi, bool d_phi_inv, double dist = -99. ) : 
        p_phi_(p_phi),
        d_phi_inv_(d_phi_inv),
        dist_(dist) {}      
    
      static double SumPz(const Hemisphere & hem) {
        double sumPz = 0.0;
        for (const auto & j : hem.jets_) {
          sumPz += j.p4_.Pz();
        }
        return sumPz;
      }
  
      static double ThrustMayor(const Hemisphere & hem) {
        double thrustMayor = 0.0;
        for (const auto & j : hem.jets_) {
          double d_phi = ROOT::Math::VectorUtil::Phi_mpi_pi(j.p4_.Phi()-M_PI/2.);
          thrustMayor += std::abs(j.p4_.Pt()* std::cos(d_phi));
        }
        return thrustMayor;
      }
  
      static double ThrustMinor(const Hemisphere & hem) {
        double thrustMinor = 0.0;
        for (const auto & j : hem.jets_) {
          double d_phi = ROOT::Math::VectorUtil::Phi_mpi_pi(j.p4_.Phi()-M_PI/2.);
          thrustMinor += std::abs(j.p4_.Pt()* std::sin(d_phi));
        }
        return thrustMinor;
      }
  
      static double InvMass(const Hemisphere & hem) {
        alp::PtEtaPhiEVector sum_v; // init null?
        for (const auto & j : hem.jets_) {
          sum_v += j.p4_;
        }
        return sum_v.M();
      }
  
      static int NJets(const Hemisphere & hem) {
        return int(hem.jets_.size());
      }
  
      static int NTags(const Hemisphere & hem,
                       std::string disc,
                       float wp) {
        int nTags = 0;
        for (const auto & j : hem.jets_) {
          if (j.disc(disc) > wp) nTags++;
        }
        return nTags;
      }

      double dist() const {
        return dist_;
      }  
  
      double sumPz() const {
        return SumPz(*this);
      }
  
      double thrustMayor() const {
        return ThrustMayor(*this);
      }
     
      double thrustMinor() const {
        return ThrustMinor(*this);
      }
  
      double invMass() const {
        return InvMass(*this);
      }
  
      int nJets() const {
        return NJets(*this);
      }

      //default values to call function directly in branches -- WARNING
      int nTags(std::string disc = "pfCombinedMVAV2BJetTags", float wp = 0.4432) const {
        return NTags(*this,disc,wp);
      }


      virtual ~Hemisphere() {}      
  
  };

}
