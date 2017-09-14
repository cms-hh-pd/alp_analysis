#!/usr/bin/env python 
# to EXE: python scripts/MixingSelector.py -s data_moriond -i def_cmva

#good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator
from ROOT import EventWriterOperator, MixedEventWriterOperator
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereMixerOperator

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.workingpoints import wps
import itertools as it

TH1F.AddDirectory(0)


all_list = [i for i in it.product(range(1,11),range(1,11))]

comb_dict = {"train" : [(1,1),(1,2),(2,1),(2,2)],
              "test" : [(3,4),(5,6),(7,8),(9,10)],
              "appl" : [(4,3),(6,5),(8,7),(10,9)] }

comb_dict["large"] = list(set(all_list)-set(comb_dict["train"]))

comb_dict_vec = {}
# ugly vector of vector transformation
for k,v in comb_dict.items():
    t_vec = vector("std::vector<std::size_t>")()
    for pair in v:
        p_vec = vector("std::size_t")()
        for e in pair:
            p_vec.push_back(e)
        t_vec.push_back(p_vec)
    # assign given that is a reference    
    comb_dict_vec[k] = t_vec    


# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("-s", "--samList", help="sample list"     , default="")
parser.add_argument("-o", "--oDir"   , help="output directory (added to iDir)", default="mixed_ntuples")
parser.add_argument("-i", "--iDir"   , help="input directory (added to iDir)", default="def_cmva")
parser.add_argument("--btag", help="which btag algo", default='cmva')
parser.add_argument("--comb", help="set of combinations to use", choices=comb_dict.keys() )
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['SM']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
intLumi_fb = 35.9
mixing_comb = comb_dict_vec[args.comb]
print mixing_comb

iDir = '/lustre/cmswork/hh/alp_moriond_base/'+ args.iDir
oDir = iDir + "/" + args.oDir # saved inside iDir to keep track of original ntuples
data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

if args.btag == 'cmva':  
    btagAlgo = "pfCombinedMVAV2BJetTags"
    btag_wp = wps['CMVAv2_moriond']
elif args.btag == 'csv': 
    btagAlgo  = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
    btag_wp = wps['CSVv2_moriond']

# variables to check nearest-neightbour
nn_vars = ["thrustMayor","thrustMinor", "sumPz","invMass"]
nn_vars_v = vector("string")()
for v in nn_vars: nn_vars_v.push_back(v)

# to parse variables to the anlyzer
config = {"eventInfo_branch_name" : "EventInfo",
          "jets_branch_name": "Jets",
          "dijets_branch_name": "DiJets",
          #"dihiggs_branch_name": "DiHiggs",
          #"muons_branch_name" : "",
          #"electrons_branch_name" : "",
          #"met_branch_name" : "",
          "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "lumiFb" : intLumi_fb,
          "isMixed" : False,
          "ofile_update" : False,
         }

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
for sname in snames:
    isHLT = False

    #get file names in all sub-folders:
    reg_exp = iDir+"/"+sname+".root"
    print "reg_exp: {}".format(reg_exp) 
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue

    if "Run" in files[0]: config["isData"] = True 

    json_str = json.dumps(config)

    #get hem_tree for mixing
    tch_hem = TChain("pair/hem_tree")    
    for f in files: 
        tch_hem.Add(f)

    print tch_hem.GetEntries()

    # define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(ThrustFinderOperator(alp.Event)())
    selector.addOperator(HemisphereProducerOperator(alp.Event)())
    selector.addOperator(HemisphereMixerOperator(alp.Event)(tch_hem, btagAlgo, btag_wp[1], nn_vars_v, 11))
    selector.addOperator(MixedEventWriterOperator(alp.Event)(mixing_comb))

    #create tChain and process each files   
    tchain = TChain("pair/tree")    
    for File in files:                     
        tchain.Add(File)      
    entr = tchain.GetEntries() 
    nev = numEvents if (numEvents > 0 and numEvents < entr) else entr
    sname = sname+"_{}".format(args.comb)
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1
   
print "### processed {} samples ###".format(ns)
