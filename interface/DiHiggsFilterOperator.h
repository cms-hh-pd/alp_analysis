#pragma once

#include "BaseOperator.h"

template <class EventClass> class DiHiggsFilterOperator : public BaseOperator<EventClass> {

  public:

    bool do_blind_;
    double min_dihiggs_mass_; 

    DiHiggsFilterOperator(bool do_blind = false, double min_dihiggs_mass = 0.):
      do_blind_(do_blind),
      min_dihiggs_mass_(min_dihiggs_mass) {}
    virtual ~DiHiggsFilterOperator() {}

    virtual bool process( EventClass & ev ) {

     // to get only event out from 'triangle'
      if(do_blind_) {
        for (const auto & dijet : ev.dijets_) {
          if (std::abs(dijet.mass() - 120.) < 40.) return false;
        }
      }
      
      if(min_dihiggs_mass_) {
        if((ev.dijets_.at(0)+ev.dijets_.at(1)).mass()< min_dihiggs_mass_) return false;
      }

      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "blind";
      return name;
    }

};
