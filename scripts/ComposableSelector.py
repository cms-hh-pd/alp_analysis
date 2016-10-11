#!/usr/bin/env python 

import json
# ROOT imports
from ROOT import TChain
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, JetFilterOperator, BTagFilterOperator, JetPairingOperator, DiJetPlotterOperator
from ROOT import BaseOperator, FolderOperator, EventWriterOperator


config = {"jets_branch_name": "Jets",
          "hlt_names":[]}

selector = ComposableSelector(alp.Event)(0, json.dumps(config))
selector.addOperator(BaseOperator(alp.Event)())
selector.addOperator(CounterOperator(alp.Event)())
selector.addOperator(JetFilterOperator(alp.Event)(2.5, 30., 4))
selector.addOperator(CounterOperator(alp.Event)())
selector.addOperator(BTagFilterOperator(alp.Event)("pfCombinedInclusiveSecondaryVertexV2BJetTags", 0.800, 4))
selector.addOperator(CounterOperator(alp.Event)())
selector.addOperator(FolderOperator(alp.Event)("empty_one"))
selector.addOperator(JetPairingOperator(alp.Event)(4))
selector.addOperator(FolderOperator(alp.Event)("4CSVM"))
selector.addOperator(DiJetPlotterOperator(alp.Event)())
selector.addOperator(CounterOperator(alp.Event)())
selector.addOperator(EventWriterOperator(alp.Event)())
selector.addOperator(FolderOperator(alp.Event)("empty_two"))

tchain = TChain("ntuple/tree")
tchain.Add("/lustre/cmswork/hh/alpha_ntuples/v0_20161004/GluGluToHHTo4B_node_SM_13TeV-madgraph_v14-v1/0000/output.root")

tchain.Process(selector, "", 10000)

