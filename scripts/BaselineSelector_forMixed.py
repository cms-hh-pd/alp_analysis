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
from ROOT import alp, ComposableSelector, CounterOperator, TriggerOperator, JetFilterOperator, BTagFilterOperator, JetPairingOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator, IsoMuFilterOperator, MetFilterOperator, JetPlotterOperator, FolderOperator, MiscellPlotterOperator
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereWriterOperator

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
parser.add_argument("-v", "--ntuplesVer", help="input sub-folder", default="def_noTrg_mix")
parser.add_argument("-o", "--oDir", help="output directory", default="/lustre/cmswork/hh/alp_baseSelector/mixed")
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['test']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
trgList   = 'def_2016'
intLumi_fb = 1.

iDir       = "./output/" #"/lustre/cmswork/hh/alpha_ntuples/"
ntuplesVer = args.ntuplesVer
oDir = args.oDir

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
weights = {}  #weights to be applied 'PUWeight', 'GenWeight', 'BTagWeight'
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

trg_names = triggerlists[trgList]
if not trg_names: print "### WARNING: empty hlt_names ###"
trg_names_v = vector("string")()
for t in trg_names: trg_names_v.push_back(t)

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)


# to parse variables to the anlyzer
config = {#"eventInfo_branch_name" : "EventInfo",
          "jets_branch_name": "Jets",
          #"muons_branch_name" : "",
          #"electrons_branch_name" : "",
          #"met_branch_name" : "",
          "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "lumiFb" : 0,
         }

snames = []
for s in samList:
    if not s in samlists: 
        snames.append(samples[s]['sam_name'])
    else: 
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
    h_invFb = TH1F('h_invFb', '',1,0,1)
    tf = TFile(files[0])
    if tf.Get('h_w_oneInvFb'):
        h_genEvts = tf.Get('h_w_oneInvFb')
    else:
        print "ERROR: no invFb histos"
        continue       
    tf.Close()
    intLumi_fb = h_invFb.GetBinContent(1)

    config["isMixed"]  = True #debug
    config["lumiFb"]  = intLumi_fb

    #read weights from alpSamples 
    config["n_gen_events"]=1.
    config["xsec_br"]  = 1.
    config["matcheff"] = 1.
    config["kfactor"]  = 1.

    json_str = json.dumps(config)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(BaseOperator(alp.Event)())
    selector.addOperator(FolderOperator(alp.Event)("base"))
    selector.addOperator(CounterOperator(alp.Event)(weights_v))

    selector.addOperator(FolderOperator(alp.Event)("acc"))
    selector.addOperator(JetFilterOperator(alp.Event)(2.5, 30., 4))
    selector.addOperator(CounterOperator(alp.Event)(weights_v)) #debug - no bTagWeight?
    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))

    selector.addOperator(FolderOperator(alp.Event)("btag"))
    selector.addOperator(BTagFilterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.800, 4, config["isData"], data_path))
    selector.addOperator(CounterOperator(alp.Event)(weights_v))
    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))        

    selector.addOperator(FolderOperator(alp.Event)("pair"))
    selector.addOperator(JetPairingOperator(alp.Event)(4))
    selector.addOperator(CounterOperator(alp.Event)(weights_v))

    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))        
    selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str,weights_v))
    selector.addOperator(ThrustFinderOperator(alp.Event)())
    selector.addOperator(HemisphereProducerOperator(alp.Event)())
    selector.addOperator(HemisphereWriterOperator(alp.Event)())

    #create tChain and process each files
    tchain = TChain("mix_tree")    
    for File in files:                     
        tchain.Add(File)       
    nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1

print "### processed {} samples ###".format(ns)
