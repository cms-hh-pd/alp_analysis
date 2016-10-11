#!/usr/bin/env python 

import json
import os
from glob import glob

# ROOT imports
from ROOT import TChain, TH1F, TFile, vector
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, TriggerOperator, JetFilterOperator, BTagFilterOperator, JetPairingOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator, IsoMuFilterOperator, MetFilterOperator, JetPlotterOperator 

from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists

# exe parameters
numEvents  = 10000       # -1 to process all (10000)
samList    = {'trigger'}  # list of samples to be processed - append multiple lists , 'data', 'mainbkg'    , 'datall', 'mainbkg', 'minortt', 'dibosons', 'bosons','trigger'
trgList    = 'singleMu_2016'
trgListN   = 'def_2016'

iDir       = '/lustre/cmswork/hh/alpha_ntuples/'
ntuplesVer = 'v0_20161004'         # equal to ntuple's folder
oDir       = './output/v0_TrgStudy'         # output dir ('./test')
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

trg_names = triggerlists[trgList]
trg_namesN = triggerlists[trgListN]
trg_names.extend(trg_namesN) #to pass all triggers in config
if not trg_names: print "### WARNING: empty hlt_names ###"
trg_names_v = vector("string")()
for trg_name in trg_names: trg_names_v.push_back(trg_name)
trg_namesN_v = vector("string")()
for trg_nameN in trg_namesN: trg_namesN_v.push_back(trg_nameN)

# to parse variables to the anlyzer
config = {"jets_branch_name": "Jets",
          "hlt_names": trg_names, 
          "n_gen_events":0
         }

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
hcount = TH1F('hcount', 'num of genrated events',1,0,1)
for sname in snames:
    isHLT = False
    isData = True

    #get file names in all sub-folders:
    files = glob(iDir+ntuplesVer+"/"+samples[sname]["sam_name"]+"/*/output.root")
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    else:
        if "Run" in files[0]: isData = True 
        elif "_v14" in files[0]: isHLT = True #patch - check better way to look for HLT
        else:
            print "WARNING: no HLT, skip samples"
            continue

    #read counters to get generated eventsbj
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
    selector.addOperator(TriggerOperator(alp.Event)(trg_names_v))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(JetFilterOperator(alp.Event)(2.5, 30., 4))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(BTagFilterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.800, 2))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(IsoMuFilterOperator(alp.Event)(0.05, 30., 1))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(MetFilterOperator(alp.Event)(40.))
    selector.addOperator(CounterOperator(alp.Event)())
#     selector.addOperator(JetPairingOperator(alp.Event)(4))
#    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags"))
    selector.addOperator(CounterOperator(alp.Event)())
    selector.addOperator(EventWriterOperator(alp.Event)())

    selector.addOperator(TriggerOperator(alp.Event)(trg_namesN_v))
    selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags"))
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

print "### processed {} samples ###".format(ns) 
