#!/usr/bin/env python

histdone=1 # 0 = no
# option 0 is  to make the 2D histos, and a second one with 1 to make the file with events and weights to test

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
#path = "/lustre/cmswork/hh/alp_baseSelector/"
path = "/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/alpha_ntuples/v1_20161028_noJetCut/" 
outpath="/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/to_Reweighting/"
fileoutput = "events_SumV0.root"
files = []
endfile = "_13TeV-madgraph_reHLT-v1.root"
files.append("GluGluToHHTo4B_node_SM")
files.append("GluGluToHHTo4B_node_box")
for ifile in range(2,14) : files.append("GluGluToHHTo4B_node_"+str(ifile))

countSig=np.zeros((15)) 
normSig= np.ones((15)) # [  0.30445146/14. ,  8.08541789/14. ,  9.07503515/14.  , 7.87640546/14.  , 5.54326759/14. , 9.07453435/14.,\ #8.89697223/14.  , 4.99948358/14. ,  6.35276001/14.   ,7.22011991/14. , 7.86669971/14. , 10.07471099/14. , 11.09319376/14.  , 8.16508973/14. ]
if histdone==0 :
  ###############################################################
  # to make the histograms to save the sum of FulSim Benchmarks
  binsx = [250.,300.,350., 400.,450.,500.,550.,600.,700.,800.,900,1000.] 
  binsy = [ -1., -0.6,0.6,1. ]
  binsx = array( 'f', [250.,270.,300.,330.,360.,390., 420.,450.,500.,550.,600.,700.,800.,1000. ] )
  binsy = array( 'f', [-1, -0.55,0.55,1] )
  bincost=3
  binmhh=13
  histAnalytical = ROOT.TH2D('SumV0_AnalyticalBin', '', binmhh,binsx,bincost,binsy)
  histAnalytical.SetTitle('HistSum2D')
  histAnalytical.SetXTitle('M_{HH}')
  histAnalytical.SetYTitle('cost*')
  histBench = ROOT.TH2D('SumV0_BenchBin', '', 90,0.,1800.,10,-1,1.)
  histBench.SetTitle('HistSum2D')
  histBench.SetXTitle('M_{HH}')
  histBench.SetYTitle('cost*')
  histmhh = ROOT.TH1D('Mhh', '', 70,0,1000)
  histmhh.SetTitle('HistSum2D Mhh')
  histmhh.SetXTitle('M_{HH}')
  histcost = ROOT.TH1D('Cost', '', 10,-1,1)
  histcost.SetTitle('HistSum2D cost')
  histcost.SetXTitle('cost*')
##################################################
# to make the weights once the histograms are done
if histdone==1 :
  ################
  sumWSM=1
  sumW1=1
  sumW2=1
  sumW3=1
  sumW4=1
  sumW5=1
  sumW6=1
  sumW7=1
  sumW8=1
  sumW9=1
  sumW10=1
  sumW11=1
  sumW12=1
  fileHH=ROOT.TFile(outpath+"HistSum2D.root")
  sumHBenchBin = fileHH.Get("SumV0_BenchBin")
  sumHAnalyticalBin = fileHH.Get("SumV0_AnalyticalBin")
  print "Sum to Bench hist ",sumHBenchBin.GetNbinsX(),sumHBenchBin.GetNbinsY(),sumHBenchBin.Integral()
  # check mhh hist to SM
  histmhhRe = ROOT.TH1D('Mhh', '', 20,0,1000)
  histmhhSM = ROOT.TH1D('Mhh', '', 20,0,1000)
  histmhhBench1 = ROOT.TH1D('Mhh', '', 20,0,1000)
  ###############################################
  # Read histograms with JHEP benchmarks
  fileH=ROOT.TFile("/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/to_BDT/Distros_5p_500000ev_12sam_13TeV_JHEP_500K.root")
  bench = []
  for ibench in range(0,12) : bench.append(fileH.Get(str(ibench)+"_bin1")) # in the old binning
  print "Bench hist ",bench[0].GetNbinsX(),bench[0].GetNbinsY(),bench[0].Integral()
  fileSM=ROOT.TFile("/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/to_BDT/Distros_5p_SM600k_sumBenchJHEP_13TeV.root")
  histSM = fileSM.Get("H0bin1")
  print "SM hist ",histSM.GetNbinsX(),histSM.GetNbinsY(),histSM.Integral(),histSM.GetXaxis().GetBinLowEdge(1),histSM.GetXaxis().GetBinUpEdge(90)
  ##############################################
  # do one file with events to test
  fileout=ROOT.TFile(outpath+fileoutput,"recreate")
  treeout = TTree('treeout', 'treeout')
  Genmhh = np.zeros(1, dtype=float)
  GenHHCost = np.zeros(1, dtype=float) 
  # weight benchmarks JHEP
  weightAnalytical = np.zeros(1, dtype=float)
  weightSM = np.zeros(1, dtype=float)
  weight1 = np.zeros(1, dtype=float)
  weight2 = np.zeros(1, dtype=float)
  weight3 = np.zeros(1, dtype=float)
  weight4 = np.zeros(1, dtype=float)
  weight5 = np.zeros(1, dtype=float)
  weight6 = np.zeros(1, dtype=float)
  weight7 = np.zeros(1, dtype=float)
  weight8 = np.zeros(1, dtype=float)
  weight9 = np.zeros(1, dtype=float)
  weight10 = np.zeros(1, dtype=float)
  weight11 = np.zeros(1, dtype=float)
  weight12 = np.zeros(1, dtype=float)
  treeout.Branch('Genmhh', Genmhh, 'Genmhh/D')
  treeout.Branch('GenHHCost', GenHHCost, 'GenHHCost/D')
  treeout.Branch('weightAnalytical', weightAnalytical, 'weightAnalytical/D')
  treeout.Branch('weightSM', weightSM, 'weightSM/D')
  treeout.Branch('weight1', weight1, 'weight1/D')
  treeout.Branch('weight2', weight2, 'weight2/D')
  treeout.Branch('weight3', weight3, 'weight3/D')
  treeout.Branch('weight4', weight4, 'weight4/D')
  treeout.Branch('weight5', weight5, 'weight5/D')
  treeout.Branch('weight6', weight6, 'weight6/D')
  treeout.Branch('weight7', weight7, 'weight7/D')
  treeout.Branch('weight8', weight8, 'weight8/D')
  treeout.Branch('weight9', weight9, 'weight9/D')
  treeout.Branch('weight10', weight10, 'weight10/D')
  treeout.Branch('weight11', weight11, 'weight11/D')
  treeout.Branch('weight12', weight12, 'weight12/D')
##############################################################
# loop in all events
countevent=0
for ifile in range(0,14) : # len(files)  
  print path+files[ifile]+endfile
  file=ROOT.TFile(path+files[ifile]+endfile)
  tree=file.ntuple.Get("tree")
  nev = tree.GetEntries()
  print nev
  counter=0
  #if ifile==16 : treeout.Fill()
  for iev in range(0,nev) :    
    tree.GetEntry(iev)
    njets=tree.Jets.size()
    GenPH1 = ROOT.TLorentzVector()
    GenPH1.SetPxPyPzE(tree.TL_GenHs.at(0).p4_.Px(),tree.TL_GenHs.at(0).p4_.Py(),tree.TL_GenHs.at(0).p4_.Pz(),tree.TL_GenHs.at(0).p4_.E())
    GenPH2 = ROOT.TLorentzVector()
    GenPH2.SetPxPyPzE(tree.TL_GenHs.at(1).p4_.Px(),tree.TL_GenHs.at(1).p4_.Py(),tree.TL_GenHs.at(1).p4_.Pz(),tree.TL_GenHs.at(1).p4_.E())
    GenPHH = ROOT.TLorentzVector()
    GenPHH = GenPH1 + GenPH2
    #countSig[ifile]+=(w_oneInvFb)/normSig[ifile]
    # make the 2D histogram
    if histdone==0 :
      histAnalytical.Fill(GenPHH.M(),CosThetaStar(GenPH1, GenPHH))
      histBench.Fill(GenPHH.M(),CosThetaStar(GenPH1, GenPHH)) 
      histmhh.Fill(GenPHH.M())
      histcost.Fill(CosThetaStar(GenPH1, GenPHH))
    # make tree for test
    if histdone==1 :
      Genmhh[0] = GenPHH.M()
      GenHHCost[0] =  CosThetaStar(GenPH1, GenPHH)
      # find the bin the event belong
      bmhh = histSM.GetXaxis().FindBin(GenPHH.M())
      bcost = histSM.GetXaxis().FindBin(CosThetaStar(GenPH1, GenPHH))
      if sumHBenchBin.GetBinContent(bmhh,bcost) >0 : # to be done with all events
         weightSM[0] = (histSM.GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./529.143984541) # 100k / 12 * 300k 
         weight1[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493)
         weight2[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493)
         weight3[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weight4[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weight5[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weight6[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weight7[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weight8[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weight9[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weight10[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weight11[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493)
         weight12[0] = (bench[0].GetBinContent(bmhh,bcost) / sumHBenchBin.GetBinContent(bmhh,bcost))*(100000./4140488)*(1./2747.43021493) 
         weightAnalytical[0] = (1./ sumHAnalyticalBin.GetBinContent(bmhh,bcost))
         sumWSM+=weightSM[0]
         sumW1+=weight1[0]
         sumW2+=weight2[0]
         sumW3+=weight3[0]
         sumW4+=weight4[0]
         sumW5+=weight5[0]
         sumW6+=weight6[0]
         sumW7+=weight7[0]
         sumW8+=weight8[0]
         sumW9+=weight9[0]
         sumW10+=weight10[0]
         sumW11+=weight11[0]
         sumW12+=weight12[0]
      elif 1>0 : weightSM[0] = 0
      # make histogram to test
      histmhhRe.Fill(GenPHH.M(),weightSM[0])
      histmhhBench1.Fill(GenPHH.M(),weight1[0])
      if ifile ==0 : histmhhSM.Fill(GenPHH.M())
      countevent+=1
  print counter
print countevent
# save tree of events
if histdone==1 :
  fileout.Write()
  fileout.Close()
  cs=ROOT.TCanvas("cs","cs",10,10,500,500)
  leg = ROOT.TLegend(0.5,0.60,0.99,0.99);
  histmhhRe.Scale(1./histmhhRe.Integral())
  histmhhRe.SetLineWidth(2)
  histmhhRe.SetLineColor(1)
  histmhhRe.Draw()
  leg.AddEntry(histmhhRe,"reweigted")
  histmhhSM.Scale(1./histmhhSM.Integral())
  histmhhSM.SetLineWidth(2)
  histmhhSM.SetLineColor(8)
  histmhhSM.Draw("same")
  leg.AddEntry(histmhhSM,"SM")
  leg.Draw("same")
  cs.SaveAs("SMtest.png") 
  histmhhBench1.Scale(1./histmhhBench1.Integral())
  histmhhBench1.Draw()
  cs.SaveAs("Bench1.png") 
  print "W1",sumW1
  print "W2",sumW2
  print "W3",sumW3
  print "W4",sumW4
  print "W5",sumW5
  print "W6",sumW6
  print "W7",sumW7
  print "W8",sumW8
  print "W9",sumW9
  print "W10",sumW10
  print "W11",sumW11
  print "W12",sumW12
  print "WSM",sumWSM
# save histogram
if histdone==0 :
  fileH=ROOT.TFile(outpath+"HistSum2D.root","recreate")
  fileH.cd()
  histAnalytical.Write()
  histBench.Write()
  fileH.Close()


print "done "
print "Sig ",countSig



