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

massup=3000.
massdo=0.
binMhh="baseline"
#binMhh="full"
#binMhh="LM"
#binMhh="HM"
##################
# read the histos tree and contruct the tree of the relevant variables 
#path = "/lustre/cmswork/hh/alp_baseSelector/"
path = "/afs/cern.ch/work/a/acarvalh/public/toHH4b/alp_baseSelector/"

#def_noTrg/
files = []
filesout = []
files.append("def/TT")
filesout.append(binMhh+"-TT")
files.append("def_noTrg/TT")
filesout.append(binMhh+"-TT_noTrg")


files.append("def/HHTo4B_SM")
filesout.append(binMhh+"-HHTo4B_SM")
for ifile in range(2,13) : # the 13 is missing
  files.append("def/HHTo4B_BM"+str(ifile))
  filesout.append(binMhh+"-HHTo4B_BM"+str(ifile))

files.append("def_noTrg/HHTo4B_SM")
filesout.append(binMhh+"-HHTo4B_SM_noTrg")
for ifile in range(2,13) :
  files.append("def_noTrg/HHTo4B_BM"+str(ifile))
  filesout.append(binMhh+"-HHTo4B_BM"+str(ifile)+"_noTrg")

HT=["100to200","200to300","300to500","500to700","700to1000","1000to1500","1500to2000","2000toInf"]
for ifile in range(1,8) :
  files.append("def_noTrg/QCD_HT"+HT[ifile])
  files.append("def_noTrg/QCD_HT"+HT[ifile]+"_ext")
  filesout.append(binMhh+"-QCD_HT"+HT[ifile])
  filesout.append(binMhh+"-QCD_HT"+HT[ifile]+"_ext")

# mixed _noTrg_mixed/
files.append("def_noTrg_mixed/QCD_HT200to500")
files.append("def_noTrg_mixed/QCD_HT500toInf")

filesout.append(binMhh+"-Mixed-QCDHT200to500_noTrg")
filesout.append(binMhh+"-Mixed-QCDHT500toInf_noTrg")

# data
#files.append("def_mixed/BTagCSVRun2016B-v1")
files.append("def_mixed/BTagCSVRun2016B-v2")
files.append("def_mixed/BTagCSVRun2016C-v2")
files.append("def_mixed/BTagCSVRun2016D-v2")

#filesout.append(binMhh+"-Mixed-BTagCSVRun2016B-v1")
filesout.append(binMhh+"-Mixed-BTagCSVRun2016B-v2")
filesout.append(binMhh+"-Mixed-BTagCSVRun2016C-v2")
filesout.append(binMhh+"-Mixed-BTagCSVRun2016D-v2")

#files.append("def/BTagCSVRun2016B-v1")
files.append("def/BTagCSVRun2016B-v2")
files.append("def/BTagCSVRun2016C-v2")
files.append("def/BTagCSVRun2016D-v2")

#filesout.append(binMhh+"-Plain-BTagCSVRun2016B-v1")
filesout.append(binMhh+"-Plain-BTagCSVRun2016B-v2")
filesout.append(binMhh+"-Plain-BTagCSVRun2016C-v2")
filesout.append(binMhh+"-Plain-BTagCSVRun2016D-v2")

"""
for ifile in range(1,8) :
  print ifile," " ,HT[ifile]
  files.append("def_noTrg/QCD_HT"+HT[ifile]+"_BGenFilter")
  files.append("def_noTrg/QCD_bEnriched_HT"+HT[ifile])
  filesout.append(binMhh+"-QCD_HT"+HT[ifile]+"_BGenFilter")
  filesout.append(binMhh+"-QCD_bEnriched_HT"+HT[ifile])
"""
#filesout =["HHTo4B_SM","TT","TT_noTrg"]
# TT_noTrg have no evWeight


CXplainQCD=2099983.14
CXTT=831.76
QCDto1fb=CXplainQCD/(CXplainQCD)
TTto1fb=CXTT/(CXplainQCD)
mixCX=[2059700,40283.14]
mixN=[1194,10100]

countSig=np.zeros((12)) 
countSigNoTr=np.zeros((12)) 

countttbar = 0
countttbarNoHLT = 0
countQCDb = 0
countQCD = 0
countQCDmixL = 0
countQCDmixH = 0
countdata=0
countdatamix=0

if binMhh=="baseline" :
  normSig= [  0.30445146 ,  8.08541789 ,  9.07503515  , 7.87640546  , 5.54326759 , 9.07453435  , 8.89697223  , 4.99948358 ,  6.35276001   ,7.22011991 , 7.86669971 , 10.07471099]
  #np.ones((12)) 
  normSigNoTr=[  0.39820884 , 11.45137869 , 11.73580169 , 11.05149414  , 9.95457663, 11.77125913 , 11.75794197,   9.89908847 , 10.58382588 , 10.83794821,11.1325214  , 12.18258459]
  #[ 6.41204264 , 6.53346172 , 6.13727502 , 5.55538704 , 6.49343605 , 6.56458484 , 5.52130693 , 5.87039014 , 5.9900769 , 6.17855073 , 6.74273375 , 0.21860946]
  normdata= 69047 #4318 #69036.0   
  normdatamix= 69047# 4318 #69047
  normttbar= 401.265999365
  normttbarNoHLT=597.248083582
  normQCDb=1.0
  normQCD=6028.12228652 #24536.7345755
  normQCDmix=1.0
if binMhh=="full" :
  normttbar= 368.49224598
  normttbarNoHLT=517.19175105
  normQCDb=6863.0229617
  normQCD=20379.258638
if binMhh=="LM" :
  normSig=np.ones((12)) 
  normSigNoTr=np.ones((12))
  normttbar=118.04878782
  normttbarNoHLT=202.761788166
  normQCDb=2787.26018316
  normQCD=8552.18719627
if binMhh=="HM" : 
  normSig=np.ones((12)) 
  normSigNoTr=np.ones((12))
  normttbar=250.44345816
  normttbarNoHLT=314.429962884
  normQCDb=4075.76277854
  normQCD=11827.0714417

for ifile in range(0,len(files)) : # len(files)  
  #print ifile
  file=ROOT.TFile(path+files[ifile]+".root")
  tree=file.pair.Get("tree")
  nev = tree.GetEntries()

  mhh =  np.zeros(1, dtype=float)
  mX =  np.zeros(1, dtype=float)
  HHpt =  np.zeros(1, dtype=float)
  HHetaAverage =  np.zeros(1, dtype=float)

  mh1 = np.zeros(1, dtype=float)
  mh2 = np.zeros(1, dtype=float)
  pth1 = np.zeros(1, dtype=float)
  pth2 = np.zeros(1, dtype=float)
  DRh1 = np.zeros(1, dtype=float)
  DRh2 = np.zeros(1, dtype=float)
  DRh2 = np.zeros(1, dtype=float)
  HHDeta = np.zeros(1, dtype=float)
  HHDphi = np.zeros(1, dtype=float)

  CSV4 = np.zeros(1, dtype=float)
  CSV3 = np.zeros(1, dtype=float)

  HHCost = np.zeros(1, dtype=float)
  H1Costbb = np.zeros(1, dtype=float)
  H2Costbb = np.zeros(1, dtype=float)

  H1Detabb = np.zeros(1, dtype=float)
  H2Detabb = np.zeros(1, dtype=float)

  H1Dphibb = np.zeros(1, dtype=float)
  H2Dphibb = np.zeros(1, dtype=float)

  weight = np.zeros(1, dtype=float)
  weight1P = np.zeros(1, dtype=float)
  weight1M = np.zeros(1, dtype=float)

  jetpt1 = np.zeros(1, dtype=float)
  jetpt2 = np.zeros(1, dtype=float)
  jetpt3 = np.zeros(1, dtype=float)
  jetpt4 = np.zeros(1, dtype=float)
  #jetpt5 = np.zeros(1, dtype=float)

  jeteta1 = np.zeros(1, dtype=float)
  jeteta2 = np.zeros(1, dtype=float)
  jeteta3 = np.zeros(1, dtype=float)
  jeteta4 = np.zeros(1, dtype=float)
  #jeteta5 = np.zeros(1, dtype=float)

  #jetcsv5 = np.zeros(1, dtype=float)
  jetN = np.zeros(1, dtype=float)
  jetHTrest = np.zeros(1, dtype=float)
  jetHTfull = np.zeros(1, dtype=float)

  fileout=ROOT.TFile("/afs/cern.ch/work/a/acarvalh/public/toHH4b/to_BDT/"+filesout[ifile]+"-toBDT.root","recreate")
  treeout = TTree('treeout', 'treeout')
  treeout.Branch('mhh', mhh, 'mhh/D')
  treeout.Branch('mX', mX, 'mX/D')
  treeout.Branch('HHpt', HHpt, 'HHpt/D')
  treeout.Branch('HHetaAverage', HHetaAverage, 'HHetaAverage/D')

  treeout.Branch('mh1', mh1, 'mh1/D')
  treeout.Branch('mh2', mh2, 'mh2/D')
  treeout.Branch('HHCost', HHCost, 'HHCost/D')
  treeout.Branch('HHDeta', HHDeta, 'HHDeta/D')
  treeout.Branch('HHDphi', HHDphi, 'HHDphi/D')

  treeout.Branch('pth1', pth1, 'pth1/D')
  treeout.Branch('pth2', pth2, 'pth2/D')
  treeout.Branch('DRh1', DRh1, 'DRh1/D')
  treeout.Branch('DRh2', DRh2, 'DRh2/D')
  treeout.Branch('H1Costbb', H1Costbb, 'H1Costbb/D')
  treeout.Branch('H2Costbb', H2Costbb, 'H2Costbb/D')
  treeout.Branch('H1Detabb', H1Detabb, 'H1Detabb/D')
  treeout.Branch('H2Detabb', H2Detabb, 'H2Detabb/D')
  treeout.Branch('H1Dphibb', H1Dphibb, 'H1Dphibb/D')
  treeout.Branch('H2Dphibb', H2Dphibb, 'H2Dphibb/D')

  treeout.Branch('CSV3', CSV3, 'CSV3/D')
  treeout.Branch('CSV4', CSV4, 'CSV4/D')

  treeout.Branch('weight', weight, 'weight/D')
  treeout.Branch('weight1P', weight1P, 'weight1P/D')
  treeout.Branch('weight1M', weight1M, 'weight1M/D')

  treeout.Branch('jetpt1', jetpt1, 'jetpt1/D')
  treeout.Branch('jetpt2', jetpt2, 'jetpt2/D')
  treeout.Branch('jetpt3', jetpt3, 'jetpt3/D')
  treeout.Branch('jetpt4', jetpt4, 'jetpt4/D')
  #treeout.Branch('jetpt5', jetpt5, 'jetpt5/D')

  treeout.Branch('jeteta1', jeteta1, 'jeteta1/D')
  treeout.Branch('jeteta2', jeteta2, 'jeteta2/D')
  treeout.Branch('jeteta3', jeteta3, 'jeteta3/D')
  treeout.Branch('jeteta4', jeteta4, 'jeteta4/D')
  #treeout.Branch('jeteta5', jeteta5, 'jeteta5/D')

  #treeout.Branch('jetcsv5', jetcsv5, 'jetcsv5/D')
  treeout.Branch('jetN', jetN, 'jetN/D')
  treeout.Branch('jetHTrest', jetHTrest, 'jetHTrest/D')
  treeout.Branch('jetHTfull', jetHTfull, 'jetHTfull/D')

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
    njets=tree.Jets.size()
    # Higgses ordered by mass by default
    # order the Higgses by CSV sum 
    if 1>0 : # tree.Jets.at(0).CSV()+ tree.Jets.at(1).CSV() > tree.Jets.at(2).CSV()+ tree.Jets.at(3).CSV() : 
       jetOrder=[0,1,2,3]
       dijetOrder=[0,1]
    else : 
       jetOrder=[2,3,0,1]
       dijetOrder=[1,0]
    # order the Higgses by Pt to calculate pt discrimination
    if  1>0 : # tree.DiJets.at(0).Pt() > tree.DiJets.at(1).Pt() : 
       dijetOrderpt=[0,1]
       jetOrderpt=[0,1,2,3]
    else : 
       jetOrderpt=[2,3,0,1]
       dijetOrderpt=[1,0]
    # order jets by pt


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

    PT= [ tree.Jets.at(0).p4_.Pt(), tree.Jets.at(1).p4_.Pt(), tree.Jets.at(2).p4_.Pt(), tree.Jets.at(3).p4_.Pt()]
    PTordered = np.argsort(PT)
    #print [ tree.Jets.at(CSVordered[0]).CSV(), tree.Jets.at(CSVordered[1]).CSV(), tree.Jets.at(CSVordered[2]).CSV(), tree.Jets.at(CSVordered[3]).CSV()]


    if PHH.M() < massup and PHH.M() > massdo : 
      counter+=1
      if ifile == 0 :
        if counter==1 : print ifile, " ttbar ", filesout[ifile]," ",str(nev)
        weight[0]= (tree.evtWeight)*(w_oneInvFb)/normttbar
        weight1P[0]= 1.1*(tree.evtWeight)*(w_oneInvFb)/normttbar
        weight1M[0]= 0.9*(tree.evtWeight)*(w_oneInvFb)/normttbar
        countttbar+=(tree.evtWeight)*(w_oneInvFb)/normttbar 
      if ifile == 1 :
        if counter==1 : print ifile, " ttbar noHLT", filesout[ifile]," ",str(nev)
        #weight[0]= (tree.evtWeight)*(w_oneInvFb)/normttbarNoHLT
        weight[0]= (w_oneInvFb)/normttbarNoHLT
        weight1P[0]= 1.1*(tree.evtWeight)*(w_oneInvFb)/normttbarNoHLT
        weight1M[0]= 0.9*(tree.evtWeight)*(w_oneInvFb)/normttbarNoHLT
        countttbarNoHLT+=(w_oneInvFb)/normttbarNoHLT 
      elif ifile >1 and ifile < 14 :
        if counter==1: print ifile," Sig ",str(ifile-2)," ", filesout[ifile]," ",str(nev)
        #weight[0]= (tree.evtWeight)*(w_oneInvFb)/normSig[ifile-2]
        weight[0]= (w_oneInvFb)/normSig[ifile-2]
        weight1P[0]= 1.1*(tree.evtWeight)*(w_oneInvFb)/normSig[ifile-2]
        weight1M[0]= 0.9*(tree.evtWeight)*(w_oneInvFb)/normSig[ifile-2]
        countSig[ifile-2]+=(w_oneInvFb)/normSig[ifile-2]
      elif ifile >13 and ifile < 26 :
        if counter==1: print ifile," Sig NoTr",str(ifile-2-12)," ", filesout[ifile]," ",str(nev)
        #weight[0]= (tree.evtWeight)*(w_oneInvFb)/normSigNoTr[ifile-2-12]
        weight[0]= (w_oneInvFb)/normSigNoTr[ifile-2-12]
        weight1P[0]= 1.1*(tree.evtWeight)*(w_oneInvFb)/normSigNoTr[ifile-2-12]
        weight1M[0]= 0.9*(tree.evtWeight)*(w_oneInvFb)/normSigNoTr[ifile-2-12]
        countSigNoTr[ifile-2-12]+=(w_oneInvFb)/normSigNoTr[ifile-2-12]
      elif ifile >25 and ifile < 40 :
        if counter==1: print ifile," QCD ", filesout[ifile]," ",str(nev)
	#weight[0]= (tree.evtWeight)*(w_oneInvFb)/normQCD
	weight[0]= (w_oneInvFb)/normQCD
        weight1P[0]= 1.1*QCDto1fb*(tree.evtWeight)*(w_oneInvFb)/normQCD
        weight1M[0]= 0.9*QCDto1fb*(tree.evtWeight)*(w_oneInvFb)/normQCD
        if ifile >29 : countQCD+=(w_oneInvFb)/normQCD 
      elif ifile ==40 :
        if counter==1: print ifile," QCD mix", filesout[ifile]," ",str(nev)
	weight[0]= 1.0/1194.
        weight1P[0]= 1.1*(tree.evtWeight)/11294.
        weight1M[0]= 0.9*(tree.evtWeight)/11294.
        countQCDmixL+=1.0/1194.
      elif ifile ==41 :
        if counter==1: print ifile," QCD mix", filesout[ifile]," ",str(nev)
	weight[0]= 1.0/10100.
        weight1P[0]= 1.1*QCDto1fb*(tree.evtWeight)/1194.
        weight1M[0]= 0.9*QCDto1fb*(tree.evtWeight)/1194.
        countQCDmixH+=1.0/10100 
      elif ifile < 45 :
        if counter==1: print ifile," data mix", filesout[ifile]," ",str(nev)
	weight[0]= 1.0/normdatamix
        weight1P[0]= 1.1
        weight1M[0]= 0.9
        countdatamix+=1.0/normdatamix
      elif ifile < 48 :
        if counter==1: print ifile," data ", filesout[ifile]," ",str(nev)
	weight[0]= 1.0/normdata
        weight1P[0]= 1.1
        weight1M[0]= 0.9
        countdata+=1.0/normdata
 
      """
      elif  ifile >25 and ifile < 26 :
        if counter==1: print ifile," QCD-b ", filesout[ifile]," ",str(nev)
	weight[0]= (tree.evtWeight)*(w_oneInvFb)/normQCDb
        countQCDb+=(tree.evtWeight)*(w_oneInvFb)/normQCDb # LM
      """

      """
      elif ifile == 2 :
        if counter==1: print ifile," ttbar no trigger ", filesout[ifile]," ",str(nev)
        weight[0]= (tree.evtWeight)*(w_oneInvFb)/normttbarNoHLT
        countttbarnoHLT+=(tree.evtWeight)*(w_oneInvFb)/normttbarNoHLT 
      """
      mhh[0] = PHH.M()
      mX[0] =  PHH.M() - PH1pt.M() - PH2pt.M() + 250. 
      HHpt[0] =  PHH.Pt()
      HHetaAverage[0] = (PH1.Eta()+PH2.Eta())/2. 
      mh1[0] = PH1pt.M()
      mh2[0] = PH2pt.M()
      pth1[0] = PH1pt.Pt()
      pth2[0] = PH2pt.Pt()
      DRh1[0] = PH1j1pt.DeltaR(PH1j2pt)
      DRh2[0] = PH2j1pt.DeltaR(PH2j2pt)

      HHDeta[0] = abs(PH1.Eta()-PH2.Eta())
      HHDphi[0] = abs(PH1.DeltaPhi(PH2))
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
      H1Dphibb[0] = abs(PH1j1pt.DeltaPhi(PH1j2pt)) # abs(abs(CosThetaStar(PH1j1, PH1))-abs(CosThetaStar(PH1j2, PH1))) # 
      H2Dphibb[0] = abs(PH2j1pt.DeltaPhi(PH2j2pt)) # abs(abs(CosThetaStar(PH2j1, PH2))-abs(CosThetaStar(PH2j2, PH2))) #

      jetpt1[0] = tree.Jets.at(PTordered[3]).p4_.Pt()
      jetpt2[0] = tree.Jets.at(PTordered[2]).p4_.Pt()
      jetpt3[0] = tree.Jets.at(PTordered[1]).p4_.Pt()
      jetpt4[0] = tree.Jets.at(PTordered[0]).p4_.Pt()

      jeteta1[0] = abs(tree.Jets.at(PTordered[3]).p4_.Eta() )
      jeteta2[0] = abs(tree.Jets.at(PTordered[2]).p4_.Eta())
      jeteta3[0] = abs(tree.Jets.at(PTordered[1]).p4_.Eta())
      jeteta4[0] = abs(tree.Jets.at(PTordered[0]).p4_.Eta())

      jetN[0] = njets
      scalarHT=0
      for ii in range(4,njets) : scalarHT+=tree.Jets.at(ii).p4_.Pt()
      jetHTrest[0] = scalarHT
      scalarHTrest=0
      for ii in range(0,njets) : scalarHT+=tree.Jets.at(ii).p4_.Pt()
      jetHTfull[0] = scalarHT
      
      #if njets > 5 :
      #  jeteta5[0] = tree.Jets.at(5).p4_.Eta()
      #  jetpt5[0] = tree.Jets.at(5).p4_.Pt()
      #  jetcsv5[0] = tree.Jets.at(5).CSV()
      #else :
      #  jeteta5[0] = -1
      #  jetpt5[0] = -100
      #  jetcsv5[0] = -100
      #if PHH.M() > 250 :
      treeout.Fill()
  print counter
  fileout.Write()
  fileout.Close()
print "done "
print "Sig ",countSig
print "Sig NoHLT ",countSigNoTr
print "ttbar ", countttbar
print "ttbar, noHLT ",countttbarNoHLT 
print "QCD ",countQCD
print "QCD mix ",countQCDmixL," ",countQCDmixH
print "QCD mix ",countdata," ",countdatamix



