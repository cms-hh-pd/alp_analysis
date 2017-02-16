#pragma once

#include "BaseOperator.h"
#include "Math/VectorUtil.h"

template <class EventClass> class MCTruthOperator : public BaseOperator<EventClass> {

  public:

     std::vector<int> matchId;
     double max_DeltaR_;
     bool HHMatchedOnly_;

     MCTruthOperator(double max_DeltaR = 0.5, bool HHMatchedOnly = false) :
      max_DeltaR_(max_DeltaR),
      HHMatchedOnly_(HHMatchedOnly) {}
    virtual ~MCTruthOperator() {}

    virtual bool process( EventClass & ev ) {

      //find gen jets per each ev.jets
      matchId.clear();
      int n_matched=0;
      double dR_min=99.;
      for (std::size_t j=0; j < ev.jets_.size(); j++) {
        matchId.push_back(-1);
        for (std::size_t g=0; g < ev.genbfromhs_.size(); g++) {
          double dR = ROOT::Math::VectorUtil::DeltaR( ev.jets_.at(j).p4_, ev.genbfromhs_.at(g).p4_);
          if ( dR < max_DeltaR_ && dR < dR_min) {
            matchId.at(j) = g;
            n_matched++;
            dR = dR_min;
          }
        }
      }
      for (std::size_t i=0; i < matchId.size(); i++){
        int id = matchId.at(i);
        for (std::size_t k=0; k < matchId.size(); k++){
//          std::cout << matchId.at(k) << std::endl;
//          if(id == matchId.at(k) && i!=k && matchId.at(k)>0) n_sameGenstd::cout<< "WARNING: same gen Jet for different reco jets" << std::endl;
        }
      }
//      std::cout << std::endl;
      if(HHMatchedOnly_ && n_matched<4) return false;               
      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "MCTruth";
      return name;
    }

};
