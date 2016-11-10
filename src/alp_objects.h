#pragma once

#include <vector>
#include <algorithm>
#include "Math/Vector4D.h"
#include "Math/Vector4Dfwd.h"

namespace alp {
  
  typedef ROOT::Math::PtEtaPhiEVector PtEtaPhiEVector;
  typedef std::pair<std::string, float> StringFloatPair;
  typedef std::vector<StringFloatPair> StringFloatPairVector;
  typedef std::pair<std::string, int> StringIntPair;
  typedef std::vector<StringIntPair> StringIntPairVector;
  typedef std::pair<std::string, int> StringBoolPair;
  typedef std::vector<StringIntPair> StringBoolPairVector;

  constexpr auto CSV_name = "pfCombinedInclusiveSecondaryVertexV2BJetTags";
  constexpr auto CMVA_name = "pfCombinedMVAV2BJetTags";

  class EventInfo {

    public:
 
      EventInfo() {}
      EventInfo(unsigned int event, unsigned int lumiBlock, unsigned int run) :
				event_(event),
    		lumiBlock_(lumiBlock),
    		run_(run) {}
 
      // copy constructor
      EventInfo( const EventInfo& rhs) :
        isMC_(rhs.isMC_),
        event_(rhs.event_),
        lumiBlock_(rhs.lumiBlock_),
        run_(rhs.run_),
        numPV_(rhs.numPV_),
        filterPairs_(rhs.filterPairs_),
        weightPairs_(rhs.weightPairs_) {}

      ~EventInfo() {}

      bool hasFilter(const std::string &name) const {
    		for( auto filterPair : filterPairs_)  {
      		if (filterPair.first == name) return true;
    		}
    		return false; 
  		}

      bool getFilter(const std::string &name) const {
    		for( auto filterPair : filterPairs_)  {
      		if (filterPair.first == name) return filterPair.second;
    		}
    		return false;
  		}

      bool getFilterC(const char * name) const { return getFilter(std::string(name)); }; 
      const StringBoolPairVector & getFilterPairs() const { return filterPairs_; } 
      void setFilterPairs(const StringBoolPairVector &filterPairs) { filterPairs_ = filterPairs; }

      bool hasWeight(const std::string &name) const {
				for( auto weightPair : weightPairs_)  {
      		if (weightPair.first == name) return true;
    		}
				return false;
			}

      float getWeight(const std::string &name) const { 
        for( auto weightPair : weightPairs_)  {
          if (weightPair.first == name) return weightPair.second;
        }
        return 1;
      }

      float getWeightC(const char * name) const { return getWeight(std::string(name)); }; 
      const StringFloatPairVector & getWeightPairs() const { return weightPairs_; } 
      void setWeightPairs(const StringFloatPairVector &weightPairs) { weightPairs_ = weightPairs; } 

      float eventWeight(const std::vector<std::string> & weights) {
        float eventWeight = 1.0;
        for (const auto & weightPair : weightPairs_ ) {
          if (std::find(weights.begin(), weights.end(), weightPair.first) != weights.end())
            eventWeight *= weightPair.second;
        }
        return eventWeight;
      }

      inline bool isMC() const { return isMC_; }
      inline void setIsMC(bool isMC) { isMC_ = isMC; }

      inline unsigned int getEvent() const { return event_; }
      inline void setEvent(unsigned int event) { event_ = event; }
      inline unsigned int getLumiBlock() const { return lumiBlock_; }
      inline void setLumiBlock(unsigned int lumiBlock) { lumiBlock_ = lumiBlock; }
      inline unsigned int getRun() const { return run_; }
      inline void setRun(int run) { run_ = run; }

      inline unsigned int getNumPV() const { return numPV_; }
      inline void setNumPV(unsigned int numPV) { numPV_ = numPV; }

   // attributes (also public)   

      bool isMC_ = true;

      unsigned int event_;
      unsigned int lumiBlock_;
      unsigned int run_; 

      unsigned int numPV_;

      // vector of generic event filters
      StringBoolPairVector filterPairs_;  
      // vector of pairs of weights 
      StringFloatPairVector weightPairs_;
      
	};

  class Candidate {

    public:

      // default constructor
      Candidate() :
        p4_() {}
      // copy constructor
      Candidate( const Candidate& rhs) : 
        p4_(rhs.p4_) {}
      // constructors from four vector
      Candidate( const PtEtaPhiEVector & p4) :
        p4_(p4) {}

      double pt() const {return p4_.Pt();}
      double eta() const {return p4_.Eta();}
      double phi() const {return p4_.Phi();}
      double energy() const {return p4_.E();}
      double et() const {return p4_.Et();}

      // attributes  (also public) 
      PtEtaPhiEVector p4_;
  };

  typedef std::vector<alp::Candidate> CandidateCollection;


  class Lepton  : public Candidate {
    
    public:
      // default constructor
      Lepton() : Candidate() {}
      // copy constructor
      Lepton( const Lepton & rhs) : 
        Candidate(rhs),
        iso03_(rhs.iso03_) {}

      // inherit other constructors
      using Candidate::Candidate;

      float iso03() const { return iso03_;} 

      // attributes (also public)
      float iso03_ = -99.;

  };

  typedef std::vector<alp::Lepton> LeptonCollection;

  class Jet : public Candidate {

    public:
      // default constructor
      Jet() : Candidate() {}
      // copy constructor
      Jet( const Jet & rhs) : 
        Candidate(rhs),
        partonFlavour_(rhs.partonFlavour_),
        hadronFlavour_(rhs.hadronFlavour_),
        ptRaw_(rhs.ptRaw_),
        JESunc_(rhs.JESunc_),
        puId_(rhs.puId_),
        mult_(rhs.mult_),
        chm_(rhs.chm_),
        chf_(rhs.chf_),
        nhf_(rhs.nhf_),
        muf_(rhs.muf_),
        discs_(rhs.discs_),
        ids_(rhs.ids_) {}

      // inherit other constructors
      using Candidate::Candidate;

      int id(const std::string & name ) const {
        for( auto id : ids_)  {
          if (id.first == name) return id.second;
        }
        return -777; 
      }

      int idC(const char * name ) const {
        return id(std::string(name));
      }

      float disc(const std::string & name ) const {
        for( auto disc : discs_)  {
          if (disc.first == name) return disc.second;
        }
        return -777.; 
      }

      float discC(const char * name ) const {
        return disc(std::string(name));
      }

      int partonFlavour() const {return partonFlavour_;};
      int hadronFlavour() const {return hadronFlavour_;};
      float CSV() const { return disc(CSV_name);}
      float CMVA() const { return disc(CMVA_name);}
      float ptRaw() const { return ptRaw_;};
      float JESunc() const { return JESunc_;};
      float puId() const { return puId_;};
      float mult() const { return mult_;};
      float chm() const { return chm_;};
      float chf() const { return chf_;};
      float nhf() const { return nhf_;};
      float muf() const { return muf_;};
     
    // attributes (also public)

      // flavour attributes (0 if data/undefined)
      int partonFlavour_ = 0;
      int hadronFlavour_ = 0;
      float ptRaw_ = 0;
      float JESunc_ = 0;
      float puId_ = 0;
      float mult_ = 0;
      float chm_ = 0;
      float chf_ = 0;
      float nhf_ = 0;
      float muf_ = 0;

      // to keep float discriminator values
      StringFloatPairVector discs_ = {};
      // to keep integer ids
      StringIntPairVector ids_ = {};

      std::vector<PtEtaPhiEVector> genJets_;
      std::vector<PtEtaPhiEVector> genPartons_;

  };

  typedef std::vector<alp::Jet> JetCollection;

}

