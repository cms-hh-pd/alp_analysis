#!/usr/bin/env python 

import json
import os
from glob import glob

# ROOT imports
from ROOT import TChain, TH1F, TFile
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, JetFilterOperator, BTagFilterOperator, JetPairingOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator

from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists

# exe parameters
numEvents  = 10000       # -1 to process all (10000)
samList    = {'SM'}  # list of samples to be processed - append multiple lists , 'data', 'mainbkg'
oDir       = './test'         # output dir ('./test')
ntuplesVer = 'v0_20161004'         # equal to ntuple's folder
iDir       = '/lustre/cmswork/hh/alpha_ntuples/'
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

# to parse variables to the anlyzer
config = {"jets_branch_name": "Jets",
          "hlt_names":[], "n_gen_events":0
         }

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
hcount = TH1F('hcount', 'num of genrated events',1,0,1)
for sname in snames:    
    isHH = False
    if "HH" in sname: isHH = True #unused...

    print "### processing {}".format(sname)        
   ######
    #get file names in all sub-folders:
    files = glob(iDir+ntuplesVer+"/"+samples[sname]["sam_name"]+"/*/output.root")
    if not files: print "WARNING: files do not exist"

    #read counters to get generated events
    ngenev = 0
    for f in files:
        tf = TFile(f)
        hcount.Add(tf.Get('counter/c_nEvents'))
        tf.Close()
    ngenev = hcount.GetBinContent(1)
    config["n_gen_events"]=ngenev
    print  "gen numEv {}".format(ngenev)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json.dumps(config))
    selector.addOperator(BaseOperator(alp.Event)())
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(JetFilterOperator(alp.Event)(2.5, 30., 4))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(BTagFilterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.800, 4))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(JetPairingOperator(alp.Event)(4))
    selector.addOperator(DiJetPlotterOperator(alp.Event)())
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(EventWriterOperator(alp.Event)())

    #create tChain and process each files
    tchain = TChain("ntuple/tree")
    for File in files:                     
        tchain.Add(File)   
    nev = numEvents if numEvents > 0 else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1
   
    #some cleaning
    hcount.Reset()

print "### processed {} samples".format(ns) 
