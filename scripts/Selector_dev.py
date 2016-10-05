#!/usr/bin/env python 

import json
import os
from glob import glob

# ROOT imports
from ROOT import TChain
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, JetFilterOperator, BTagFilterOperator, JetPairingOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator

from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists

# exe parameters
numEvents  = -1       # -1 to process all (10000)
samList    = 'signals'         # list of samples to be processed
oDir       = './test'         # output dir ('./test')
ntuplesVer = 'v0_20161004'         # equal to ntuple's folder
iDir       = '/lustre/cmswork/hh/alpha_ntuples/'
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

config = {"jets_branch_name": "Jets",
          "hlt_names":[]}

snames = samlists[samList]

# process samples
for sname in snames:
    isHH = False
    if "HH" in sname: isHH = True #unused...

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

    print "### processing {}".format(sname)    
    tchain = TChain("ntuple/tree")
    #get files in all sub-folders:
    files = glob(iDir+ntuplesVer+"/"+samples[sname]["sam_name"]+"/*/output.root") 
    if not files: print "WARNING: files do not exist"
    for File in files:
        tchain.Add(File)
    nev = numEvents if numEvents > 0 else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev) 
