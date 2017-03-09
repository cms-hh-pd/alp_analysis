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
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereWriterOperator, DiHiggsFilterOperator

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
parser.add_argument("-o", "--oDir", help="output directory", default="mass_cmva")
parser.add_argument("--jetCorr", help="apply [0=jesUp, 1=jesDown, 2=jerUp, 3=jerDown]", type=int, default='-1')
parser.add_argument("-b", "--doBlind", help="do blind", action='store_true')
parser.add_argument("-m", "--runMixed", help="to run on mixed samples", action='store_true') 
parser.add_argument("--btag", help="which btag algo", default='cmva')
parser.set_defaults(doBlind=False, runMixed=False)
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['signals']
else: samList = [args.samList]
trgList   = 'def_2016'
intLumi_fb = 35.9

c_dijets_mass = {100.,180.,90.,170.}
c_dijets_mass_v = vector("double")()
for c in c_dijets_mass: c_dijets_mass_v.push_back(c)

iDir = "/lustre/cmswork/hh/alp_moriond_base/"+ args.iDir
oDir = '/lustre/cmswork/hh/alp_moriond_base/' + args.oDir
if args.runMixed:
    iDir += "_mixed"
    oDir += "_mixed"
if args.jetCorr   == 0: 
    iDir += "_JESup"
    oDir += "_JESup"
elif args.jetCorr == 1: 
    iDir += "_JESdown"
    oDir += "_JESdown"
elif args.jetCorr == 2:
    iDir += "_JERup"
    oDir += "_JERup"
elif args.jetCorr == 3:
    iDir += "_JERdown"
    oDir += "_JERdown"
iDir += "/"
oDir += "/"

doBlind = args.doBlind

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])

weights        = {}
if not args.runMixed:
    weights        = {'PUWeight', 'PdfWeight', 'BTagWeight'}
# ---------------

if args.btag == 'cmva':  
    btagAlgo = "pfCombinedMVAV2BJetTags"
    btag_wp = wps['CMVAv2_moriond']
elif args.btag == 'csv': 
    btagAlgo  = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
    btag_wp = wps['CSVv2_moriond']

if not os.path.exists(oDir): os.mkdir(oDir)

trg_names = triggerlists[trgList]
if not trg_names: print "### WARNING: empty hlt_names ###"
trg_names_v = vector("string")()
for t in trg_names: trg_names_v.push_back(t)

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)

# to parse variables to the anlyzer
config = {
          "jets_branch_name": "Jets",
          "dijets_branch_name": "DiJets",
          "dihiggs_branch_name": "DiHiggs",
          "tl_genhh_branch_name" : "TL_GenHH"
          }
if not args.runMixed: config.update(
         {"eventInfo_branch_name" : "EventInfo",
          "genbfromhs_branch_name" : "GenBFromHs",
          "genhs_branch_name" : "GenHs",
          "tl_genhs_branch_name" : "TL_GenHs",
         })
config.update(        
         {"n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "isSignal" : False,
          "lumiFb" : intLumi_fb,
          "isMixed" : args.runMixed,
         })

snames = []
for s in samList:
    snames.extend(samlists[s])

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

    if not args.runMixed:
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

    selector.addOperator(FolderOperator(alp.Event)("base"))
    selector.addOperator(CounterOperator(alp.Event)(weights_v))

    selector.addOperator(FolderOperator(alp.Event)("pair"))
    selector.addOperator(DiHiggsFilterOperator(alp.Event)(c_dijets_mass_v, doBlind))
    selector.addOperator(CounterOperator(alp.Event)(weights_v))
    selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo, weights_v))        
    selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str, weights_v))

    #selector.addOperator(DiHiggsFilterOperator(alp.Event)(doBlind, 250.))
    #selector.addOperator(CounterOperator(alp.Event)())
    #selector.addOperator(FolderOperator(alp.Event)("pair_minM250"+opt))
    #selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))
    #selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))
    #selector.addOperator(EventWriterOperator(alp.Event)(json_str,weights_v))

    #selector.addOperator(DiHiggsFilterOperator(alp.Event)(doBlind, 350.))
    #selector.addOperator(CounterOperator(alp.Event)())
    #selector.addOperator(FolderOperator(alp.Event)("pair_minM350"+opt))
    #selector.addOperator(JetPlotterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags",weights_v))
    #selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))
    #selector.addOperator(EventWriterOperator(alp.Event)(json_str,weights_v))

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
