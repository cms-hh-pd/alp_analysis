
#pragma once

#define _USE_MATH_DEFINES

#include "Analysis/alp_analysis/interface/Event.h"
#include "Analysis/alp_analysis/interface/Utils.h"

#include "Math/GenVector/VectorUtil.h"

namespace alp { 
  class Hemisphere { 
    public:
  
      std::vector<alp::Jet> jets_;
  
      double p_phi_ = 0.;
      bool sumPz_inv_ = false;
      bool d_phi_inv_ = false;
      double dist_ = -99.;
      static constexpr const char* disc_ = "pfCombinedMVAV2BJetTags";; 
      static constexpr float disc_wp_  = 0.4432;
  
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

      static double MinPtBtag(const Hemisphere & hem,
                           std::string disc,
                           float wp) {
        double minPtBtag = 999.0; //debug
        for (const auto & j : hem.jets_) {
          if (j.disc(disc) > wp){
            double pt = j.p4_.Pt();
            if(pt < minPtBtag) minPtBtag = pt;
          }
        }
        return minPtBtag;
      }

      static double PtNBtag(const Hemisphere & hem,
                           std::string disc, float wp,
                           unsigned int nBtag) {
        double pt = 0.;
        std::vector<alp::Jet> tjets = hem.jets_;
        if(tjets.size()>nBtag){
          auto iter = remove_if(tjets.begin(),tjets.end(),  
               [&] (const alp::Jet & jet) {
               return jet.disc(disc)>=wp; });
          tjets.erase(iter, tjets.end());

          if(tjets.size()>nBtag) {
            order_jets_by_disc(tjets, disc);
            pt = tjets.at(nBtag).p4_.Pt();
          }
        }
        return pt;
      }

      static double Pt1Btag(const Hemisphere & hem,
                           std::string disc, float wp) {
        return PtNBtag(hem,disc,wp,0);
      }

      static double Pt2Btag(const Hemisphere & hem,
                           std::string disc, float wp) {
        return PtNBtag(hem,disc,wp,1);
      }

      static double Pt3Btag(const Hemisphere & hem,
                           std::string disc, float wp) {
        return PtNBtag(hem,disc,wp,2);
      }

      static double Pt4Btag(const Hemisphere & hem,
                           std::string disc, float wp) {
        return PtNBtag(hem,disc,wp,3);
      }

      static double PtMaxBtag(const Hemisphere & hem,
                           std::string disc) {
        double maxBtag = 0.;
        double pt = 0.;
        for (const auto & j : hem.jets_) {
          if (j.disc(disc) > maxBtag){
            pt = j.p4_.Pt();
            maxBtag = j.disc(disc);
          }
        }
        return pt;
      }

      static double HtBtag(const Hemisphere & hem,
                           std::string disc,
                           float wp) {
        double ht = 0.;
        for (const auto & j : hem.jets_) {
          if (j.disc(disc) > wp){
            ht += j.p4_.Pt();
          }
        }
        return ht;
      }

      static double Ht(const Hemisphere & hem) {
        double ht = 0.;
        for (const auto & j : hem.jets_) {
            ht += j.p4_.Pt();
        }
        return ht;
      }

      // functions to call on branches
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
      int nTags(std::string disc = disc_, float wp = disc_wp_) const {
        return NTags(*this,disc,wp);
      }

      double minPtBtag(std::string disc = disc_, float wp = disc_wp_) const {
        return MinPtBtag(*this,disc,wp);
      }

      double ptMaxBtag(std::string disc = disc_) const {
        return PtMaxBtag(*this,disc);
      }

      double htBtag(std::string disc = disc_, float wp = disc_wp_) const {
        return HtBtag(*this,disc,wp);
      }

      double ht() const {
        return Ht(*this);
      }

      double pt1Btag(std::string disc = disc_, float wp = disc_wp_) const {
        return Pt1Btag(*this,disc,wp);
      }

      double pt2Btag(std::string disc = disc_, float wp = disc_wp_) const {
        return Pt2Btag(*this,disc,wp);
      }

      double pt3Btag(std::string disc = disc_, float wp = disc_wp_) const {
        return Pt3Btag(*this,disc,wp);
      }

      double pt4Btag(std::string disc = disc_, float wp = disc_wp_) const {
        return Pt4Btag(*this,disc,wp);
      }

      virtual ~Hemisphere() {}      
  
  };

}
