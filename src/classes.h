
#include "Analysis/alp_analysis/interface/Event.h"
#include "Analysis/alp_analysis/interface/ComposableSelector.h"
#include "Analysis/alp_analysis/interface/BaseOperator.h"
#include "Analysis/alp_analysis/interface/CounterOperator.h"
#include "Analysis/alp_analysis/interface/TriggerOperator.h"
#include "Analysis/alp_analysis/interface/JetFilterOperator.h"
#include "Analysis/alp_analysis/interface/IsoMuFilterOperator.h"
#include "Analysis/alp_analysis/interface/MetFilterOperator.h"
#include "Analysis/alp_analysis/interface/BTagFilterOperator.h"
#include "Analysis/alp_analysis/interface/JetPairingOperator.h"

#include "Analysis/alp_analysis/interface/JetPlotterOperator.h"
#include "Analysis/alp_analysis/interface/DiJetPlotterOperator.h"
#include "Analysis/alp_analysis/interface/EventWriterOperator.h"


namespace {

  // templated struct to initialize all Event format dependent instances
  template < typename EventBase >
  struct instances {
    EventBase event_base; 
    ComposableSelector<EventBase> composable_selector; 
    BaseOperator<EventBase> base_operator; 
    CounterOperator<EventBase> counter_operator; 
    TriggerOperator<EventBase> trigger_operator; 
    JetFilterOperator<EventBase> jet_filter_operator; 
    IsoMuFilterOperator<EventBase> isomu_filter_operator; 
    MetFilterOperator<EventBase> met_filter_operator; 
    BTagFilterOperator<EventBase> b_tag_filter_operator; 
    JetPairingOperator<EventBase> jet_pairing_operator; 
    SetJetPairingOperator<EventBase> set_jet_pairing_operator; 
    JetPlotterOperator<EventBase> jet_plotter_operator; 
    DiJetPlotterOperator<EventBase> di_jet_plotter_operator; 
    EventWriterOperator<EventBase> event_writer_operator; 
  };

  struct event_formats {
    instances<alp::Event> instances_alp_event;
    };

}
