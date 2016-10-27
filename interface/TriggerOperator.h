#pragma once

#include "BaseOperator.h"

template <class EventClass> class TriggerOperator : public BaseOperator<EventClass> {

  public:

    std::vector<std::string> or_paths_; 

    TriggerOperator(std::vector<std::string> or_paths) :
      or_paths_(or_paths) {}
    virtual ~TriggerOperator() {}

    virtual bool process( EventClass & ev ) {
      for (const auto & or_path : or_paths_) {
        if (ev.eventInfo_.getFilter(or_path)) return true;
      }
      return false;
    }

    virtual std::string get_name() {
      auto name = std::string{};
      name+= "trigger";
      for (const auto & or_path : or_paths_) name+="_OR"+or_path; 
      return name;
    }

};
