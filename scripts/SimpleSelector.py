#!/usr/bin/env python 

# good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
from ROOT import TChain, TH1F, TFile, vector, gROOT
# custom ROOT classes 
from ROOT import alp, ComposableSelector

TH1F.AddDirectory(0)

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists


# exe parameters
numEvents  = 1000       # -1 to process all (10000)
samList    = {'trigger'}   # list of samples to be processed - append multiple lists , 'data', 'mainbkg'    , 'datall', 'mainbkg', 'minortt', 'dibosons', 'bosons','trigger'
trgList    = 'singleMu_2016'
trgListN   = 'def_2016'
intLumi_fb = 12.6          # data integrated luminosity

iDir       = '/lustre/cmswork/hh/alpha_ntuples/'
ntuplesVer = 'v0_20161004'         # equal to ntuple's folder
oDir       = './output/v0_Simple'         # output dir ('./test')
operator_file = "LiveOperator.h"
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
hcount = TH1F('hcount', 'num of genrated events',1,0,1)
for sname in snames:
    isHLT = False

    #get file names in all sub-folders:
    files = glob(iDir+ntuplesVer+"/"+samples[sname]["sam_name"]+"/*/output.root")
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    else:
        if "Run" in files[0]: config["isData"] = True 
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

    #read weights from alpSamples 
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    # load the operator
    gROOT.ProcessLine("#include \"{}\"".format(operator_file))
    operator_name = os.path.splitext(os.path.basename(operator_file))[0]
    Operator = importlib.import_module("ROOT.{}".format(operator_name))

    # define selectors list
    selector = ComposableSelector(alp.Event)(0, json.dumps(config))
    selector.addOperator(Operator(alp.Event)())

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
