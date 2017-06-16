#!/usr/bin/env python 

# good old python modules
import json
import os
from glob import glob

import numpy as np

# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT
from ROOT import TEventList
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator
from ROOT import EventWriterOperator, MixedEventWriterOperator
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereMixerOperator

import pandas as pd
from tqdm import trange

# imports from ../python 
from Analysis.alp_analysis.workingpoints import wps


def array_to_list(index_array, ev_list):
    for i in index_array:
        ev_list.Enter(i)
    return ev_list    

TH1F.AddDirectory(0)

comb_dict = {"train" : [[1,1],[1,2],[2,1],[2,2]],
              "test" : [[3,4],[5,6],[7,8],[9,10]],
              "appl" : [[4,3],[6,5],[8,7],[10,9]] }

comb_dict_vec = {}
# ugly vector of vector transformation
for k,v in comb_dict.items():
    t_vec = vector("std::vector<std::size_t>")()
    for pair in v:
        p_vec = vector("std::size_t")()
        for e in pair:
            p_vec.push_back(e)
        t_vec.push_back(p_vec)
    # assign given that is a reference    
    comb_dict_vec[k] = t_vec    

weights = []
# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)


# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("--sig", help="signal cross section", type=int, default=0)
parser.add_argument("--comb", help="set of combinations to use", choices=comb_dict.keys() )
args = parser.parse_args()


n_samples = 100
# sample with replacement
replace = False
# numpy random states for reproducibility
sig_rs = np.random.RandomState(2020)
bkg_rs = np.random.RandomState(1010)

sig_xs_per_fb = 0.670
n_sam_sig_ev = int(sig_xs_per_fb*args.sig) 
print n_sam_sig_ev

# exe parameters
numEvents  =  args.numEvts
intLumi_fb = 35.9
mixing_comb = comb_dict_vec[args.comb]

bkg_parent_files = ["/lustre/cmswork/hh/alp_moriond_base/bootstrap_parent/BTagCSVRun2016_test.root",
                    "/lustre/cmswork/hh/alp_moriond_base/bootstrap_parent/BTagCSVRun2016_appl.root"]
sig_parent_files = ["/lustre/cmswork/hh/alp_moriond_base/bootstrap_parent/HHTo4B_SM_all.root"]
sig_index_h5 = "/lustre/cmswork/hh/alp_moriond_base/bootstrap_parent/indexes.h5"
sample_path = "/lustre/cmswork/hh/alp_moriond_base/bootstrap_mixing_sig_{}_fb".format(args.sig)

# load h5 index (avoid using training events)
with pd.HDFStore(sig_index_h5) as store:

    sig_tot_index = sum([store[s].size for s in ["d_train","d_test", "d_appl"]]) 
    raw_index_not_train = np.concatenate([store[s].values for s in ["d_test", "d_appl"]])

tch_hem = TChain("pair/hem_tree")
tchain = TChain("pair/tree")

for bkg_parent_file in bkg_parent_files:
    tch_hem.Add(bkg_parent_file)
    tchain.Add(bkg_parent_file)

n_tot_bkg_ev = tchain.GetEntries()
bkg_all_arr = np.arange(n_tot_bkg_ev)

for sig_parent_file in sig_parent_files:
    tch_hem.Add(sig_parent_file)
    tchain.Add(sig_parent_file)

n_tot_sig_ev = tchain.GetEntries() - n_tot_bkg_ev
sm_index_not_train = raw_index_not_train - sig_tot_index + n_tot_sig_ev
sm_index_not_train = sm_index_not_train[sm_index_not_train > -1] 
sig_all_arr = sm_index_not_train + n_tot_bkg_ev 

n_mix_combs = 8 
n_sam_bkg_ev = n_tot_bkg_ev/n_mix_combs
print n_sam_bkg_ev


if not os.path.exists(sample_path): os.mkdir(sample_path)

btagAlgo = "pfCombinedMVAV2BJetTags"
btag_wp = wps['CMVAv2_moriond']

# variables to check nearest-neightbour
nn_vars = ["thrustMayor","thrustMinor", "sumPz","invMass"]
nn_vars_v = vector("string")()
for v in nn_vars: nn_vars_v.push_back(v)

# to parse variables to the anlyzer
config = {#"eventInfo_branch_name" : "EventInfo",
          "jets_branch_name": "Jets",
          "dijets_branch_name": "DiJets",
          "dihiggs_branch_name": "DiHiggs",
          #"muons_branch_name" : "",
          #"electrons_branch_name" : "",
          #"met_branch_name" : "",
          "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "lumiFb" : intLumi_fb,
          "isMixed" : False,
          "ofile_update" : False,
         }

for s_n in trange(n_samples):

    bkg_sam_arr = bkg_rs.choice(bkg_all_arr, n_sam_bkg_ev,
                                replace=replace)
    sig_sam_arr = sig_rs.choice(sig_all_arr, n_sam_sig_ev,
                                replace=replace)

    ev_list = TEventList("TEventList")
    ev_list = array_to_list(bkg_sam_arr, ev_list)
    ev_list = array_to_list(sig_sam_arr, ev_list)

    tchain.SetEventList(ev_list)
    tch_hem.SetEventList(ev_list)

    config["isData"] = True 
    config["isSignal"] = False 

    json_str = json.dumps(config)

    # selector to do mixing
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(EventWriterOperator(alp.Event)(json_str, weights_v))
    selector.addOperator(ThrustFinderOperator(alp.Event)())
    selector.addOperator(HemisphereProducerOperator(alp.Event)())
    hem_mix_op = HemisphereMixerOperator(alp.Event)(tch_hem, btagAlgo, btag_wp[1], nn_vars_v, 11)
    selector.addOperator(hem_mix_op)
    selector.addOperator(MixedEventWriterOperator(alp.Event)(mixing_comb))

    process_options = "ofile={}/BTagCSVRun2016_bootstrap_{}_{}.root".format(sample_path, s_n, args.comb)
    print process_options
    tchain.Process(selector, process_options)

    del hem_mix_op 
    selector.ops_.clear()
    del selector
    del ev_list
