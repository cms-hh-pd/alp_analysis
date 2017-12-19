
#include "Analysis/alp_analysis/interface/Event.h"
#include "Analysis/alp_analysis/interface/Hemisphere.h"
#include "Analysis/alp_analysis/interface/ComposableSelector.h"
#include "Analysis/alp_analysis/interface/BaseOperator.h"
#include "Analysis/alp_analysis/interface/FolderOperator.h"
#include "Analysis/alp_analysis/interface/CounterOperator.h"
#include "Analysis/alp_analysis/interface/JEShifterOperator.h"
#include "Analysis/alp_analysis/interface/JERShifterOperator.h"
#include "Analysis/alp_analysis/interface/TriggerOperator.h"
#include "Analysis/alp_analysis/interface/JetFilterOperator.h"
#include "Analysis/alp_analysis/interface/IsoMuFilterOperator.h"
#include "Analysis/alp_analysis/interface/MetFilterOperator.h"
#include "Analysis/alp_analysis/interface/BTagFilterOperator.h"
#include "Analysis/alp_analysis/interface/JetPairingOperator.h"

#include "Analysis/alp_analysis/interface/MiscellPlotterOperator.h"
#include "Analysis/alp_analysis/interface/JetPlotterOperator.h"
#include "Analysis/alp_analysis/interface/GenJetPlotterOperator.h"
#include "Analysis/alp_analysis/interface/DiJetPlotterOperator.h"
#include "Analysis/alp_analysis/interface/EventWriterOperator.h"
#include "Analysis/alp_analysis/interface/TreeConverterOperator.h"
#include "Analysis/alp_analysis/interface/MCTruthOperator.h"
#include "Analysis/alp_analysis/interface/DiHiggsFilterOperator.h"

#include "Analysis/alp_analysis/interface/ThrustFinderOperator.h"
#include "Analysis/alp_analysis/interface/HemisphereProducerOperator.h"
#include "Analysis/alp_analysis/interface/HemisphereMixerOperator.h"
#include "Analysis/alp_analysis/interface/HemisphereWriterOperator.h"
#include "Analysis/alp_analysis/interface/MixedEventWriterOperator.h"

#include "Analysis/alp_analysis/interface/ClassifierOperator.h"
#include "Analysis/alp_analysis/interface/ReWeightingOperator.h"
#include "Analysis/alp_analysis/interface/WeightSumOperator.h"
#include "Analysis/alp_analysis/interface/Utils.h"


namespace {

  // templated struct to initialize all Event format dependent instances
  template < typename EventBase >
  struct instances {
    EventBase event_base; 
    ComposableSelector<EventBase> composable_selector; 
    BaseOperator<EventBase> base_operator; 
    FolderOperator<EventBase> folder_operator; 
    CounterOperator<EventBase> counter_operator; 
    TriggerOperator<EventBase> trigger_operator; 
    JEShifterOperator<EventBase> jes_shifter_operator;
    JERShifterOperator<EventBase> jer_shifter_operator;
    JetFilterOperator<EventBase> jet_filter_operator; 
    IsoMuFilterOperator<EventBase> isomu_filter_operator; 
    MetFilterOperator<EventBase> met_filter_operator; 
    BTagFilterOperator<EventBase> b_tag_filter_operator; 
    JetPairingOperator<EventBase> jet_pairing_operator; 
    SetJetPairingOperator<EventBase> set_jet_pairing_operator; 
    MiscellPlotterOperator<EventBase> miscell_plotter_operator; 
    JetPlotterOperator<EventBase> jet_plotter_operator; 
    GenJetPlotterOperator<EventBase> gen_jet_plotter_operator;
    DiJetPlotterOperator<EventBase> di_jet_plotter_operator; 
    EventWriterOperator<EventBase> event_writer_operator; 
    TreeConverterOperator<EventBase> tree_converter_operator; 
    MCTruthOperator<EventBase> mc_truth_operator; 
    DiHiggsFilterOperator<EventBase> dihigg_filter_operator; 
    ThrustFinderOperator<EventBase> thrust_finder_operator;
    HemisphereProducerOperator<EventBase> hemisphere_producer_operator;
    HemisphereMixerOperator<EventBase> hemisphere_mixer_operator;
    HemisphereWriterOperator<EventBase> hemisphere_writer_operator;
    MixedEventWriterOperator<EventBase> mixed_event_writer_operator;
    ReWeightingOperator<EventBase> reweighting_operator;
    WeightSumOperator<EventBase> weightsum_operator;
    ClassifierOperator<EventBase> classifier_operator;
  };

  struct event_formats {
    alp::Hemisphere alp_hemisphere;
    std::vector<alp::Hemisphere> vector_alp_hemisphere;
    instances<alp::Event> instances_alp_event;
    };

}
