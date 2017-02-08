
# lists of samples to be processed. Insert the proper label in the config file.

samlists = {

   'SM'      : ['HHTo4B_SM'],
   'signals' : ['HHTo4B_SM', 'HHTo4B_BM2','HHTo4B_BM3','HHTo4B_BM4','HHTo4B_BM5','HHTo4B_BM7','HHTo4B_BM8',
                'HHTo4B_BM9','HHTo4B_BM10','HHTo4B_BM11','HHTo4B_BM12','HHTo4B_BM13','HHTo4B_BMbox','VBF_HHTo4B_SM'], #'HHTo4B_BM6',

   'data'  : ['BTagCSVRun2016'],
   'data_ichep'    : ['BTagCSVRun2016B-v1','BTagCSVRun2016B-v2','BTagCSVRun2016C-v2','BTagCSVRun2016D-v2'], #12.6 fb-1
   'data_singleMu' : ['SingleMuonRun2016B-v1', 'SingleMuonRun2016B-v2', 'SingleMuonRun2016C-v2', 'SingleMuonRun2016D-v2'],
   'data_moriond'  : ['BTagCSVRun2016B-23Sep2016-v2', 'BTagCSVRun2016B-23Sep2016-v3', 'BTagCSVRun2016C-23Sep2016-v1',
                      'BTagCSVRun2016D-23Sep2016-v1', 'BTagCSVRun2016E-23Sep2016-v1', 'BTagCSVRun2016F-23Sep2016-v1', 
                      'BTagCSVRun2016G-23Sep2016-v1', 'BTagCSVRun2016H-PromptReco-v2', 'BTagCSVRun2016H-PromptReco-v3' ], #36.26 fb-1
   'data_moriond1' : ['BTagCSVRun2016B-23Sep2016-v2', 'BTagCSVRun2016B-23Sep2016-v3', 'BTagCSVRun2016C-23Sep2016-v1', 'BTagCSVRun2016D-23Sep2016-v1'],
   'data_moriond2' : ['BTagCSVRun2016E-23Sep2016-v1', 'BTagCSVRun2016F-23Sep2016-v1' ],
   'data_moriond3' : ['BTagCSVRun2016G-23Sep2016-v1', 'BTagCSVRun2016H-PromptReco-v2', 'BTagCSVRun2016H-PromptReco-v3' ],
   'data_moriond_singleMu' : [ 'SingleMuonRun2016B-23Sep2016-v1', 'SingleMuonRun2016B-23Sep2016-v3', 'SingleMuonRun2016C-23Sep2016-v1',
                      'SingleMuonRun2016D-23Sep2016-v1', 'SingleMuonRun2016E-23Sep2016-v1', 'SingleMuonRun2016F-23Sep2016-v1', 
                      'SingleMuonRun2016G-23Sep2016-v1', 'SingleMuonRun2016H-PromptReco-v2', 'SingleMuonRun2016H-PromptReco-v3' ], #36.26 fb-1

   'mainbkg' : ['QCD_HT100to200',
                'QCD_HT1000to1500', 'QCD_HT1000to1500_ext', 'QCD_HT1500to2000', 'QCD_HT1500to2000_ext', 
                'QCD_HT2000toInf', 'QCD_HT2000toInf_ext', 'QCD_HT200to300', 'QCD_HT200to300_ext', 'QCD_HT300to500',
                'QCD_HT300to500_ext', 'QCD_HT500to700', 'QCD_HT500to700_ext', 'QCD_HT700to1000', 'QCD_HT700to1000_ext',
                'TT' ],

   'minortt' : ['ttHTobb', 'TTZToQQ', 'TTWJetsToQQ', 'TTTT', 'ttbb', 'ST_tW_antitop_5f_incl', 'ST_tW_top_5f_incl'],

   'dibosons': ['ZH_HToBB_ZToQQ', 'WZ', 'ZZTo4Q'],

   'bosons'  : [ 'ZJetsToQQ_HT-600ToInf', 'DYJetsToQQ_HT180',
                'VBFHToBB', 'VBFHToBB_ext', 'GluGluHToBB', 'GluGluHToBB_ext'], 

   'def'     : ['HHTo4B_SM', 'HHTo4B_BM3', 'HHTo4B_BM13', 
                'BTagCSVRun2016B-v1','BTagCSVRun2016B-v2','BTagCSVRun2016C-v2','BTagCSVRun2016D-v2',
                'TT'],
   'def_noTrg' : ['HHTo4B_SM', 'HHTo4B_BM3', 'HHTo4B_BM13', 
                  'BTagCSVRun2016B-v1','BTagCSVRun2016B-v2','BTagCSVRun2016C-v2','BTagCSVRun2016D-v2',
                  'TT',
                  'QCD_HT1000to1500', 'QCD_HT1000to1500_ext', 'QCD_HT1500to2000', 'QCD_HT1500to2000_ext',
                  'QCD_HT2000toInf', 'QCD_HT2000toInf_ext', 'QCD_HT200to300', 'QCD_HT200to300_ext', 'QCD_HT300to500',
                  'QCD_HT300to500_ext', 'QCD_HT500to700', 'QCD_HT500to700_ext', 'QCD_HT700to1000', 'QCD_HT700to1000_ext'
                  'QCD_bEnriched_HT1000to1500', 'QCD_bEnriched_HT100to200', 'QCD_bEnriched_HT1500to2000', 'QCD_bEnriched_HT2000toInf', 'QCD_bEnriched_HT200to300', 'QCD_bEnriched_HT300to500', 'QCD_bEnriched_HT500to700', 'QCD_bEnriched_HT700to1000', 'QCD_HT1000to1500_BGenFilter', 'QCD_HT100to200_BGenFilter', 'QCD_HT1500to2000_BGenFilter', 'QCD_HT2000toInf_BGenFilter', 'QCD_HT200to300_BGenFilter', 'QCD_HT300to500_BGenFilter', 'QCD_HT500to700_BGenFilter', 'QCD_HT700to1000_BGenFilter' ],

   'trigger' : ['TT',
                'ST_t-channel_4f_lept',
                'SingleMuonRun2016B-v1', 'SingleMuonRun2016B-v2', 'SingleMuonRun2016C-v2', 'SingleMuonRun2016D-v2', ],

   'trigger_noHLT' : ['TT',
                'ST_s-channel_4f_lept', 'ST_t-channel_4f_lept',
                'WJetsToLNu_HT-100To200_ext', 'WJetsToLNu_HT-100To200', 'WJetsToLNu_HT-200To400',
                'WJetsToLNu_HT-200To400_ext', 'WJetsToLNu_HT-400To600', 'WJetsToLNu_HT-400To600_ext',
                'WJetsToLNu_HT-600To800', 'WJetsToLNu_HT-800To1200', 'WJetsToLNu_HT-800To1200_ext',
                'WJetsToLNu_HT-1200To2500', 'WJetsToLNu_HT-1200To2500_ext', 'WJetsToLNu_HT-2500ToInf'],

   ## single bkg
   'qcd' : [ 'QCD_HT200to300', 'QCD_HT200to300_ext', 'QCD_HT300to500', 'QCD_HT300to500_ext',
             'QCD_HT500to700', 'QCD_HT500to700_ext', 'QCD_HT700to1000', 'QCD_HT700to1000_ext',
             'QCD_HT1000to1500', 'QCD_HT1000to1500_ext', 'QCD_HT1500to2000', 'QCD_HT1500to2000_ext', 
             'QCD_HT2000toInf', 'QCD_HT2000toInf_ext' ],

   'qcd_500toInf' : [ 'QCD_HT500to700', 'QCD_HT500to700_ext', 'QCD_HT700to1000', 'QCD_HT700to1000_ext',
                      'QCD_HT1000to1500', 'QCD_HT1000to1500_ext', 'QCD_HT1500to2000', 'QCD_HT1500to2000_ext', 
                      'QCD_HT2000toInf', 'QCD_HT2000toInf_ext' ],
   'qcd_200to500' : [ 'QCD_HT200to300', 'QCD_HT200to300_ext', 'QCD_HT300to500', 'QCD_HT300to500_ext' ],

   'qcd_m' : [ 'QCD_HT200to300_m', 'QCD_HT300to500_m', 'QCD_HT500to700_m', 'QCD_HT700to1000_m',
               'QCD_HT1000to1500_m', 'QCD_HT1500to2000_m', 'QCD_HT2000toInf_m' ],

   'qcd_500toInf_m' : [ 'QCD_HT500to700_m', 'QCD_HT700to1000_m', 'QCD_HT1000to1500_m', 'QCD_HT1500to2000_m', 'QCD_HT2000toInf_m' ],
   'qcd_200to500_m' : [ 'QCD_HT200to300_m', 'QCD_HT300to500_m' ],

#   'qcd_b' : ['QCD_bEnriched_HT1000to1500', 'QCD_bEnriched_HT100to200', 'QCD_bEnriched_HT1500to2000', 'QCD_bEnriched_HT2000toInf', 'QCD_bEnriched_HT200to300', 'QCD_bEnriched_HT300to500', 'QCD_bEnriched_HT500to700', 'QCD_bEnriched_HT700to1000', 'QCD_HT1000to1500_BGenFilter', 'QCD_HT100to200_BGenFilter', 'QCD_HT1500to2000_BGenFilter', 'QCD_HT2000toInf_BGenFilter', 'QCD_HT200to300_BGenFilter', 'QCD_HT300to500_BGenFilter', 'QCD_HT500to700_BGenFilter', 'QCD_HT700to1000_BGenFilter' ],
   'qcd_b' : ['QCD_bEnriched_HT1000to1500',  'QCD_bEnriched_HT1500to2000', 'QCD_bEnriched_HT2000toInf',  'QCD_bEnriched_HT300to500', 'QCD_bEnriched_HT500to700', 'QCD_bEnriched_HT700to1000', 'QCD_HT1000to1500_BGenFilter',  'QCD_HT1500to2000_BGenFilter', 'QCD_HT2000toInf_BGenFilter',  'QCD_HT300to500_BGenFilter', 'QCD_HT500to700_BGenFilter', 'QCD_HT700to1000_BGenFilter' ],

   'tt' : ['TT'], #reHLT

   'st' : ['ST_t-channel_4f_lept'], #reHLT

   ## for testing 
   'short'   : ['QCD_HT300to500_BGenFilter', 'QCD_HT500to700_BGenFilter', 'QCD_HT700to1000_BGenFilter'],
   'test'   : ['BTagCSVRun2016'], #'QCD_HT200to300''SingleMuonRun2016B-v2'SingleMuonRun2016B-v2

}
