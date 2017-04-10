#pragma once

#include "BaseOperator.h"

template <class EventClass> class FolderOperator : public BaseOperator<EventClass> {

  public:

    std::string folder_name_;

    FolderOperator(std::string folder_name) :
      folder_name_(folder_name) {}
    virtual ~FolderOperator() {}

    virtual std::string get_name() {
      auto name = std::string("folder_")+folder_name_;
      return name;
    }

    virtual bool output ( std::ostream & os ) {    
      os << "--- " << folder_name_ << std::endl;
      return true;
    }

};
