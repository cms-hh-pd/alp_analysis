#pragma once

#include "BaseOperator.h"

template <class EventClass> class ClassifierOperator : public BaseOperator<EventClass> {

  public:

    float_t clfmin_;
    float_t clfmax_;

    ClassifierOperator(float_t clfmin, float_t clfmax) :
    clfmin_(clfmin),
    clfmax_(clfmax) {}
    virtual ~ClassifierOperator() {}

    virtual bool process( EventClass & ev ) {
      if (ev.classifier_ >= clfmin_ && ev.classifier_ < clfmax_ ) return true;
      return false;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "clf";
      return name;
    }

};
