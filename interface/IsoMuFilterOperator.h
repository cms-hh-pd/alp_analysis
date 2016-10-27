
#pragma once

#include <algorithm>

#include "BaseOperator.h"
#include "Event.h"

template <class EventClass> class IsoMuFilterOperator : public BaseOperator<EventClass> {

  public:

    double iso03_min_;
    double pt_max_;
    std::size_t min_number_;

    IsoMuFilterOperator( double iso03_min, double pt_max , std::size_t min_number ) :
    iso03_min_(iso03_min),
    pt_max_(pt_max),
    min_number_(min_number) {}
    virtual ~IsoMuFilterOperator() {}

    virtual bool process( EventClass & ev ) {

      //sanity check (due to lack of muon object)
      if(ev.muons_pt_.size() != ev.muons_pfiso03_.size()) {
        std::cout << "WARNING: different size between muons_pt and muons_pfiso03" << std::endl;
        return false;
      }    
      else {
        std::vector<float> pts;
        std::vector<float> isos;
        for(std::size_t i=0; i< ev.muons_pt_.size(); ++i){
          if ((ev.muons_pfiso03_[i] >= iso03_min_ ) && (ev.muons_pt_[i] <= pt_max_ )) {
            pts.push_back(ev.muons_pt_[i]);
            isos.push_back(ev.muons_pfiso03_[i]);
          }
        }
        ev.muons_pfiso03_ = isos;
        ev.muons_pt_ = pts;
      }

      //pass selection if at least min_number_ muons in region
      if (ev.muons_pt_.size() < min_number_) return false;
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "isomu_selection_min_"+std::to_string(min_number_);
      name+= "mu_pt<"+std::to_string(pt_max_);
      name+= "iso03>"+std::to_string(iso03_min_);
      return name;
    }

};
