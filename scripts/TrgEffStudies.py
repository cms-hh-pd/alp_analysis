#!/usr/bin/env python 

import json
import os
from glob import glob

# ROOT imports
from ROOT import TChain, TH1F, TFile, vector
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, TriggerOperator, JetFilterOperator, BTagFilterOperator, JetPairingOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator, IsoMuFilterOperator, MetFilterOperator, JetPlotterOperator, FolderOperator, MiscellPlotterOperator, WeightSumOperator

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
parser.add_argument("--nbtag", help="min btag jets", type=int, default='4',  )
parser.add_argument("--btag", help="which btag algo", default='cmva')
parser.add_argument("-i", "--iDir", help="input directory", default="v2_20170222-trg") 
parser.add_argument("-o", "--oDir", help="output directory", default="trgEff_draft")
parser.add_argument("-f", "--no_savePlots", help="to save histos already in output file", action='store_false', dest='savePlots', )
parser.set_defaults(savePlots=True)
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts      
if not args.samList: samList = ['st','tt']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
trgListD   = 'singleMu_2016'
trgListN   = 'def_2016'
intLumi_fb = 35.9


iDir = "/lustre/cmswork/hh/alpha_ntuples/" + args.iDir
oDir = '/lustre/cmswork/hh/alp_moriond_base/' + args.oDir
data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])

if args.btag == 'cmva':  
    btagAlgo = "pfCombinedMVAV2BJetTags"
    btag_wp = wps['CMVAv2_moriond']
elif args.btag == 'csv': 
    btagAlgo  = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
    btag_wp = wps['CSVv2_moriond']


#weights to be applied 
weights        = {'PUWeight', 'LeptonWeight', 'BTagWeight'} #'lhe_weight_10',
weights_nobTag = {'PUWeight', 'LeptonWeight'} #'lhe_weight_10'
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)
print oDir

trg_namesD = triggerlists[trgListD]
trg_namesN = triggerlists[trgListN]
trg_names  = trg_namesD + trg_namesN
print trg_namesD
print trg_namesN
if not trg_names: print "### WARNING: empty hlt_names ###"
trg_namesD_v = vector("string")()
for t in trg_namesD: trg_namesD_v.push_back(t)
trg_namesN_v = vector("string")()
for t in trg_namesN: trg_namesN_v.push_back(t)

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)
w_nobTag_v = vector("string")()
for w in weights_nobTag: w_nobTag_v.push_back(w)

# to parse variables to the anlyzer
config = {"eventInfo_branch_name" : "EventInfo",
          "jets_branch_name": "Jets",
          "muons_branch_name" : "Muons",
          "electrons_branch_name" : "Electrons",
          "met_branch_name" : "MET",
          #"genbfromhs_branch_name" : "GenBFromHs",
          "genhs_branch_name" : "GenHs",
         }
config.update(        
        { "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData"  : False,
          "isSignal" : False,
          "lumiFb" : intLumi_fb,
          "isMixed" : False,
          "ofile_update" : False,
         } )        

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
for sname in snames:
    
    #get file names in all sub-folders:
    reg_exp = iDir+"/"+samples[sname]["sam_name"]+"/*/output.root"
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
    print "reg_exp: {}".format(reg_exp)

    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    else:
        if "Run" in files[0]: 
            config["isData"] = True
        if "GluGluToHH" in files[0] or "HHTo4B" in files[0]: config["isSignal"] = True
   
    #read counters to get generated events
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
    print  "empty files {}".format(nerr)
    print  "genevts {}".format(ngenev)

    #read weights from alpSamples 
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    json_str = json.dumps(config)
    
    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(BaseOperator(alp.Event)())
    selector.addOperator(FolderOperator(alp.Event)("base"))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"],w_nobTag_v))

    selector.addOperator(FolderOperator(alp.Event)("trigger"))
    selector.addOperator(TriggerOperator(alp.Event)(trg_namesD_v))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"],w_nobTag_v))

    selector.addOperator(FolderOperator(alp.Event)("acc"))
    selector.addOperator(JetFilterOperator(alp.Event)(2.4, 30., 4)) 
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"],w_nobTag_v))
#    selector.addOperator(JetPlotterOperator(alp.Event)("pt",w_nobTag_v))
#    selector.addOperator(MiscellPlotterOperator(alp.Event)(w_nobTag_v))

    selector.addOperator(FolderOperator(alp.Event)("btag"))
    selector.addOperator(BTagFilterOperator(alp.Event)(btagAlgo, btag_wp[1], args.nbtag, 99, config["isData"], data_path))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"],weights_v))

    selector.addOperator(FolderOperator(alp.Event)("isomu"))
    selector.addOperator(IsoMuFilterOperator(alp.Event)(0.15, 30., 1))  #debug 0.05
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"],weights_v))

    selector.addOperator(FolderOperator(alp.Event)("met"))
    selector.addOperator(MetFilterOperator(alp.Event)(40.))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"],weights_v))

    selector.addOperator(FolderOperator(alp.Event)("trg_Iso"))
    if args.savePlots: selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo,weights_v)) 
    if args.savePlots: selector.addOperator(MiscellPlotterOperator(alp.Event)(weights_v))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"],weights_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str, weights_v))

    selector.addOperator(FolderOperator(alp.Event)("trg_IsoAndJet"))
    selector.addOperator(TriggerOperator(alp.Event)(trg_namesN_v))
    if args.savePlots: selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo,weights_v))
    if args.savePlots: selector.addOperator(MiscellPlotterOperator(alp.Event)(weights_v))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"],weights_v))
    selector.addOperator(EventWriterOperator(alp.Event)(json_str, weights_v))

    #create tChain and process each files
    tchain = TChain("ntuple/tree")    
    for File in files:                     
        tchain.Add(File)       
    nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "maxevts {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1
   
    #some cleaning
    hcount.Reset()
    print "{}".format(procOpt)

print "### processed {} samples ###".format(ns) 
