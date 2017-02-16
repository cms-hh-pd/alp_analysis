#!/usr/bin/env python 
# to EXE: python scripts/BaselineSelector.py -s data_moriond -t -o def_cmva

# good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, TriggerOperator, JetFilterOperator, BTagFilterOperator, JetPairingOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator, IsoMuFilterOperator, MetFilterOperator, JetPlotterOperator, FolderOperator, MiscellPlotterOperator
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereWriterOperator, JEShifterOperator, JERShifterOperator, ReWeightingOperator

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
parser.add_argument("-i", "--iDir", help="input directory", default="def_cmva")
parser.add_argument("-o", "--oDir", help="output directory", default="re_weighted")
parser.add_argument("-f", "--no_savePlots", help="to save histos already in output file", action='store_false', dest='savePlots', ) #to get faster execution
# NOTICE: do not use trigger, jesUp, jesDown with '-m'
parser.set_defaults(doTrigger=False, doMixed=False, savePlots=True)
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['SM']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
trgList   = 'def_2016'
intLumi_fb = 36.26

iDir = "/lustre/cmswork/hh/alp_moriond_base/" + args.iDir
oDir = '/lustre/cmswork/hh/alp_moriond_base/' + args.oDir

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])

#weights to be applied 
weights        = {'PUWeight', 'PdfWeight', 'BTagWeight'}
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)
print oDir

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)

# to parse variables to the anlyzer
config = { "eventInfo_branch_name" : "EventInfo",
              "jets_branch_name": "Jets",
              "dijets_branch_name": "DiJets",
              "dihiggs_branch_name": "DiHiggs",
              "genbfromhs_branch_name" : "GenBFromHs",
              "genhs_branch_name" : "GenHs",
              "tl_genhs_branch_name" : "TL_GenHs",
            }
#"muons_branch_name" : "",
#"electrons_branch_name" : "",
#"met_branch_name" : "",
config.update(        
        { "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "lumiFb" : intLumi_fb,
          "isMixed" : False,
         } )

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
for sname in snames:

 #loop on all samples needed.... or just the one to apply rew?
    #get file names in all sub-folders:
    reg_exp = iDir+sname+".root"
    print "reg_exp: {}".format(reg_exp) 
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    else:
        if "Run" in files[0]: config["isData"] = True

    #read weights from alpSamples 
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    json_str = json.dumps(config)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(BaseOperator(alp.Event)())

    selector.addOperator(FolderOperator(alp.Event)("base"))
    selector.addOperator(CounterOperator(alp.Event)(weights_v))

    selector.addOperator(ReWeightingOperator(alp.Event)())

    selector.addOperator(FolderOperator(alp.Event)("reweight"))
    selector.addOperator(CounterOperator(alp.Event)(weights_v))
    if args.savePlots: selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo, weights_v))        
    if args.savePlots: selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str, weights_v))

    #create tChain and process each files
    treename = "pair/tree"
    tchain = TChain(treename)    
    for File in files:                     
        tchain.Add(File)
    nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1
   
    #some cleaning


print "### processed {} samples ###".format(ns)
