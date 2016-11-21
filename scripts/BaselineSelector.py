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
parser.add_argument("-o", "--oDir", help="output directory", default="")
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['qcd_b']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
trgList   = 'def_2016'
intLumi_fb = 12.6

iDir       = "/lustre/cmswork/hh/alpha_ntuples/"
ntuplesVer = "v1_20161028"        
if not args.oDir: oDir = "/lustre/cmswork/hh/alp_baseSelector/def"
else: oDir = args.oDir

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
weights = {'PUWeight', 'GenWeight', 'BTagWeight'}  #weights to be applied
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
config = {"eventInfo_branch_name" : "EventInfo",
          "jets_branch_name": "Jets",
          #"muons_branch_name" : "",
          #"electrons_branch_name" : "",
          #"met_branch_name" : "",
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
    isHLT = False

    #get file names in all sub-folders:
    reg_exp = iDir+ntuplesVer+"/"+samples[sname]["sam_name"]+"/*/output.root"
    print "reg_exp: {}".format(reg_exp) 
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    else:
        if "Run" in files[0]: config["isData"] = True 
        elif "_withHLT" in files[0]: isHLT = True
        elif "_reHLT" in files[0]: isHLT = True
        else:
            print "WARNING: no HLT branch in tree."

    #read counters to get generated eventsbj
    ngenev = 0
    nerr = 0
    hcount = TH1F('hcount', 'num of genrated events',1,0,1)
    for f in files:
        tf = TFile(f)
        if tf.Get('counter/c_nEvents'):
            hcount.Add(tf.Get('counter/c_nEvents'))
        else:
            nerr+=1        
        tf.Close()
    ngenev = hcount.GetBinContent(1)
    config["n_gen_events"]=ngenev
    print  "gen numEv {}".format(ngenev)
    print  "empty files {}".format(nerr)

    #read weights from alpSamples 
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    json_str = json.dumps(config)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(BaseOperator(alp.Event)())
    selector.addOperator(CounterOperator(alp.Event)())

   # selector.addOperator(TriggerOperator(alp.Event)(trg_names_v))
    selector.addOperator(CounterOperator(alp.Event)())

    selector.addOperator(JetFilterOperator(alp.Event)(2.5, 30., 4))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(FolderOperator(alp.Event)("acc"))
    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))

    selector.addOperator(BTagFilterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.800, 4, config["isData"], data_path))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(FolderOperator(alp.Event)("btag"))
    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))        

    selector.addOperator(JetPairingOperator(alp.Event)(4))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(FolderOperator(alp.Event)("pair"))
    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))        
    selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str,weights_v))
    selector.addOperator(ThrustFinderOperator(alp.Event)())
    selector.addOperator(HemisphereProducerOperator(alp.Event)())
    selector.addOperator(HemisphereWriterOperator(alp.Event)())

    #create tChain and process each files
    tchain = TChain("ntuple/tree")    
    for File in files:                     
        tchain.Add(File)       
    nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1
   
    #some cleaning
    hcount.Reset()

print "### processed {} samples ###".format(ns)
