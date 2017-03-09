#pragma once

#include "BaseOperator.h"

template <class EventClass> class DiHiggsFilterOperator : public BaseOperator<EventClass> {

  public:

    bool do_blind_;
    std::vector<double> c_dijets_mass_; 

    DiHiggsFilterOperator(const std::vector<double> & c_dijets_mass = {}, bool do_blind = false):
      do_blind_(do_blind),
      c_dijets_mass_(c_dijets_mass) {}
    virtual ~DiHiggsFilterOperator() {}

    virtual bool process( EventClass & ev ) {

     // to get only event out from 'triangle'
      if(do_blind_) {
        for (const auto & dijet : ev.dijets_) {
          if (std::abs(dijet.mass() - 120.) < 40.) return false;
        }
      }
      
      if(c_dijets_mass_.size()==4) {
        if( (ev.dijets_.at(0).mass()< c_dijets_mass_.at(0) || ev.dijets_.at(0).mass()> c_dijets_mass_.at(1)) &&
            (ev.dijets_.at(1).mass()< c_dijets_mass_.at(2) || ev.dijets_.at(1).mass()> c_dijets_mass_.at(3))  ){
           return false;
        }
      }
      else return false; //DEBUG

      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "blind";
      return name;
    }

};
