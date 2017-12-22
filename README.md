#alp_analysis

Repo to create skimmed ntuples from the output of ALPHA framework.
Main features: trigger, kinematics, btagging selection; weights computation/handling; plot creation; higher level variables creation.

## CODE STRUCTURE
alp_analysis inherits classes from ALPHA framework.
The latter has to be installed before, together with a CMSSW release.
Execution from python scripts which call operators defined in interface folder.

## TO DEBUG:
Look at issue on GitHub and use this chat for discuss about the code:
[![Join the chat at https://gitter.im/cms-hh-pd/alp_analysis](https://badges.gitter.im/cms-hh-pd/alp_analysis.svg)](https://gitter.im/cms-hh-pd/alp_analysis?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## TO INSTALL:
- Prerequisites
git account, git environment set, CERN account.

- Git instructions
    0. In your working area, first set up the CMSSW release:
        ```
        cmsrel CMSSW_8_0_12

        cd CMSSW_8_0_12/src/

        cmsenv

        git cms-init
        ```
    1. Install packages needed by ALPHA:
        see README from ALPHA repo [https://github.com/cms-hh-pd/ALPHA#alpha]

    2. Clone ALPHA and setup it:
        see README from ALPHA repo [https://github.com/cms-hh-pd/ALPHA#alpha]
        NOTE: clone it from cms-hh-pd repo:
            ```bash
            git clone git@github.com:cms-hh-pd/ALPHA.git
            ```
    3. Clone the alp_analysis git repository:
        ```bash

        cd $CMSSW_BASE/src/Analysis

        git clone git@github.com:cms-hh-pd/alp_analysis.git
        ```

## TO RUN:
Compile the code:
```bash
cd $CMSSW_BASE/src/
scram b -j 8
```
and run it:
```bash
cd $CMSSW_BASE/src/Analysis/alp_analysis
python scripts/Selector.py
```

If you do not have ALPHA compiled do: 

cd Analysis/alp_analysis/src/
root -l
> .L ../src/alp_objects.h++

## SCRIPT DESCRIPTION:

- #### BaselineSelector:
  
   to apply object/event selection. it has option to get antitag CR and to run over mixed events. event tree and hemisphere tree are saved by default

   python scripts/BaselineSelector.py -s signals -o def_cmva -i v2_20170606 (-a -m)

- #### MixingSelector:

   to create mixed events (baseline selector needs to be run after, to get standard ntuple structure). !!remember to use -a option to run in antitag CR!!

   python scripts/MixingSelector.py -s Data -i def_cmva --comb appl (-a)

- #### ClfSelector:

   to select event in a specif range of the classifier. !!additional sample needed with classifier, run columns2tree from hh2bbbb_limit before!!

   python scripts/ClfSelector.py -s Data_  -i 20171205 -o test


- #### TrgEffStudies:

   to get event selection for trigger efficiency studies.

- #### MCTruthSelector.py:

   to select only jets matched with gen

- #### TriggerSelector:

   to apply trigger and get plots.

- #### NoCutSelector.py:

   simple processing of the input data. No selection/object creation applied.

- #### comp_boost:

   to count fraction of common events between two samples (for comparison with boosted analysis)

- #### tkTDRSelector:

   to apply default selection to ntuple with different pu (for tracker tdr studies)

- #### ttHSelector:

   to apply a baseline selection for ttH searches. output is a 'plain tree' with no structures.

- #### AddPlots:

   to add plots (jets, dijets, dihiggs) on top of the input file

- #### GetPlainTree:

   to get simple tree with one variable per branch. readable with a simple ROOT macro - no classes needed. Useful for students.

- #### ReWeighting.py:

   to re-weight input file *not maintained*

- #### ToyDatasetCreator:

   to create a pseudo-data with signal injected. *not maintained*

- #### HistFromPangea.py:

   to get histogram comparison - pangea vs different benchmarks *not maintained*

- #### DiHiggsSelector:

   to test different higgs mass selection *not maintained*

- #### ComposableSelector:

   bare example of how to use operators.

## INPUT FOLDERS FROM ALPHA_NTUPLES:

- v2_20170222-trg -> TT

- v2_20170405 -> ttHbb

- v2_20170222 -> Data 

- v2_20170606 -> signals
