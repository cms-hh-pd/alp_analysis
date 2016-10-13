#! /usr/bin/env python
# 'xsec' is xs*br
#---------------------

samples = {
    ########## Data ##########
   'SingleMuonRun2016B-v1' : {
        'sam_name': 'SingleMuonRun2016B-PromptReco-v1',
        'nevents' : 2816842,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
   'SingleMuonRun2016B-v2' : {
        'sam_name': 'SingleMuonRun2016B-PromptReco-v2',
        'nevents' : 93833758,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
   'SingleMuonRun2016C-v2' : {
        'sam_name': 'SingleMuonRun2016C-PromptReco-v2',
        'nevents' : 68492270,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
   'SingleMuonRun2016D-v2' : {
        'sam_name': 'SingleMuonRun2016D-PromptReco-v2',
        'nevents' : 98175265,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },

   'BTagCSVRun2016B-v1' : {
        'sam_name': 'BTagCSVRun2016B-PromptReco-v1',
        'nevents' : 1973077, #FIXME
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
   'BTagCSVRun2016B-v2' : {
        'sam_name': 'BTagCSVRun2016B-PromptReco-v2',
        'nevents' : 77545653, #FIXME
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
   'BTagCSVRun2016C-v2' : {
        'sam_name': 'BTagCSVRun2016C-PromptReco-v2',
        'nevents' : 31253722, #FIXME
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
   'BTagCSVRun2016D-v2' : {
        'sam_name': 'BTagCSVRun2016D-PromptReco-v2',
        'nevents' : 56725352, #FIXME
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    

    ########## MC ##########
    ### Signals
    'HHTo4B_SM' :{
        'sam_name': 'GluGluToHHTo4B_node_SM_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 0.03345*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM2' :{
        'sam_name': 'GluGluToHHTo4B_node_2_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM3' :{
        'sam_name': 'GluGluToHHTo4B_node_3_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM4' :{
    'sam_name': 'GluGluToHHTo4B_node_4_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM5' :{
        'sam_name': 'GluGluToHHTo4B_node_5_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM6' :{
        'sam_name': 'GluGluToHHTo4B_node_6_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM7' :{
        'sam_name': 'GluGluToHHTo4B_node_7_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM8' :{
        'sam_name': 'GluGluToHHTo4B_node_8_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM9' :{
        'sam_name': 'GluGluToHHTo4B_node_9_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM10' :{
        'sam_name': 'GluGluToHHTo4B_node_10_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM11' :{
        'sam_name': 'GluGluToHHTo4B_node_11_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM12' :{
        'sam_name': 'GluGluToHHTo4B_node_12_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'HHTo4B_BM13' :{
        'sam_name': 'GluGluToHHTo4B_node_13_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },    
    'HHTo4B_BMbox' :{
        'sam_name': 'GluGluToHHTo4B_node_box_13TeV-madgraph_v14-v1',
        'nevents' : 300000,
        'xsec_br' : 1.*0.577*0.577,
        'matcheff': 1.,
        'kfactor' : 1.,
    },

    ### Backgrounds
    # Background QCD
    'QCD_HT1000to1500' :{
        'sam_name': 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v2',
        'nevents' : 4980387,
        'xsec_br' : 1207.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT1000to1500_ext' :{
        'sam_name': 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 10335975,
        'xsec_br' : 1207.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT1500to2000' :{
        'sam_name': 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v3',
        'nevents' : 3846616,
        'xsec_br' : 119.9,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT1500to2000_ext' :{
        'sam_name': 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 7803965,
        'xsec_br' : 119.9,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT2000toInf' :{
        'sam_name': 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 1960245,
        'xsec_br' : 25.24,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT2000toInf_ext' :{
        'sam_name': 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 4047532,
        'xsec_br' : 25.24,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT200to300' :{
        'sam_name': 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 18523829,
        'xsec_br' : 1712000.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT200to300_ext' :{
        'sam_name': 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 38812676,
        'xsec_br' : 1712000.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT300to500' :{
        'sam_name': 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 16830696,
        'xsec_br' : 347700.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT300to500_ext' :{
        'sam_name': 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 37875602,
        'xsec_br' : 347700.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT500to700' :{
        'sam_name': 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 19199088,
        'xsec_br' : 32100.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT500to700_ext' :{
        'sam_name': 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 44138665,
        'xsec_br' : 32100.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT700to1000' :{
        'sam_name': 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 15621634,
        'xsec_br' : 6831.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT700to1000_ext' :{
        'sam_name': 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 29832311,
        'xsec_br' : 6831.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },   
    
    # Background QCD bEnriched FIXME  xsec
    'QCD_bEnriched_HT1000to1500' :{
        'sam_name': 'QCD_bEnriched_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 221429,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_bEnriched_HT100to200' :{
        'sam_name': 'QCD_bEnriched_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 5341805,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_bEnriched_HT1500to2000' :{
        'sam_name': 'QCD_bEnriched_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 50978,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_bEnriched_HT2000toInf' :{
        'sam_name': 'QCD_bEnriched_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 23671,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_bEnriched_HT200to300' :{
        'sam_name': 'QCD_bEnriched_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 4735212,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_bEnriched_HT300to500' :{
        'sam_name': 'QCD_bEnriched_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 2871164,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_bEnriched_HT500to700' :{
        'sam_name': 'QCD_bEnriched_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 2426857,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_bEnriched_HT700to1000' :{
        'sam_name': 'QCD_bEnriched_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 877400,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },

    # Background QCD BGenFilter FIXME  xsec*br
    'QCD_HT1000to1500_BGenFilter' :{
        'sam_name': 'QCD_HT1000to1500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 830868,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT100to200_BGenFilter' :{
        'sam_name': 'QCD_HT100to200_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 7819821,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT1500to2000_BGenFilter' :{
        'sam_name': 'QCD_HT1500to2000_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 240962,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT2000toInf_BGenFilter' :{
        'sam_name': 'QCD_HT2000toInf_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 136826,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT200to300_BGenFilter' :{
        'sam_name': 'QCD_HT200to300_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 8251443,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT300to500_BGenFilter' :{
        'sam_name': 'QCD_HT300to500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 5772931,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT500to700_BGenFilter' :{
        'sam_name': 'QCD_HT500to700_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 7083503,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'QCD_HT700to1000_BGenFilter' :{
        'sam_name': 'QCD_HT700to1000_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 2893038,
        'xsec_br' : 1.,
        'matcheff': 1.,
        'kfactor' : 1.,
    },

    'TT' :{
        'sam_name': 'TT_TuneCUETP8M1_13TeV-powheg-pythia8_v14_ext3-v1',
        'nevents' : 92925926,
        'xsec_br' : 831.76, #*(6./9.)*(6./9.) FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'ttHTobb' :{
        'sam_name': 'ttHTobb_M125_13TeV_powheg_pythia8_v14-v1',
        'nevents' : 3912212.,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'TTZToQQ' :{
        'sam_name': 'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v0-v1',
        'nevents' : 749400.,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'TTWJetsToQQ' :{
        'sam_name': 'TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_v0-v1',
        'nevents' : 833298.,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'TTTT' :{
        'sam_name': 'TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8_v0_ext1-v1',
        'nevents' : 989025.,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'ttbb' :{
        'sam_name': 'ttbb_4FS_ckm_amcatnlo_madspin_pythia8_v0_ext1-v1',
        'nevents' : 3955742.,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    
    'ST_tW_antitop_5f_incl' :{
        'sam_name': 'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v0-v1',
        'nevents' : 985000.,
        'xsec_br' : 38.09,
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'ST_tW_top_5f_incl' :{
        'sam_name': 'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_v0-v2',
        'nevents' : 998400.,
        'xsec_br' : 38.09,
        'matcheff': 1.,
        'kfactor' : 1.,
    },

    'ZH_HToBB_ZToQQ' :{
        'sam_name': 'ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8_v14-v1',
        'nevents' : 493590,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'WZ' :{
        'sam_name': 'WZ_TuneCUETP8M1_13TeV-pythia8_v0-v1',
        'nevents' : 1000000.,
        'xsec_br' : 47.2,#cerca
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'ZZTo4Q' :{
        'sam_name': 'ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8_v0-v1',
        'nevents' : 29948451.,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'WJetsToQQ_HT-600ToInf' :{    
        'sam_name': 'WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 1025005,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'ZJetsToQQ_HT-600ToInf' :{
        'sam_name': 'ZJetsToQQ_HT600toInf_13TeV-madgraph_v14-v1',
        'nevents' : 992590.,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'DYJetsToQQ_HT180' :{
        'sam_name': 'DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 12052369,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },   

    'VBFHToBB' :{
        'sam_name': 'VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix_v14-v1',
        'nevents' : 931614,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'VBFHToBB_ext' :{
        'sam_name': 'VBFHToBB_M-125_13TeV_powheg_pythia8_weightfix_v14_ext1-v1',
        'nevents' : 3645385,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'GluGluHToBB' :{
        'sam_name': 'GluGluHToBB_M125_13TeV_powheg_pythia8_v14-v1',
        'nevents' : 4825748,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'GluGluHToBB_ext' :{
        'sam_name': 'GluGluHToBB_M125_13TeV_powheg_pythia8_v14_ext1-v1',
        'nevents' : 4867387,
        'xsec_br' : 1., #FIXME
        'matcheff': 1.,
        'kfactor' : 1.,
    },        

    ## for trigger studies
    'ST_s-channel_4f_lept' :{
        'sam_name': 'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_v0-v1',
        'nevents' : 1000000.,
        'xsec_br' : 10.32, #10.11
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'ST_t-channel_4f_lept' :{
        'sam_name': 'ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_v14_ext1-v1',
        'nevents' : 19835374.,
        'xsec_br' : 216.99, #70.69
        'matcheff': 1.,
        'kfactor' : 1.,
    },
    'WJetsToLNu_HT-100To200_ext' :{    
        'sam_name': 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 35244500,#27546978,
        'xsec_br' : 1292.,
        'matcheff': 1.,
        'kfactor' : 1.459,#1721.83/1292., #1.459
    },
    'WJetsToLNu_HT-100To200' :{    
        'sam_name': 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 3524450,#27546978,#cerca
        'xsec_br' : 1292.,
        'matcheff': 1.,
        'kfactor' : 1.459,#1721.83/1292., #1.459
    },
    'WJetsToLNu_HT-200To400' :{    
        'sam_name':'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 4963240,
        'xsec_br' : 385.9,
        'matcheff': 1.,
        'kfactor' : 1.434,#392.68/385.9, #1.434
    },
    'WJetsToLNu_HT-200To400_ext' :{    
        'sam_name':'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 19851624,#14888384,
        'xsec_br' : 385.9,
        'matcheff': 1.,
        'kfactor' : 1.434,#392.68/385.9, #1.434
    },
    'WJetsToLNu_HT-400To600' :{    
        'sam_name':'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 7432746,#1963464,
        'xsec_br' : 47.9,
        'matcheff': 1.,
        'kfactor' : 1.532,#42.89/47.9, #1.532
    },
    'WJetsToLNu_HT-400To600_ext' :{    
        'sam_name':'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 5469282,
        'xsec_br' : 47.9,
        'matcheff': 1.,
        'kfactor' : 1.532,#42.89/47.9, #1.532
    },
    'WJetsToLNu_HT-600To800' :{    
        'sam_name':'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 3722395,
        'xsec_br' : 12.8,
        'matcheff': 1.,
        'kfactor' : 1.004,#8.74/12.8,
    },
    'WJetsToLNu_HT-800To1200' :{    
        'sam_name':'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v2',
        'nevents' : 1540477,
        'xsec_br' : 5.261,
        'matcheff': 1.,
        'kfactor' : 1.004,#3.2684/5.261,
    },
    'WJetsToLNu_HT-800To1200_ext' :{    
        'sam_name':'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 7854734,#6314257,
        'xsec_br' : 5.261,
        'matcheff': 1.,
        'kfactor' : 1.004,#3.2684/5.261,
    },
    'WJetsToLNu_HT-1200To2500' :{    
        'sam_name':'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 246737*10,
        'xsec_br' : 1.334,
        'matcheff': 1.,
        'kfactor' : 1.004,#0.7082/1.334,
    },
    'WJetsToLNu_HT-1200To2500_ext' :{    
        'sam_name':'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0_ext1-v1',
        'nevents' : 7063909,#6817172,
        'xsec_br' : 1.334,
        'matcheff': 1.,
        'kfactor' : 1.004,#0.7082/1.334,
    },
    'WJetsToLNu_HT-2500ToInf' :{    
        'sam_name':'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_v0-v1',
        'nevents' : 2507809,#253561,
        'xsec_br' : 0.03089,
        'matcheff': 1.,
        'kfactor' : 1.004,#0.01816/0.03089,
    },   

}

