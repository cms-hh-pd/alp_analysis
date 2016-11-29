#!/usr/bin/env python 
# to EXE: python scripts/MixingSelector.py -s data_ichep -i data_def -o output/mixSel_data_def

# good old python modules
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
from Analysis.alp_analysis.triggerlists import triggerlists

TH1F.AddDirectory(0)

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("-s", "--samList", help="sample list"     , default="")
parser.add_argument("-o", "--oDir"   , help="output directory", default="./output/mixSel_sig_def")
parser.add_argument("-i", "--iDir"   , help="input directory (added to iDir)", default="MC_def")
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['SM']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
trgList   = 'def_2016'
intLumi_fb = 12.6

iDir = 'output/' + args.iDir #/lustre/cmswork/hh/alp_baseSelector/
oDir = args.oDir
data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
weights = {}  #weights to be applied - EventWeight, PUWeight, GenWeight 
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

trg_names = triggerlists[trgList]
if not trg_names: print "### WARNING: empty hlt_names ###"
trg_names_v = vector("string")()
for t in trg_names: trg_names_v.push_back(t)

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)

nn_vars = ["thrustMayor","thrustMinor", "sumPz","invMass"]
nn_vars_v = vector("string")()
for v in nn_vars: nn_vars_v.push_back(v)



# to parse variables to the anlyzer
config = {"eventInfo_branch_name" : "EventInfo",
          "jets_branch_name": "Jets",
          "dijets_branch_name": "DiJets",
         # "dihiggs_branch_name": "DiHiggs",
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
         }

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
for sname in snames:
    isHLT = False

    #get file names in all sub-folders:
    reg_exp = iDir+"/"+sname+"*.root"
    print "reg_exp: {}".format(reg_exp) 
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue

    if "Run" in files[0]: config["isData"] = True 

    #read weights from alpSamples 
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    json_str = json.dumps(config)

    #get hem_tree for mixing
    tch_hem = TChain("pair/hem_tree")    
    for f in files: 
        tch_hem.Add(f)

    print tch_hem.GetEntries()    

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(ThrustFinderOperator(alp.Event)())
    selector.addOperator(HemisphereProducerOperator(alp.Event)())
    selector.addOperator(HemisphereMixerOperator(alp.Event)(tch_hem, nn_vars_v))
    selector.addOperator(MixedEventWriterOperator(alp.Event)())

    #create tChain and process each files   
    tchain = TChain("pair/tree")    
    for File in files:                     
        tchain.Add(File)       
    nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1
   
    #some cleaning
    #hcount.Reset()

print "### processed {} samples ###".format(ns)
