
#pragma once

#include <algorithm>
#include "Event.h"

// WARNING: it sorts event related variable - used by different operators
inline void order_jets_by_disc(std::vector<alp::Jet> & jets, std::string & disc) {
  // sort in discriminator order 
  auto comparator = [&](alp::Jet a, alp::Jet b){ 
    return a.disc(disc) > b.disc(disc); };
  std::sort(jets.begin(), jets.end(), comparator );
}

inline void get_sortIndex_jets(std::vector<std::size_t> & j_sort, std::vector<alp::Jet> & jets, std::string & disc) {
  // to get sorting indexes for current jets list
  j_sort = std::vector<std::size_t>(jets.size());
  std::iota(j_sort.begin(), j_sort.end(), 0);
  auto comparator = [&](std::size_t a, std::size_t b){ 
    return jets.at(a).disc(disc) > jets.at(b).disc(disc); };
  std::sort(j_sort.begin(), j_sort.end(), comparator ); 
}

inline float get_jets_ht(std::vector<alp::Jet> & jets) {
  // to compute HT from jets list
  float ht = 0;
  for(auto iter= jets.begin(); iter != jets.end(); iter++){
    ht += (*iter).pt();
  }
  return ht;
}

