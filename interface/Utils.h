
#pragma once

#include <algorithm>
#include "Event.h"

inline void order_jets_by_disc(std::vector<alp::Jet> & jets, std::string & disc) {
      // sort in discriminator order 
      auto comparator = [&](alp::Jet a, alp::Jet b){ 
        return a.disc(disc) > b.disc(disc); };
      std::sort(jets.begin(), jets.end(), comparator );
}
