
# lists of samples to be processed. Insert the proper label in the config file.

samlists = {

   'SM'      : {'HHTo4B_SM'},

   'signals' : {'HHTo4B_SM', 'HHTo4B_BM2','HHTo4B_BM3','HHTo4B_BM4','HHTo4B_BM5','HHTo4B_BM6','HHTo4B_BM7','HHTo4B_BM8',
                'HHTo4B_BM9','HHTo4B_BM10','HHTo4B_BM11','HHTo4B_BM12','HHTo4B_BM13','HHTo4B_BMbox'},

   'data'    : {'BTagCSVRun2016D'},

   'datall'  : {'SingleMuonRun2016D', 'BTagCSVRun2016D'},

   'mainbkg' : {'QCD_HT1000to1500', 'QCD_HT1000to1500_ext', 'QCD_HT1500to2000', 'QCD_HT1500to2000_ext', 
                'QCD_HT2000toInf', 'QCD_HT2000toInf_ext', 'QCD_HT200to300', 'QCD_HT200to300_ext', 'QCD_HT300to500',
                'QCD_HT300to500_ext', 'QCD_HT500to700', 'QCD_HT500to700_ext', 'QCD_HT700to1000', 'QCD_HT700to1000_ext',
                'QCD_bEnriched_HT1000to1500', 'QCD_bEnriched_HT100to200', 'QCD_bEnriched_HT1500to2000', 'QCD_bEnriched_HT2000toInf',
                'QCD_bEnriched_HT200to300', 'QCD_bEnriched_HT300to500', 'QCD_bEnriched_HT500to700', 'QCD_bEnriched_HT700to1000',
                'QCD_HT1000to1500_BGenFilter', 'QCD_HT100to200_BGenFilter', 'QCD_HT1500to2000_BGenFilter', 'QCD_HT2000toInf_BGenFilter',
                'QCD_HT200to300_BGenFilter', 'QCD_HT300to500_BGenFilter', 'QCD_HT500to700_BGenFilter', 'QCD_HT700to1000_BGenFilter',
                'TT' },

   'minortt' : {'ttHTobb', 'TTZToQQ', 'TTWJetsToQQ', 'TTTT', 'ttbb', 'ST_tW_antitop_5f_incl', 'ST_tW_top_5f_incl'},

   'dibosons': {'ZH_HToBB_ZToQQ', 'WZ', 'ZZTo4Q'},

   'bosons'  : { 'ZJetsToQQ_HT-600ToInf', 'DYJetsToQQ_HT180', #'WJetsToQQ_HT-600ToInf',
                'VBFHToBB', 'VBFHToBB_ext', 'GluGluHToBB', 'GluGluHToBB_ext'}, 
   'trigger' : {'ST_s-channel_4f_lept', 'ST_t-channel_4f_lept',
                'WJetsToLNu_HT-100To200_ext', 'WJetsToLNu_HT-100To200', 'WJetsToLNu_HT-200To400',
                'WJetsToLNu_HT-200To400_ext', 'WJetsToLNu_HT-400To600', 'WJetsToLNu_HT-400To600_ext',
                'WJetsToLNu_HT-600To800', 'WJetsToLNu_HT-800To1200', 'WJetsToLNu_HT-800To1200_ext',
                'WJetsToLNu_HT-1200To2500', 'WJetsToLNu_HT-1200To2500_ext', 'WJetsToLNu_HT-2500ToInf'},

   ## for testing 
   'short'   : {'HHTo4B_SM'},
   'test'   : {'WJetsToLNu_HT-100To200'},

}
