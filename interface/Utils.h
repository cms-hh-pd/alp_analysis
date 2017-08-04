
#pragma once

#include <algorithm>
#include "Event.h"
#include "Hemisphere.h"

#include "TLorentzVector.h"
#include "Math/VectorUtil.h"

// WARNING: it sorts event related variable - used by different operators
inline void order_jets_by_disc(std::vector<alp::Jet> & jets, std::string & disc) {
  auto compare_disc = [&](alp::Jet a, alp::Jet b){
      return a.disc(disc) > b.disc(disc); };

  auto compare_pt = [&](alp::Jet a, alp::Jet b){
      return a.pt() > b.pt(); };

  //sort in discriminator order 
  if(disc == "pt")  std::sort(jets.begin(), jets.end(), compare_pt );
  else std::sort(jets.begin(), jets.end(), compare_disc );
}      

inline void get_sortIndex_jets(std::vector<std::size_t> & j_sort, std::vector<alp::Jet> & jets, std::string & disc) {
  // to get sorting indexes for current jets list
  j_sort = std::vector<std::size_t>(jets.size());
  std::iota(j_sort.begin(), j_sort.end(), 0);

  auto comp_disc = [&](std::size_t a, std::size_t b){ 
    return jets.at(a).disc(disc) > jets.at(b).disc(disc); };

  auto comp_pt = [&](std::size_t a, std::size_t b){   
      return jets.at(a).pt() > jets.at(b).pt(); };

  // sort in discriminator order 
  if(disc == "pt")  std::sort(j_sort.begin(), j_sort.end(), comp_pt );
  else std::sort(j_sort.begin(), j_sort.end(), comp_disc ); 
}

inline float get_jets_ht(std::vector<alp::Jet> & jets) {
  // to compute HT from jets list
  float ht = 0;
  for(auto iter= jets.begin(); iter != jets.end(); iter++){
    ht += (*iter).pt();
  }
  return ht;
}

inline float get_dj_dPhiabs(alp::Jet & jet0, alp::Jet & jet1) {
  // to compute abs deltaPhi of Jets
  return (M_PI - std::abs(std::abs(jet0.phi() - jet1.phi()) - M_PI));
}

inline float get_ddj_dPhiabs(alp::PtEtaPhiEVector & dijet0, alp::PtEtaPhiEVector & dijet1) {
  // to compute abs deltaPhi of diJets
  return (M_PI - std::abs(std::abs(dijet0.phi() - dijet1.phi()) - M_PI));
}

float get_absCosThetaStar(alp::PtEtaPhiEVector j, alp::PtEtaPhiEVector j_RF){     
  // to get star angle computation    
  alp::PtEtaPhiEVector boosted_dj =  ROOT::Math::VectorUtil::boost(j, j_RF.BoostToCM()); //minus already in the function
  return std::abs(std::cos(boosted_dj.theta()));
}

