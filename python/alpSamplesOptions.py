#! /usr/bin/env python
# plotting options
#---------------------

sam_opt = {
    ########## Data ##########
   'SingleMuonRun2016B-v1' : {
        'sam_name'  : 'SingleMuonRun2016B-PromptReco-v1',
        'order'     : 0,
        'fillcolor' : 1, #kBlack
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'Data',
    },
   'SingleMuonRun2016B-v2' : {
        'sam_name'  : 'SingleMuonRun2016B-PromptReco-v2',
        'order'     : 0,
        'fillcolor' : 1,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'Data',
    },
   'SingleMuonRun2016C-v2' : {
        'sam_name'  : 'SingleMuonRun2016C-PromptReco-v2',
        'order'     : 0,
        'fillcolor' : 1,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'Data',
    },
   'SingleMuonRun2016D-v2' : {
        'sam_name'  : 'SingleMuonRun2016D-PromptReco-v2',
        'order'     : 0,
        'fillcolor' : 1,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'Data',
    },
   'BTagCSVRun2016B-v1' : {
        'sam_name'  : 'BTagCSVRun2016B-PromptReco-v1',
        'order'     : 0,
        'fillcolor' : 1,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'Data',
    },
   'BTagCSVRun2016B-v2' : {
        'sam_name'  : 'BTagCSVRun2016B-PromptReco-v2',
        'order'     : 0,
        'fillcolor' : 1,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'Data',
    },
   'BTagCSVRun2016C-v2' : {
        'sam_name'  : 'BTagCSVRun2016C-PromptReco-v2',
        'order'     : 0,
        'fillcolor' : 1,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'Data',
    },
   'BTagCSVRun2016D-v2' : {
        'sam_name'  : 'BTagCSVRun2016D-PromptReco-v2',
        'order'     : 0,
        'fillcolor' : 1,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'Data',
    },
    
    ########## MC ##########
    ### Signals
    'HHTo4B_SM' :{
        'sam_name': 'GluGluToHHTo4B_node_SM_13TeV-madgraph_reHLT-v1',
        'order'     : 2001,
        'fillcolor' : 632-4, #kRed
        'fillstyle' : 1,
        'linecolor' : 632-4,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'SM HH',
    },

    ### Backgrounds
    'TT' :{
        'sam_name': 'TT_TuneCUETP8M1_13TeV-powheg-pythia8_reHLT_ext3-v1',
        'order'     : 4,
        'fillcolor' : 4, #kBlue-2
        'fillstyle' : 1,
        'linecolor' : 4,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'tt',
    },

 # Background QCD
    'QCD_HT1000to1500' : {
        'sam_name': 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v2',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT1000to1500_ext' : {
        'sam_name': 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT1500to2000' : {
        'sam_name': 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v3',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT1500to2000_ext' : {
        'sam_name': 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT2000toInf' : {
        'sam_name': 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT2000toInf_ext' : {
        'sam_name': 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT200to300' : {
        'sam_name': 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT200to300_ext' : {
        'sam_name': 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT300to500' : {
        'sam_name': 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT300to500_ext' : {
        'sam_name': 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT500to700' : {
        'sam_name': 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT500to700_ext' : {
        'sam_name': 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT700to1000' : {
        'sam_name': 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },
    'QCD_HT700to1000_ext' : {
        'sam_name': 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'     : 5,
        'fillcolor' : 414, #kGreen-2
        'fillstyle' : 1,
        'linecolor' : 416,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'QCD',
    },

    ## for trigger studies
    'ST_s-channel_4f_lept' :{
        'sam_name'  : 'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_v0-v1',
        'order'     : 1001,
        'fillcolor' : 616-4,
        'fillstyle' : 1,
        'linecolor' : 616,
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'ST s-channel',
    },
    'ST_t-channel_4f_lept' :{
        'sam_name'  : 'ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_withHLT_ext1-v1',
         'order'    : 1002,
        'fillcolor' : 616-2, #kMagenta
        'fillstyle' : 1,
        'linecolor' : 616, #kMagenta
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'ST t-channel',
    },
  
    'WJetsToLNu_HT-100To200_ext' :{    
        'sam_name': 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-100To200' :{    
        'sam_name': 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-200To400' :{    
        'sam_name':'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-200To400_ext' :{    
        'sam_name':'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-400To600' :{    
        'sam_name':'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
          'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-400To600_ext' :{    
        'sam_name':'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-600To800' :{    
        'sam_name':'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-800To1200' :{    
        'sam_name':'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v2',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-800To1200_ext' :{    
        'sam_name':'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
         'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
   },
    'WJetsToLNu_HT-1200To2500' :{    
        'sam_name':'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-1200To2500_ext' :{    
        'sam_name':'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },
    'WJetsToLNu_HT-2500ToInf' :{    
        'sam_name':'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'order'    : 1003,
        'fillcolor' : 430, #kCyan-2
        'fillstyle' : 1,
        'linecolor' : 430, 
        'linewidth' : 2,
        'linestyle' : 1,
        'label'     : 'WJetsToLNu',
    },   

}
