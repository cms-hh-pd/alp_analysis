
# lists of trigger paths to be used to select events (logical OR). Insert the proper label in the config file.
# warning: square bracket and "" are compulsory.

triggerlists = {

   ''  : [], #null lists

   'def_2016'       : [ "HLT_QuadJet45_TripleBTagCSV_p087_v",
                        "HLT_DoubleJet90_Double30_TripleBTagCSV_p087_v" ],

   'prescaled_2016' : [ "HLT_DoubleJet90_Double30_DoubleBTagCSV_p087_v",
                        "HLT_QuadJet45_DoubleBTagCSV_p087_v" ],

   'singleMu_2016'  : [ "HLT_IsoMu18_v",
                        "HLT_IsoMu20_v",
                        "HLT_IsoMu22_v",
                        "HLT_IsoMu24_v", ],

   'singleMu_short'  : [ "HLT_IsoMu18_v",
                        #"HLT_IsoMu20_v",
                         "HLT_IsoMu22_v",
                        #"HLT_IsoMu24_v", 
                       ],

   'others_2016'  : [ ],

}
