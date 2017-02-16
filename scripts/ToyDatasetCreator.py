#!/usr/bin/env python 
# to EXE: python scripts/ToyDatasetCreator.py 

# good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
import ROOT
from ROOT import TH1F, TFile, TEventList, vector, TChain
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator
from ROOT import DiJetPlotterOperator, JetPairingOperator
from ROOT import EventWriterOperator, IsoMuFilterOperator, MetFilterOperator, JetPlotterOperator, FolderOperator, MiscellPlotterOperator

from ROOT import EventWriterOperator, MixedEventWriterOperator
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereMixerOperator

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.alpSamplesOptions  import sam_opt
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists
from Analysis.alp_analysis.workingpoints import wps

TH1F.AddDirectory(0)

# parsing parameters

import argparse
parser = argparse.ArgumentParser(description='Create mixed dataset.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument('--nn_vars', nargs='+', default=default_nn_vars,help="list of vars for metric in NN search")
parser.add_argument('-l', '--lumi_factor', type=float, default=1.0,help="percentage of 12.9fb-1 to use")
parser.add_argument('-m', '--hh_times_sm', type=float, default=150.,help="times the expected SM hh contribution")
parser.add_argument('--mult', type=int, default=1,help="number of mixing combinations")
parser.add_argument('--extra_cut', default="",help="TTree::Draw like condition (e.g. && (@pfjets.size() > 5))" ) #debug
parser.add_argument('--extra_cut_name', default="",help="label for the extra cut") #debug
parser.add_argument("-v", "--ntuplesVer", help="input sub-folder", default="def_noTrg_test")
parser.add_argument("-o", "--oDir", help="output directory", default="/lustre/cmswork/hh/alp_baseSelector/toy")
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("--btag", help="which btag algo", default='cmva')
#parser.add_argument("-s", "--samList", help="sample list", default="")
args = parser.parse_args()

# exe parameters

numEvents  =  args.numEvts
oname = "QCD500_tt_SM100k"
samList = ['qcd_500toInf_m','tt','SM'] #,'SM' 'qcd_200to500_m','tt' # debug - qcd never as last sample
times_sm = 100000. #, args.hh_times_sm
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
weights = {}  #weights to be applied 'PUWeight', 'GenWeight', 'BTagWeight'
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)

if args.btag == 'cmva':  
    btagAlgo = "pfCombinedMVAV2BJetTags"
    btag_wp = wps['CMVAv2_moriond']
elif args.btag == 'csv': 
    btagAlgo  = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
    btag_wp = wps['CSVv2_moriond']

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
          "isMixed" : True,
          "lumiFb" : 0, #debug
         }

# to get sample names
snames = []
for s in samList:
    snames.extend(samlists[s])

tc_hem = TChain("pair/hem_tree")
tchain = TChain("pair/tree")

ns = 0
n_ev_subsam = []
l_eq_subsam = []
for s, sname in enumerate(snames):

    tc = TChain("pair/tree")
    samOpt = sam_opt[sname]
    reg_exp = iDir+ntuplesVer+"/"+sname+".root"
    files = glob(reg_exp)

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
    #read weights from alpSamples --to avoid crash -- not useful..
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    tc_hem.Add(reg_exp)
    tchain.Add(reg_exp)
    tc.Add(reg_exp)
    l_eq_subsam.append( ngenev / (samples[sname]['xsec_br']*samples[sname]['matcheff']*samples[sname]['kfactor']*1000) )
    n_ev_subsam.append(tc.GetEntries())
    print "{} ev_subsam {}".format(sname, n_ev_subsam)
    print "   l_eq_subsam {}".format(l_eq_subsam[s])
    print "   ngenev {}".format(ngenev)
    ns+=1

# set min lum eq
min_lum_eq = 999999.
for s, sname in enumerate(snames):
    if (l_eq_subsam[s] < min_lum_eq): min_lum_eq = l_eq_subsam[s]
print "min_lum_eq {}".format(min_lum_eq)

config["isMixed"]  = True #debug
config["lumiFb"]  = min_lum_eq

json_str = json.dumps(config)    

els = [TEventList("el"+sname,"el"+sname) for sname in snames]
n_ev_base = 0
t_sm = 1.
for s, sname in enumerate(snames):
    if(s == len(snames)-1): t_sm = times_sm #debug
    n_ev_sfrac = n_ev_subsam[s]*(min_lum_eq/l_eq_subsam[s])*t_sm
    print "# {} events to use: {} ".format(sname, n_ev_sfrac)
    print tchain.Draw(">>el{}".format(sname),"(Entry$ > {}) && ( Entry$ <= {} ) {}".format(n_ev_base, n_ev_base+n_ev_sfrac, extra_cut))
    n_ev_base += n_ev_subsam[s]
el = TEventList("el","el")
for list_to_add in els:
    el.Add(list_to_add)
print "total number of entries in list " + str(el.GetN())
tc_hem.SetEventList(el)
tchain.SetEventList(el)

selector = ComposableSelector(alp.Event)(0, json_str)

selector.addOperator(FolderOperator(alp.Event)("pair"))
selector.addOperator(JetPairingOperator(alp.Event)(4))
selector.addOperator(CounterOperator(alp.Event)(weights_v))
selector.addOperator(JetPlotterOperator(alp.Event)(bTagAlgo,weights_v))        
selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))
selector.addOperator(EventWriterOperator(alp.Event)(json_str,weights_v))

selector.addOperator(ThrustFinderOperator(alp.Event)())
selector.addOperator(HemisphereProducerOperator(alp.Event)())
selector.addOperator(HemisphereMixerOperator(alp.Event)(tc_hem, nn_vars_v))
selector.addOperator(MixedEventWriterOperator(alp.Event)())

ofile = oDir
nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
procOpt = "ofile=./"+oname+".root" if not oDir else "ofile="+oDir+"/"+oname+".root"
#procOpt = "ofile=./.root" if not oDir else "ofile="+oDir+"/mixed_.root"
print "max numEv {}".format(nev)
tchain.Process(selector, procOpt, nev)

#check_mixed_data(ofile, mult)

print "### mixed {} samples ###".format(ns)
