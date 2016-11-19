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
  #fCSaxis = CSaxis(dihiggs)
  #cosThetaStar = fCSaxis.Dot(diphoton_vect)
  cosThetaStar = diphoton.CosTheta()
  return cosThetaStar

 
def CosThetaStarh1(parton, higgs):
  boost_higgs = -higgs.BoostVector()
  parton.Boost(boost_higgs)
  cosThetaStarh1 = parton.CosTheta() #  
  return cosThetaStarh1;

def PtBalanceRest(jet1,jet2,H):
  #full = H+ HH
  boost_H = -H.BoostVector()
  jet1.Boost(boost_H)
  jet2.Boost(boost_H)
  diffpt = abs(jet1.Pt()-jet2.Pt())
  diffpt = jet1.DeltaR(jet2)
  return diffpt


##################
# read the histos tree and contruct the tree of the relevant variables 
path = "/lustre/cmswork/hh/alp_baseSelector/"
#def_noTrg/
files = []
filesout = []
files.append("def/TT")
filesout.append("full-TT")
#files.append("def_noTrg/TT")
#filesout.append("full-TT_noTrg")

files.append("def/HHTo4B_SM")
filesout.append("full-HHTo4B_SM")
for ifile in range(2,13) :
  files.append("def/HHTo4B_BM"+ifile)
  filesout.append("full-HHTo4B_BM"+ifile)
HT=["100to200","200to300","300to500","500to700","700to1000","1000to1500","1500to2000","2000toInf"]
for ifile in range(1,8) :
  print ifile," " ,HT[ifile]
  files.append("def_noTrg/QCD_HT"+HT[ifile]+"_BGenFilter")
  files.append("def_noTrg/QCD_bEnriched_HT"+HT[ifile])
  filesout.append("full-QCD_HT"+HT[ifile]+"_BGenFilter")
  filesout.append("full-QCD_bEnriched_HT"+HT[ifile])
for ifile in range(1,8) :
  files.append("def_noTrg/QCD_HT"+HT[ifile])
  files.append("def_noTrg/QCD_HT"+HT[ifile]+"_ext")
  filesout.append("full-QCD_HT"+HT[ifile])
  filesout.append("full-QCD_HT"+HT[ifile]+"_ext")
files.append("def/HHTo4B_BM8")
filesout.append("full-HHTo4B_BM8")
#filesout =["HHTo4B_SM","TT","TT_noTrg"]
# TT_noTrg have no evWeight

countttbar = 0
countttbarnoHLT = 0
countSM = 0
countQCDb = 0
countQCD = 0

#"""
# full 
normSM=0.164524939149
normttbar= 368.49224598
normttbarNoHLT=517.19175105
normQCDb=6863.0229617
normQCD=20379.258638
# """

"""
# LM
normSM=0.0289395151884
normttbar=118.04878782
normttbarNoHLT=202.761788166
normQCDb=2787.26018316
normQCD=8552.18719627
# """

"""
# HM
normSM=0.135585423961
normttbar=250.44345816
normttbarNoHLT=314.429962884
normQCDb=4075.76277854
normQCD=11827.0714417
# """

for ifile in range(1,len(files)) : # len(files)  
  #print ifile
  file=ROOT.TFile(path+files[ifile]+".root")
  tree=file.pair.Get("tree")
  nev = tree.GetEntries()

  mhh =  np.zeros(1, dtype=float)
  mh1 = np.zeros(1, dtype=float)
  mh2 = np.zeros(1, dtype=float)
  pth1 = np.zeros(1, dtype=float)
  pth2 = np.zeros(1, dtype=float)
  DRh1 = np.zeros(1, dtype=float)
  DRh2 = np.zeros(1, dtype=float)
  DRh2 = np.zeros(1, dtype=float)
  HHDeta = np.zeros(1, dtype=float)
  CSV4 = np.zeros(1, dtype=float)
  CSV3 = np.zeros(1, dtype=float)
  HHCost = np.zeros(1, dtype=float)
  H1Costbb = np.zeros(1, dtype=float)
  H2Costbb = np.zeros(1, dtype=float)

  H1Detabb = np.zeros(1, dtype=float)
  H2Detabb = np.zeros(1, dtype=float)
  weight = np.zeros(1, dtype=float)
  #ptH1D = np.zeros(1, dtype=float)
  #ptH2D = np.zeros(1, dtype=float)

  fileout=ROOT.TFile(filesout[ifile]+"-toBDT.root","recreate")
  treeout = TTree('treeout', 'treeout')
  treeout.Branch('mhh', mhh, 'mhh/D')
  treeout.Branch('mh1', mh1, 'mh1/D')
  treeout.Branch('mh2', mh2, 'mh2/D')
  treeout.Branch('HHCost', HHCost, 'HHCost/D')
  treeout.Branch('HHDeta', HHDeta, 'HHDeta/D')

  treeout.Branch('pth1', pth1, 'pth1/D')
  treeout.Branch('pth2', pth2, 'pth2/D')
  treeout.Branch('DRh1', DRh1, 'DRh1/D')
  treeout.Branch('DRh2', DRh2, 'DRh2/D')
  treeout.Branch('CSV4', CSV4, 'CSV4/D')

  treeout.Branch('H1Costbb', H1Costbb, 'H1Costbb/D')
  treeout.Branch('H2Costbb', H2Costbb, 'H2Costbb/D')
  treeout.Branch('H1Detabb', H1Detabb, 'H1Detabb/D')
  treeout.Branch('H2Detabb', H2Detabb, 'H2Detabb/D')
  treeout.Branch('CSV3', CSV3, 'CSV3/D')
  treeout.Branch('weight', weight, 'weight/D')
  #treeout.Branch('ptH1D', ptH1D, 'ptH1D/D')
  #treeout.Branch('ptH2D', ptH2D, 'ptH2D/D')

  # save also weights == to QCD later...
  h_genEvts = file.Get( 'h_genEvts' )
  h_genEvts.Write()
  nevGen = h_genEvts.GetBinContent(1) # num of genrated events
  h_w_XsBrEff = file.Get( 'h_w_XsBrEff' )
  h_w_XsBrEff.Write()
  #w_XsBrEff = h_w_XsBrEff.GetBinContent(0) # event weight = xsec*BR*genEff
  h_w_oneInvFb = file.Get( 'h_w_oneInvFb' )
  h_w_oneInvFb.Write()
  w_oneInvFb = h_w_oneInvFb.GetBinContent(1) # event weight = xsec*BR*genEff
  #print files[ifile]+" "+str( nev)+" "+str(nevGen)+" "+str(w_oneInvFb)
  counter=0
  #if ifile==16 : treeout.Fill()
  for iev in range(0,nev) :
    
    tree.GetEntry(iev)
    # Higgses ordered by mass by default
    # order the Higgses by CSV sum 
    if tree.Jets.at(0).CSV()+ tree.Jets.at(1).CSV() > tree.Jets.at(2).CSV()+ tree.Jets.at(3).CSV() : 
       jetOrder=[0,1,2,3]
       dijetOrder=[0,1]
    else : 
       jetOrder=[2,3,0,1]
       dijetOrder=[1,0]

    # order the Higgses by Pt to calculate pt discrimination
    if tree.DiJets.at(0).Pt() > tree.DiJets.at(1).Pt() : 
       dijetOrderpt=[0,1]
       jetOrderpt=[0,1,2,3]
    else : 
       jetOrderpt=[2,3,0,1]
       dijetOrderpt=[1,0]

    PH1 = ROOT.TLorentzVector()
    PH1.SetPxPyPzE(tree.DiJets.at(dijetOrder[0]).Px(),tree.DiJets.at(dijetOrder[0]).Py(),tree.DiJets.at(dijetOrder[0]).Pz(),tree.DiJets.at(dijetOrder[0]).E())
    PH1j1 = ROOT.TLorentzVector()
    PH1j1.SetPxPyPzE(tree.Jets.at(jetOrder[0]).p4_.Px(),tree.Jets.at(jetOrder[0]).p4_.Py(),tree.Jets.at(jetOrder[0]).p4_.Pz(),tree.Jets.at(jetOrder[0]).p4_.E())
    PH1j2 = ROOT.TLorentzVector()
    PH1j2.SetPxPyPzE(tree.Jets.at(jetOrder[1]).p4_.Px(),tree.Jets.at(jetOrder[1]).p4_.Py(),tree.Jets.at(jetOrder[1]).p4_.Pz(),tree.Jets.at(jetOrder[1]).p4_.E())

    PH2 = ROOT.TLorentzVector()
    PH2.SetPxPyPzE(tree.DiJets.at(dijetOrder[1]).Px(),tree.DiJets.at(dijetOrder[1]).Py(),tree.DiJets.at(dijetOrder[1]).Pz(),tree.DiJets.at(dijetOrder[1]).E())
    PH2j1 = ROOT.TLorentzVector()
    PH2j1.SetPxPyPzE(tree.Jets.at(jetOrder[2]).p4_.Px(),tree.Jets.at(jetOrder[2]).p4_.Py(),tree.Jets.at(jetOrder[2]).p4_.Pz(),tree.Jets.at(jetOrder[2]).p4_.E())
    PH2j2 = ROOT.TLorentzVector()
    PH2j2.SetPxPyPzE(tree.Jets.at(jetOrder[3]).p4_.Px(),tree.Jets.at(jetOrder[3]).p4_.Py(),tree.Jets.at(jetOrder[3]).p4_.Pz(),tree.Jets.at(jetOrder[3]).p4_.E())
    ##########################################################################
    PH1pt = ROOT.TLorentzVector()
    PH1pt.SetPxPyPzE(tree.DiJets.at(dijetOrderpt[0]).Px(),tree.DiJets.at(dijetOrderpt[0]).Py(),tree.DiJets.at(dijetOrderpt[0]).Pz(),tree.DiJets.at(dijetOrderpt[0]).E())
    PH2pt = ROOT.TLorentzVector()
    PH2pt.SetPxPyPzE(tree.DiJets.at(dijetOrderpt[1]).Px(),tree.DiJets.at(dijetOrderpt[1]).Py(),tree.DiJets.at(dijetOrderpt[1]).Pz(),tree.DiJets.at(dijetOrderpt[1]).E())

    PH1j1pt = ROOT.TLorentzVector()
    PH1j1pt.SetPxPyPzE(tree.Jets.at(jetOrderpt[0]).p4_.Px(),tree.Jets.at(jetOrderpt[0]).p4_.Py(),tree.Jets.at(jetOrderpt[0]).p4_.Pz(),tree.Jets.at(jetOrderpt[0]).p4_.E())
    PH1j2pt = ROOT.TLorentzVector()
    PH1j2pt.SetPxPyPzE(tree.Jets.at(jetOrderpt[1]).p4_.Px(),tree.Jets.at(jetOrderpt[1]).p4_.Py(),tree.Jets.at(jetOrderpt[1]).p4_.Pz(),tree.Jets.at(jetOrderpt[1]).p4_.E())
    PH2j1pt = ROOT.TLorentzVector()
    PH2j1pt.SetPxPyPzE(tree.Jets.at(jetOrderpt[2]).p4_.Px(),tree.Jets.at(jetOrderpt[2]).p4_.Py(),tree.Jets.at(jetOrderpt[2]).p4_.Pz(),tree.Jets.at(jetOrderpt[2]).p4_.E())
    PH2j2pt = ROOT.TLorentzVector()
    PH2j2pt.SetPxPyPzE(tree.Jets.at(jetOrderpt[3]).p4_.Px(),tree.Jets.at(jetOrderpt[3]).p4_.Py(),tree.Jets.at(jetOrderpt[3]).p4_.Pz(),tree.Jets.at(jetOrderpt[3]).p4_.E())

    PHH = ROOT.TLorentzVector()
    PHH = PH1 +PH2
    CSV= [ tree.Jets.at(0).CSV(), tree.Jets.at(1).CSV(), tree.Jets.at(2).CSV(), tree.Jets.at(3).CSV()]
    CSVordered = np.argsort(CSV)
    #print [ tree.Jets.at(CSVordered[0]).CSV(), tree.Jets.at(CSVordered[1]).CSV(), tree.Jets.at(CSVordered[2]).CSV(), tree.Jets.at(CSVordered[3]).CSV()]

    if PHH.M() > 250 :
    #if PHH.M() < 350 and PHH.M() > 250 : 
    #if  PHH.M() > 350 :
      counter+=1
      elif ifile == 0 :
        if counter==1 : print ifile, " ttbar ", filesout[ifile]," ",str(nev)
        weight[0]= (tree.evtWeight)*(w_oneInvFb)/normttbar
        countttbar+=(tree.evtWeight)*(w_oneInvFb)/normttbar # LM
      if ifile ==0 :
        if counter==1: print ifile," SM ", filesout[ifile]," ",str(nev)
        weight[0]= (tree.evtWeight)*(w_oneInvFb)/normSM
        countSM+=(tree.evtWeight)*(w_oneInvFb)/normSM # LM

      elif ifile == 2 :
        if counter==1: print ifile," ttbar no trigger ", filesout[ifile]," ",str(nev)
        weight[0]= (tree.evtWeight)*(w_oneInvFb)/normttbarNoHLT
        countttbarnoHLT+=(tree.evtWeight)*(w_oneInvFb)/normttbarNoHLT # LM
      elif ifile < 17 :
        if counter==1: print ifile," QCD-b ", filesout[ifile]," ",str(nev)
	weight[0]= (tree.evtWeight)*(w_oneInvFb)/normQCDb
        countQCDb+=(tree.evtWeight)*(w_oneInvFb)/normQCDb # LM
      else :
        if counter==1: print ifile," QCD ", filesout[ifile]," ",str(nev)
	weight[0]= (tree.evtWeight)*(w_oneInvFb)/normQCD
        countQCD+=(tree.evtWeight)*(w_oneInvFb)/normQCD # LM

      mhh[0] = PHH.M()
      mh1[0] = PH1pt.M()
      mh2[0] = PH2pt.M()
      pth1[0] = PH1pt.Pt()
      pth2[0] = PH2pt.Pt()
      DRh1[0] = PH1j1pt.DeltaR(PH1j2pt)
      DRh2[0] = PH2j1pt.DeltaR(PH2j2pt)

      HHDeta[0] = abs(PH1.Eta()-PH2.Eta())
      #Dphih12[0] = PH1.DeltaR(PH2) #abs(PH1.Phi()-PH2.Phi())
      CSV4[0] = tree.Jets.at(CSVordered[0]).CSV() #+ tree.Jets.at(2).CSV()+ tree.Jets.at(3).CSV()
      CSV3[0] =  tree.Jets.at(CSVordered[1]).CSV()
      HHCost[0] =  abs(CosThetaStar(PH1, PHH))
      #if tree.Jets.at(jetOrder[0]).CSV() > tree.Jets.at(jetOrder[1]).CSV() : 
      #if PH1j1.Pt() > PH1j1.Pt() : 
      if 1>0 : 
        H1Costbbc = abs(CosThetaStar(PH1j2pt, PH1pt))
      else : H1Costbbc = ab(CosThetaStar(PH1j2pt, PH1pt))
      #if tree.Jets.at(jetOrder[2]).CSV() > tree.Jets.at(jetOrder[3]).CSV() : 
      #if PH2j1.Pt() > PH2j1.Pt() :
      if 1>0 : 
        H2Costbbc = abs(CosThetaStar(PH2j2pt, PH2pt))
      else : H2Costbbc = abs(CosThetaStar(PH2j2pt, PH2pt))
      H1Costbb[0] = H1Costbbc  
      H2Costbb[0] = H2Costbbc
      H1Detabb[0] = abs(PH1j1pt.Eta()-PH1j2pt.Eta()) # abs(abs(CosThetaStar(PH1j1, PH1))-abs(CosThetaStar(PH1j2, PH1))) # 
      H2Detabb[0] = abs(PH2j1pt.Eta()-PH2j2pt.Eta()) # abs(abs(CosThetaStar(PH2j1, PH2))-abs(CosThetaStar(PH2j2, PH2))) #
      #ptH1D[0] = PtBalanceRest(PH1j1,PH1j2,PH1) #abs(CosThetaStar(PH1j1, PH1)-CosThetaStar(PH1j2, PH1))
      #ptH2D[0] = PtBalanceRest(PH2j1,PH2j2,PH2) #abs(CosThetaStar(PH2j1, PH2)-CosThetaStar(PH2j2, PH2))

      #if PHH.M() > 250 :
      treeout.Fill()
  print counter
  fileout.Write()
  fileout.Close()
print "done "
print "SM ",countSM
print "ttbar ", countttbar
print "ttbar, noHLT ",countttbarnoHLT 
print "QCD ",countQCD
print "QCDb ",countQCDb




