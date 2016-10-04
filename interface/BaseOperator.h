
#pragma once
#include <TFile.h>

template <class EventClass> class BaseOperator {

  public:
    BaseOperator() {}
    virtual ~BaseOperator() {}
    
    virtual void init(TDirectory * tdir) { }

    virtual bool process( EventClass & ev ) {
      return true;
    }

    virtual bool output( TFile * tfile ) {
      return false;
    }   

    virtual bool output( std::ostream & os ) {
      return false;
    } 

    virtual std::string get_name() {
      // return empty string if unnamed
      return std::string{};
    }

};
