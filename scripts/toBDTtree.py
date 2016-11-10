#!/usr/bin/env python

# good old python modules
import json
import os
import importlib
from array import array
from glob import glob
import numpy as np
import os, sys, time,math
import shutil,subprocess

# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT, TTree
# custom ROOT classes 
from ROOT import alp
#import import_alp
#import ctypes
#libalp = ctypes.CDLL("../src/alp_objects_h.so")

import ctypes
my_test_lib = ctypes.cdll.LoadLibrary('../src/alp_objects_h.so')

#print '   *** Loading Alp libraries == to have jets CSV'        
#output = open('load.cc','w')     
#output.write('{.L ../src/alp_objects.h++;}')     
#output.close()     
#proc=subprocess.Popen(['root -l -q load.cc; '], shell=True,stdout=subprocess.PIPE)     
#out = proc.stdout.read()
#ROOT.gSystem.Load("../src/alp_objects.h++") # == to have the jets CSV
#include <Python.h>


def CSaxis(H):
  p1 = ROOT.TLorentzVector();
  p2 = ROOT.TLorentzVector();
  p1.SetPxPyPzE(0, 0,  6500, 6500);
  p2.SetPxPyPzE(0, 0,  -6500, 6500);
  boost_H = -H.BoostVector();
  p1.Boost(boost_H)
  p2.Boost(boost_H)
  p1v3 = p1.BoostVector().Unit(); 
  p2v3 = p2.BoostVector().Unit();
  CSaxisv3 = (p1v3 - p2v3).Unit();
  return CSaxisv3;

def CosThetaStar(diphoton, dihiggs):
  boost_H = -dihiggs.BoostVector()
  diphoton.Boost(boost_H)
  diphoton_vect = diphoton.Vect().Unit()
  fCSaxis = CSaxis(dihiggs)
  #cosThetaStar = diphoton.CosTheta()
  cosThetaStar = fCSaxis.Dot(diphoton_vect)
  return cosThetaStar

 
def CosThetaStarh1(parton, higgs):
  boost_higgs = -higgs.BoostVector()
  parton.Boost(boost_higgs)
  cosThetaStarh1 = parton.CosTheta() #  
  return cosThetaStarh1;

def PtBalanceRest(jet1,jet2,H):
  boost_H = -H.BoostVector()
  jet1.Boost(boost_H)
  jet2.Boost(boost_H)
  diffpt = abs(jet1.Pt()-jet2.Pt())
  return diffpt


##################
# read the histos tree and contruct the tree of the relevant variables 
path = "/lustre/cmswork/hh/alp_baseSelector/MC"
files =["_def/HHTo4B_SM","_def/TT","_noTrg/TT"] #
filesout =["HHTo4B_SM","TT","TT_noTrg"]

for ifile in range(0,len(files)) : # len(files)  
  file=ROOT.TFile(path+files[ifile]+".root")
  tree=file.pair.Get("tree")
  nev = tree.GetEntries()

  toBDT_mhh =  np.zeros(1, dtype=float)
  mh1 = np.zeros(1, dtype=float)
  mh2 = np.zeros(1, dtype=float)
  toBDT_pth1 = np.zeros(1, dtype=float)
  toBDT_pth2 = np.zeros(1, dtype=float)
  toBDT_DRh1 = np.zeros(1, dtype=float)
  toBDT_DRh2 = np.zeros(1, dtype=float)
  toBDT_DRh2 = np.zeros(1, dtype=float)
  toBDT_Detah12 = np.zeros(1, dtype=float)
  toBDT_Dphih12 = np.zeros(1, dtype=float)
  toBDT_CSVsum = np.zeros(1, dtype=float)
  toBDT_CSV3 = np.zeros(1, dtype=float)
  toBDT_CostHH = np.zeros(1, dtype=float)
  toBDT_CostH1 = np.zeros(1, dtype=float)
  toBDT_CostH2 = np.zeros(1, dtype=float)

  toBDT_CostH1diff = np.zeros(1, dtype=float)
  toBDT_CostH2diff = np.zeros(1, dtype=float)

  print files[ifile]+" "+str( nev)
  fileout=ROOT.TFile(filesout[ifile]+"-toBDT.root","recreate")
  treeout = TTree('treeout', 'treeout')
  treeout.Branch('toBDT_mhh', toBDT_mhh, 'toBDT_mhh/D')
  treeout.Branch('mh1', mh1, 'toBDT_mh1/D')
  treeout.Branch('mh2', mh2, 'toBDT_mh2/D')
  treeout.Branch('toBDT_pth1', toBDT_pth1, 'toBDT_pth1/D')
  treeout.Branch('toBDT_prh2', toBDT_pth2, 'toBDT_pth2/D')
  treeout.Branch('toBDT_DRh1', toBDT_DRh1, 'toBDT_DRh1/D')
  treeout.Branch('toBDT_DRh2', toBDT_DRh2, 'toBDT_DRh2/D')
  treeout.Branch('toBDT_Detah12', toBDT_Detah12, 'toBDT_Detah12/D')
  treeout.Branch('toBDT_Dphih12', toBDT_Dphih12, 'toBDT_Dphih12/D')
  treeout.Branch('toBDT_CSVsum', toBDT_CSVsum, 'toBDT_CSVsum/D')
  treeout.Branch('toBDT_CSV3', toBDT_CSV3, 'toBDT_CSV3/D')
  treeout.Branch('toBDT_CostHH', toBDT_CostHH, 'toBDT_CostHH/D')
  treeout.Branch('toBDT_CostH1', toBDT_CostH1, 'toBDT_CostH1/D')
  treeout.Branch('toBDT_CostH2', toBDT_CostH2, 'toBDT_CostH2/D')

  treeout.Branch('toBDT_CostH1diff', toBDT_CostH1diff, 'toBDT_CostH1diff/D')
  treeout.Branch('toBDT_CostH2diff', toBDT_CostH2diff, 'toBDT_CostH2diff/D')

  # save also weights == to QCD later...
  h_genEvts = file.Get( 'h_genEvts' )
  nevGen = h_genEvts.GetBinContent(0) # num of genrated events
  h_w_XsBrEff = file.Get( 'h_w_XsBrEff' )
  w_XsBrEff = h_w_XsBrEff.GetBinContent(0) # event weight = xsec*BR*genEff
  h_w_oneInvFb = file.Get( 'h_w_oneInvFb' )
  w_oneInvFb = h_w_oneInvFb.GetBinContent(0) # event weight = xsec*BR*genEff

  for iev in range(0,nev) :
    tree.GetEntry(iev)

    # order the Higgses by CSV sum 
    if tree.Jets.at(0).CSV()+ tree.Jets.at(1).CSV() > tree.Jets.at(2).CSV()+ tree.Jets.at(3).CSV() : 
       dijetOrder=[0,1,2,3]
       dijetOrderpt=[0,1]
    else : 
       dijetOrder=[2,3,0,1]
       dijetOrderpt=[1,0]

    # order the Higgses by Pt to calculate pt discrimination
    #if tree.DiJets.at(0).Pt() > tree.DiJets.at(1).Pt() : 
    #   dijetOrderpt=[0,1]
    #   dijetOrder=[0,1,2,3]
    #else : 
    #    dijetOrder=[2,3,0,1]
    #    dijetOrderpt=[1,0]


    PH1 = ROOT.TLorentzVector()
    PH1.SetPxPyPzE(tree.DiJets.at(dijetOrderpt[0]).Px(),tree.DiJets.at(dijetOrderpt[0]).Py(),tree.DiJets.at(dijetOrderpt[0]).Pz(),tree.DiJets.at(dijetOrderpt[0]).E())
    PH2 = ROOT.TLorentzVector()
    PH2.SetPxPyPzE(tree.DiJets.at(dijetOrderpt[1]).Px(),tree.DiJets.at(dijetOrderpt[1]).Py(),tree.DiJets.at(dijetOrderpt[1]).Pz(),tree.DiJets.at(dijetOrderpt[1]).E())

    PH1j1 = ROOT.TLorentzVector()
    PH1j1.SetPxPyPzE(tree.Jets.at(dijetOrder[0]).p4_.Px(),tree.Jets.at(dijetOrder[0]).p4_.Py(),tree.Jets.at(dijetOrder[0]).p4_.Pz(),tree.Jets.at(dijetOrder[0]).p4_.E())
    PH1j2 = ROOT.TLorentzVector()
    PH1j2.SetPxPyPzE(tree.Jets.at(dijetOrder[1]).p4_.Px(),tree.Jets.at(dijetOrder[1]).p4_.Py(),tree.Jets.at(dijetOrder[1]).p4_.Pz(),tree.Jets.at(1).p4_.E())

    PH2j1 = ROOT.TLorentzVector()
    PH2j1.SetPxPyPzE(tree.Jets.at(dijetOrder[2]).p4_.Px(),tree.Jets.at(dijetOrder[2]).p4_.Py(),tree.Jets.at(dijetOrder[2]).p4_.Pz(),tree.Jets.at(dijetOrder[2]).p4_.E())
    PH2j2 = ROOT.TLorentzVector()
    PH2j2.SetPxPyPzE(tree.Jets.at(dijetOrder[3]).p4_.Px(),tree.Jets.at(dijetOrder[3]).p4_.Py(),tree.Jets.at(dijetOrder[3]).p4_.Pz(),tree.Jets.at(3).p4_.E())
    
    PHH = ROOT.TLorentzVector()
    PHH = PH1 +PH2

    CSV= [ tree.Jets.at(0).CSV(), tree.Jets.at(1).CSV(), tree.Jets.at(2).CSV(), tree.Jets.at(3).CSV()]
    CSVordered = np.argsort(CSV)
    #print [ tree.Jets.at(CSVordered[0]).CSV(), tree.Jets.at(CSVordered[1]).CSV(), tree.Jets.at(CSVordered[2]).CSV(), tree.Jets.at(CSVordered[3]).CSV()]
    #print tree.Jets.at(0).CSV()
    #
    toBDT_mhh[0] = PHH.M()
    mh1[0] = PH1.M()
    mh2[0] = PH2.M()
    toBDT_pth1[0] = PH1.Pt()
    toBDT_pth2[0] = PH2.Pt()
    toBDT_DRh1[0] = PH1j1.DeltaR(PH1j2)
    toBDT_DRh2[0] = PH2j1.DeltaR(PH2j2)
    toBDT_Detah12[0] = abs(PH1.Eta()-PH2.Eta())
    toBDT_Dphih12[0] = abs(PH1.Phi()-PH2.Phi())
    toBDT_CSVsum[0] = tree.Jets.at(0).CSV()+ tree.Jets.at(1).CSV()+ tree.Jets.at(2).CSV()+ tree.Jets.at(3).CSV()
    toBDT_CSV3[0] =  tree.Jets.at(CSVordered[1]).CSV()
    toBDT_CostHH[0] =  CosThetaStar(PH1, PHH)
    if PH1j1.Pt() > PH1j2.Pt() : CostH1 = CosThetaStar(PH1j1, PH1)
    else : CostH1 = CosThetaStar(PH1j2, PH1)
    if PH2j1.Pt() > PH2j2.Pt() : CostH2 = CosThetaStar(PH2j1, PH2)
    else : CostH2 = CosThetaStar(PH2j2, PH2)
    toBDT_CostH1[0] = CostH1  
    toBDT_CostH2[0] = CostH2
    toBDT_CostH1diff[0] =  abs(CosThetaStar(PH1j1, PH1)-CosThetaStar(PH1j2, PH1))
    toBDT_CostH2diff[0] =  abs(CosThetaStar(PH2j1, PH2)-CosThetaStar(PH2j2, PH2))
    treeout.Fill()

  fileout.Write()
  fileout.Close()
print "done "





