#!/usr/bin/env python 
# to EXE: python scripts/HistFromPangea.py

# good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator, JetPlotterOperator, FolderOperator, MiscellPlotterOperator
from ROOT import JEShifterOperator, JERShifterOperator, ReWeightingOperator

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists
from Analysis.alp_analysis.workingpoints import wps

TH1F.AddDirectory(0)

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--iDir", help="input directory", default="def_cmva")
parser.add_argument("-o", "--oDir", help="output directory", default="def_cmva")
parser.add_argument("-s", "--samList", help="sample list", default="")
parser.set_defaults()
args = parser.parse_args()

# exe parameters
intLumi_fb = 36.26
iDir = "/lustre/cmswork/hh/alp_moriond_base/" + args.iDir + "/"
if args.oDir: oDir = '/lustre/cmswork/hh/alp_moriond_base/' + args.oDir + "_pangea/"
else: oDir = '/lustre/cmswork/hh/alp_moriond_base/' + args.iDir + "_pangea/"
data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
# ---------------

#define sample list - default == all
if args.samList: sam_list_ = [args.samList]
else: sam_list_ = ["SM","BM1","BM2","BM3","BM4","BM5","BM6","BM7","BM8","BM9","BM10","BM11","BM12"] 

if not os.path.exists(oDir): os.mkdir(oDir)
print oDir

btagAlgo = "pfCombinedMVAV2BJetTags"
btag_wp = wps['CMVAv2_moriond']

# to parse variables to the anlyzer
config = { "eventInfo_branch_name" : "EventInfo",
              "jets_branch_name": "Jets",
              "dijets_branch_name": "DiJets",
              "dihiggs_branch_name": "DiHiggs",
              "genbfromhs_branch_name" : "GenBFromHs",
              "genhs_branch_name" : "GenHs",
              "tl_genhs_branch_name" : "TL_GenHs",
              "tl_genhh_branch_name" : "TL_GenHH",
            }
config.update(        
        { "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "isSignal" : False,
          "lumiFb" : intLumi_fb,
          "isMixed" : False,
         } )

ns = 0
#create tChain with pangea file
treename = "pair/tree"
tchain = TChain(treename)    
reg_exp = iDir+"HHTo4B_pangea.root"
print "\n reg_exp: {}".format(reg_exp) 
files = glob(reg_exp)
#preliminary checks
if not files: 
   print "WARNING: files do not exist"
   exit()
else:
   if "Run" in files[0]: config["isData"] = True
   if "GluGluToHH" in files[0] or "HHTo4B" in files[0]: config["isSignal"] = True
for File in files:                     
    tchain.Add(File)

json_str = json.dumps(config)

#weights to be applied 
for sam in sam_list_ :
  ns+=1
  selector = ComposableSelector(alp.Event)(0, json_str)
  selector.addOperator(BaseOperator(alp.Event)())
  weightsSM = {'PUWeight', 'PdfWeight', 'BTagWeight','ReWeighting_'+sam}
  weightsSM_v = vector("string")()
  for w in weightsSM: weightsSM_v.push_back(w)
  selector.addOperator(FolderOperator(alp.Event)("pair"))
  selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo, weightsSM_v))        
  selector.addOperator(DiJetPlotterOperator(alp.Event)(weightsSM_v))
  procOpt = "ofile=./"+"HHTo4B_"+sam+".root" if not oDir else "ofile="+oDir+"HHTo4B_"+sam+".root"
  tchain.Process(selector, procOpt, tchain.GetEntries())  

print "### processed {} samples ###".format(ns)
