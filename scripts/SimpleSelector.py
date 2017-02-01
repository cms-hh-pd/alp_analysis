#!/usr/bin/env python 

# good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, EventWriterOperator

TH1F.AddDirectory(0)

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("-s", "--samList", help="sample list", default="")
parser.add_argument("--jesUp", help="use JES up", action='store_true')
parser.add_argument("--jesDown", help="use JES down", action='store_true')
parser.add_argument("-i", "--iDir", help="input directory", default="v1_20161028_noJetCut") # _noJetCut -- 20161028 (ICHEP) -- 20161212 -- def_cmva
parser.add_argument("-o", "--oDir", help="output directory", default="def_cmva")
# NOTICE: do not use trigger, jesUp, jesDown with '-m'
parser.set_defaults(doTrigger=False, jesUp=False, jesDown=False, doMixed=False)
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['test']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
trgList   = 'def_2016'
intLumi_fb = 12.6 #36.26 12.6

iDir = "/lustre/cmswork/hh/alpha_ntuples/" + args.iDir
oDir = '/lustre/cmswork/hh/alp_baseSelector/' + args.oDir
if args.jesUp: oDir += "_JESup"
elif args.jesDown: oDir += "_JESdown"

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])

#weights to be applied 
weights        = {'PUWeight', 'GenWeight', 'BTagWeight'} 
weights_nobTag = {'PUWeight', 'GenWeight'} 

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)
w_nobTag_v = vector("string")()
for w in weights_nobTag: w_nobTag_v.push_back(w)
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

if args.doMixed: config = { "jets_branch_name": "Jets", }
else: config = { "eventInfo_branch_name" : "EventInfo",
              "jets_branch_name": "Jets",
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
          "isMixed" : args.doMixed,
         } )

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
for sname in snames:
    isHLT = False

    reg_exp = iDir+"/"+samples[sname]["sam_name"]+"/*/output.root" #for alpha_ntuple
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
    hcount = TH1F('hcount', 'num of genrated events',1,0,1)
    for f in files:
        tf = TFile(f)
        hcount.Add(tf.Get('counter/c_nEvents'))
        tf.Close()
    ngenev = hcount.GetBinContent(1)
    config["n_gen_events"]=ngenev
    print  "gen numEv {}".format(ngenev)

    #read weights from alpSamples 
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    json_str = json.dumps(config)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)

    #simple dump of alpha ntuples in alp format
    selector.addOperator(CounterOperator(alp.Event)(w_nobTag_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str, w_nobTag_v))

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
