#!/usr/bin/env python 
# to EXE: python scripts/MCTruthSelector.py -s SM -o output/bSel_sig_def

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
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereWriterOperator, MCTruthOperator

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists

TH1F.AddDirectory(0)

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("-s", "--samList", help="sample list", default="")
parser.add_argument("-v", "--ntuplesVer", help="input sub-folder", default="")
parser.add_argument("-o", "--oDir", help="output directory", default="")
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['SM']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
intLumi_fb = 12.6

iDir       = "./output/" #"/lustre/cmswork/hh/alpha_ntuples/"
if not args.ntuplesVer: ntuplesVer = "def"
else: ntuplesVer = args.ntuplesVer
if not args.oDir: oDir = "/lustre/cmswork/hh/alp_baseSelector/def_truth"
else: oDir = args.oDir

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
weights = {'PUWeight', 'GenWeight', 'BTagWeight'}  #weights to be applied
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)

# to parse variables to the anlyzer
config = {"eventInfo_branch_name" : "EventInfo",
          "jets_branch_name": "Jets",
          "dijets_branch_name": "DiJets",
          "genbfromhs_branch_name" : "GenBFromHs",
          "genhs_branch_name" : "GenHs",
          "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "lumiFb" : intLumi_fb,
         }

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
for sname in snames:

    #get file names in all sub-folders:
    reg_exp = iDir+ntuplesVer+"/"+sname+".root"
    print "reg_exp: {}".format(reg_exp) 
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    if "Run" in files[0]: config["isData"] = True

    #read counters to get generated eventsbj
    ngenev = 0
    h_genEvts = TH1F('h_genEvts', 'num of generated events',1,0,1)
    tf = TFile(files[0])
    if tf.Get('h_genEvts'):
        h_genEvts = tf.Get('h_genEvts')
    else:
        print "ERROR: no generated evts histos"
        continue       
    tf.Close()
    ngenev = h_genEvts.GetBinContent(1)
    config["n_gen_events"]=ngenev

    #read weights from alpSamples 
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    json_str = json.dumps(config)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(BaseOperator(alp.Event)())
    selector.addOperator(CounterOperator(alp.Event)())

    selector.addOperator(MCTruthOperator(alp.Event)(0.5, True))

    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(FolderOperator(alp.Event)("pair"))
    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))        
    selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str,weights_v))

    #create tChain and process each files
    tchain = TChain("pair/tree")    
    for File in files:                     
        tchain.Add(File)       
    nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1

print "### processed {} samples ###".format(ns)
