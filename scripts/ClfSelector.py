#!/usr/bin/env python 
# to EXE: python scripts/BaselineSelector.py -s SM -o output/bSel_sig_def

# good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, JetPlotterOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator, FolderOperator, ClassifierOperator
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereWriterOperator

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists
from Analysis.alp_analysis.workingpoints import wps

TH1F.AddDirectory(0)

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("-s", "--samList", help="sample list", default="")
parser.add_argument("-i", "--iDir", help="input directory", default="") 
parser.add_argument("-o", "--oDir", help="output directory", default="")
parser.set_defaults()
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['test']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
trgList   = 'def_2016'
intLumi_fb = 35.9

iDir = "/lustre/cmswork/hh/alp_mva/h5/" + args.iDir
oDir = '/lustre/cmswork/hh/alp_mva/h5/' + args.iDir + "/" + args.oDir

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])

if not os.path.exists(oDir): os.mkdir(oDir)
print oDir

# to parse variables to the anlyzer
config = {"jets_branch_name": "Jets",
          "dijets_branch_name": "DiJets",
          "dihiggs_branch_name": "DiHiggs",
          "classifier_branch_name": "classifier",
          "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "isSignal" : False,
          "lumiFb" : intLumi_fb,
          "isMixed" : False,
          "ofile_update" : False,
          "evt_weight_name" : "evtWeight",
         }

snames = []
for s in samList:
    snames.extend(samlists[s])

# to convert weights 
weights_v = vector("string")()

# process samples
ns = 0
for sname in snames:
    #get file names in all sub-folders:
    reg_exp = iDir+"/"+sname+".root"
    print "reg_exp: {}".format(reg_exp) 
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    else:
        if "Run" in files[0]: config["isData"] = True
        if "GluGluToHH" in files[0] or "HHTo4B" in files[0]: config["isSignal"] = True

    json_str = json.dumps(config)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(BaseOperator(alp.Event)())
    selector.addOperator(FolderOperator(alp.Event)("base"))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], weights_v))

    selector.addOperator(FolderOperator(alp.Event)("pair"))
    selector.addOperator(ClassifierOperator(alp.Event)(0.,0.3))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], weights_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str,weights_v))
    #create hemisphere library
    selector.addOperator(ThrustFinderOperator(alp.Event)())
    selector.addOperator(HemisphereProducerOperator(alp.Event)())
    selector.addOperator(HemisphereWriterOperator(alp.Event)())

    #create tChain and process each files
    tchain = TChain("pair/tree")
    f_tchain = TChain("extra")    
    for File in files:                     
        tchain.Add(File)
        f_tchain.Add(File.replace(".root","_extra.root"))
    tchain.AddFriend(f_tchain)       
    nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
    procOpt = "ofile=./"+sname+"_clf.root" if not oDir else "ofile="+oDir+"/"+sname+"_clf.root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1

print "### processed {} samples ###".format(ns)
