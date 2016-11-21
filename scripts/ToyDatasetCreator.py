#!/usr/bin/env python 
# to EXE: python scripts/ToyDatasetCreator.py 

# good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
import ROOT
from ROOT import TH1, TFile, TEventList, vector, TChain
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator
from ROOT import EventWriterOperator, MixedEventWriterOperator
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereMixerOperator

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.alpSamplesOptions  import sam_opt
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists

TH1.AddDirectory(0)

# parsing parameters

import argparse
parser = argparse.ArgumentParser(description='Create mixed dataset.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument('--nn_vars', nargs='+', default=default_nn_vars,help="list of vars for metric in NN search")
parser.add_argument('-l', '--lumi_factor', type=float, default=1.0,help="percentage of 12.9fb-1 to use")
parser.add_argument('-m', '--hh_times_sm', type=float, default=150.,help="times the expected SM hh contribution")
parser.add_argument('--mult', type=int, default=1,help="number of mixing combinations")
parser.add_argument('--extra_cut', default="",help="TTree::Draw like condition (e.g. && (@pfjets.size() > 5))" ) #debug
parser.add_argument('--extra_cut_name', default="",help="label for the extra cut") #debug
parser.add_argument("-v", "--ntuplesVer", help="input sub-folder", default="def_noTrg")
parser.add_argument("-o", "--oDir", help="output directory", default="/lustre/cmswork/hh/alp_baseSelector/toy")
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
#parser.add_argument("-s", "--samList", help="sample list", default="")
args = parser.parse_args()

# exe parameters

numEvents  =  args.numEvts
samList = ['qcd', 'tt', 'SM'] #,'SM'  # debug - qcd never as last sample
fraction = [0.80, 0.19 , 5.668e-6 ] #5.668e-6 what is it?
times_sm = [1., 1., args.hh_times_sm]
intLumi_fb = 12.6
lumi_factor = args.lumi_factor
lumi = intLumi_fb*lumi_factor

nn_vars = ["thrustMayor","thrustMinor", "sumPz","invMass"]
nn_vars_v = vector("string")()
for v in nn_vars: nn_vars_v.push_back(v)

mult = args.mult
extra_cut = args.extra_cut
extra_cut_name = args.extra_cut_name

iDir       = "/lustre/cmswork/hh/alp_baseSelector/"
ntuplesVer = args.ntuplesVer
oDir = args.oDir
data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
weights = {'PUWeight', 'GenWeight', 'BTagWeight'}  #weights to be applied
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)

# to parse variables to the anlyzer
config = {"eventInfo_branch_name" : "EventInfo",
          "jets_branch_name": "Jets",
          "dijets_branch_name": "DiJets",
          #"muons_branch_name" : "",
          #"electrons_branch_name" : "",
          #"met_branch_name" : "",
          "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "lumiFb" : intLumi_fb,
         }

# to get sample names
snames = []
for s in samList:
    snames.extend(samlists[s])

tc_hem = TChain("pair/hem_tree")
tchain = TChain("pair/tree")
n_evs = [0]

#to get weights
order_prec = -1
ws = []
weights_sum = []
ns = 0
for s, sname in enumerate(snames):
    samOpt = sam_opt[sname]
    print sname
    ws.append( samples[sname]["xsec_br"]*samples[sname]["matcheff"]*samples[sname]["kfactor"] )
    if(samOpt['order'] != order_prec): 
        weights_sum.append(ws[s])
        if s>0 : ns+=1
    else: weights_sum[ns] += ws[s]
    order_prec = sam_opt[sname]['order']

#add file to tchain and normalize wieght to 1
ns = 0
ws_n = []
for s, sname in enumerate(snames):
    samOpt = sam_opt[sname]
    reg_exp = iDir+ntuplesVer+"/"+sname+".root"
    tc_hem.Add(reg_exp)
    tchain.Add(reg_exp)
    n_evs.append(tchain.GetEntries())
    if s>0 and samOpt['order'] != order_prec : ns+=1
    ws_n.append(ws[s]/weights_sum[ns])
    order_prec = sam_opt[sname]['order']

#cross check
for s,sname in enumerate(snames):
    print ws_n[s]

json_str = json.dumps(config)

els = [TEventList("el"+sname,"el"+sname) for sname in snames]
for s, sname in enumerate(snames):
    print ws_n[s]
    tot_frac = ws_n[s]*fraction[s]*times_sm[s]*lumi_factor
    n_ev = float((n_evs[s+1]-n_evs[s])*tot_frac)
    print "# {} events to use: {} ".format(sname, n_ev)
    print tchain.Draw(">>el{}".format(sname),"(Entry$ > {}) && ( Entry$ <= {} ) {}".format(n_evs[s], n_evs[s]+n_ev, extra_cut))
el = TEventList("el","el")
for list_to_add in els:
    el.Add(list_to_add)
print "total number of entries in list" + str(el.GetN())
tc_hem.SetEventList(el)
tchain.SetEventList(el)

selector = ComposableSelector(alp.Event)(0, json_str)
selector.addOperator(ThrustFinderOperator(alp.Event)())
selector.addOperator(HemisphereProducerOperator(alp.Event)())
selector.addOperator(HemisphereMixerOperator(alp.Event)(tc_hem, nn_vars_v))
selector.addOperator(MixedEventWriterOperator(alp.Event)())

ofile = oDir

nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
procOpt = "ofile=./mixed_.root" if not oDir else "ofile="+oDir+"/mixed_.root"
print "max numEv {}".format(nev)
tchain.Process(selector, procOpt, nev)

#check_mixed_data(ofile, mult)

print "### mixed {} samples ###".format(ns)
