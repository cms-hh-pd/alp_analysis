#!/usr/bin/env python

histdone=1 # 0 = no
# option 0 is  to make the 2D histos, and a second one with 1 to make the file with events and weights to test
# lambda scan: 0 ,  +-1 , 2 , 2.4 , 3, 5,7 , 10 , 15, 20

# good old python modules
import json
import os
import importlib
from array import array
from glob import glob
import numpy as np
import os, sys, time,math
import shutil,subprocess
from HHStatAnalysis.AnalyticalModels.NonResonantModel import NonResonantModel

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
path = "/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/alp_baseSelector/def/" 
outpath="/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/to_Reweighting/"
#data="/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/CMSSW_7_4_7/src/HHStatAnalysis_git/AnalyticalModels/data/"
data="../../../HHStatAnalysis/AnalyticalModels/data/"
model = NonResonantModel()
# obtaining BSM/SM coeficients
dumb = model.ReadCoefficients("../../../HHStatAnalysis/AnalyticalModels/data/coefficientsByBin_klkt.txt",model.effSM,model.effSum,model.MHH,model.COSTS,model.A1,model.A3,model.A7)  

fileoutput = "events_SumV0_afterBaseline.root"
files = []
endfile = ".root"
files.append("HHTo4B_SM")
files.append("HHTo4B_BMbox")
for ifile in range(2,14) : files.append("HHTo4B_BM"+str(ifile))
# to analytical re
# We sum SM + box + the benchmarks from 2-13 
# read the 2D histo referent to the sum of events
fileHH=ROOT.TFile("../../../Support/NonResonant/Hist2DSum_V0_SM_box.root")
sumHAnalyticalBin = fileHH.Get("SumV0_AnalyticalBin")
sumHBenchBin = fileHH.Get("SumV0_AnalyticalBin")

countSig=np.zeros((15)) 
normSig= np.ones((15)) # [  0.30445146/14. ,  8.08541789/14. ,  9.07503515/14.  , 7.87640546/14.  , 5.54326759/14. , 9.07453435/14.,\ #8.89697223/14.  , 4.99948358/14. ,  6.35276001/14.   ,7.22011991/14. , 7.86669971/14. , 10.07471099/14. , 11.09319376/14.  , 8.16508973/14. ]
if 1 > 0 :
  ################
  sumWSM=0
  sumWSMA=0
  sumWboxA=0
  sumW1=0
  sumW2=0
  sumW3=0
  sumW4=0
  sumW5=0
  sumW6=0
  sumW7=0
  sumW8=0
  sumW9=0
  sumW10=0
  sumW11=0
  sumW12=0
  # lambda scan: 
  sumL0=0
  sumL2p4=0
  sumL3=0
  sumL4=0
  sumL5=0
  sumL7=0
  sumL10=0
  sumL12p5=0
  sumL15=0
  sumL20=0
  sumLm1=0
  sumLm2p4=0
  sumLm3=0
  sumLm4=0
  sumLm5=0
  sumLm7=0
  sumLm10=0
  sumLm12p5=0
  sumLm15=0
  sumLm20=0
  #fileHH=ROOT.TFile(outpath+"HistSum2D.root")
  sumHBenchBin = fileHH.Get("SumV0_BenchBin")
  sumHAnalyticalBin = fileHH.Get("SumV0_AnalyticalBin")
  print "Sum to Bench hist ",sumHBenchBin.GetNbinsX(),sumHBenchBin.GetNbinsY(),sumHBenchBin.Integral()
  # check mhh hist to SM
  binsxV0 = array( 'f',  [240.,250.,270.,290.,310.,330.,350.,390.,410.,450.,500.,550.,600.,700.,800.,1000.,1200 ])
  binsyV0 = array( 'f', [-1., -0.6,0.6,1.] )
  histmhhRe = ROOT.TH1D('MhhRe', '', 30,200.,1000.) #50,240,1000) # 14,binsxV0) #13,binsxV0)
  histmhhSM = ROOT.TH1D('MhhSM', '', 30,200.,1000.) # 13,binsxV0)
  histmhhReA = ROOT.TH1D('MhhSMA', '', 30,200.,1000.) # 13,binsxV0)
  histmhhBox = ROOT.TH1D('MhhBox', '', 30,200.,1000.) # 13,binsxV0)
  histmhhBoxA = ROOT.TH1D('MhhBoxA', '', 30,200.,1000.) # 13,binsxV0)
  histmhhL15 = ROOT.TH1D('MhhL15', '', 30,200.,1000.) # 13,binsxV0)
  histmhhBench1 = ROOT.TH1D('MhhBench1', '', 30,0.,1000.) # 50,240,1000)
  ###############################################
  # Read histograms with JHEP benchmarks
  fileH=ROOT.TFile("../../../Support/NonResonant/Distros_5p_500000ev_12sam_13TeV_JHEP_500K.root")
  bench = []
  for ibench in range(0,12) : bench.append(fileH.Get(str(ibench)+"_bin1")) # in the old binning
  print "Bench hist ",bench[0].GetNbinsX(),bench[0].GetNbinsY(),bench[0].Integral()
  fileSM=ROOT.TFile("../../../Support/NonResonant/Distros_5p_SM3M_sumBenchJHEP_13TeV.root")
  histSM = fileSM.Get("H0bin1") # fine binning (the H0bin2 is with the bin used to analytical)
  #create a new TH2 with your bin arrays spec 
  xaxis = histSM.GetXaxis()
  yaxis = histSM.GetYaxis()
  histmhhSM3M = fileSM.Get("0_mhh") # binning 200,0.,1000.
  """
  histSM = ROOT.TH2F("SMrebin","",48,240.,1200.,5,-1,1.)
  histmhhSM3M = ROOT.TH1F("histmhhSM3M","",14,binsxV0)
  for i in range(1,xaxis.GetNbins()+1) :
     histmhhSM3M.Fill(xaxis.GetBinCenter(i),histmhhSM3M0.GetBinContent(i));  # 24,240.,1200.,5,-1,1.
     for j in range(1,yaxis.GetNbins()+1) :
         bmhh0= xaxis.GetBinCenter(i)
         bcost0=yaxis.GetBinCenter(j)
         if bmhh0>245 and bmhh0<1801 :
           histSM.Fill(xaxis.GetBinCenter(i),yaxis.GetBinCenter(j),histSM0.GetBinContent(i,j));
           #h1Sum.Fill(xaxis.GetBinCenter(i),yaxis.GetBinCenter(j),h1Sum.GetBinContent(i,j));
  """
  print "SM hist ",histSM.GetNbinsX(),histSM.GetNbinsY(),histSM.Integral(),histSM.GetXaxis().GetBinLowEdge(1),histSM.GetXaxis().GetBinUpEdge(xaxis.GetNbins())
  print "Sum hist ",sumHBenchBin.GetNbinsX(),sumHBenchBin.GetNbinsY(),sumHBenchBin.Integral(),sumHBenchBin.GetXaxis().GetBinLowEdge(1),sumHBenchBin.GetXaxis().GetBinUpEdge(sumHBenchBin.GetXaxis().GetNbins())
  print "Sum hist Analytical ",sumHAnalyticalBin.GetNbinsX(),sumHAnalyticalBin.GetNbinsY(),sumHAnalyticalBin.Integral(),sumHAnalyticalBin.GetXaxis().GetBinLowEdge(1),sumHAnalyticalBin.GetXaxis().GetBinUpEdge(sumHAnalyticalBin.GetXaxis().GetNbins())
  #histSM.Draw("colz")
  ##############################################
  # do one file with events to test
  fileout=ROOT.TFile(outpath+fileoutput,"recreate")
  treeout = TTree('treeout', 'treeout')
  Genmhh = np.zeros(1, dtype=float)
  GenHHCost = np.zeros(1, dtype=float) 
  # weight benchmarks JHEP
  effSumV0AnalyticalBin = np.zeros(1, dtype=float)
  weightSM = np.zeros(1, dtype=float)
  weightSMA = np.zeros(1, dtype=float)
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
  # lamda scan
  weightL0 = np.zeros(1, dtype=float)
  weightL2p4 = np.zeros(1, dtype=float) 
  weightL3 = np.zeros(1, dtype=float) 
  weightL4 = np.zeros(1, dtype=float) 
  weightL5 = np.zeros(1, dtype=float) 
  weightL7 = np.zeros(1, dtype=float) 
  weightL10 = np.zeros(1, dtype=float) 
  weightL12p5 = np.zeros(1, dtype=float) 
  weightL15 = np.zeros(1, dtype=float) 
  weightL20 = np.zeros(1, dtype=float) 
  weightLm1 = np.zeros(1, dtype=float) 
  weightLm2p4 = np.zeros(1, dtype=float) 
  weightLm3 = np.zeros(1, dtype=float) 
  weightLm4 = np.zeros(1, dtype=float) 
  weightLm5 = np.zeros(1, dtype=float) 
  weightLm7 = np.zeros(1, dtype=float) 
  weightLm10 = np.zeros(1, dtype=float) 
  weightLm12p5 = np.zeros(1, dtype=float) 
  weightLm15 = np.zeros(1, dtype=float) 
  weightLm20 = np.zeros(1, dtype=float) 
  sumL0=0
  sumL2p4=0
  sumL3=0
  sumL4=0
  sumL5=0
  sumL7=0
  sumL10=0
  sumL12p5=0
  sumL15=0
  sumL20=0
  sumLm1=0
  sumLm2p4=0
  sumLm3=0
  sumLm4=0
  sumLm5=0
  sumLm7=0
  sumLm10=0
  sumLm12p5=0
  sumLm15=0
  sumLm20=0
  treeout.Branch('Genmhh', Genmhh, 'Genmhh/D')
  treeout.Branch('GenHHCost', GenHHCost, 'GenHHCost/D')
  treeout.Branch('effSumV0AnalyticalBin', effSumV0AnalyticalBin, 'effSumV0AnalyticalBin/D')
  treeout.Branch('weightSM', weightSM, 'weightSM/D')
  treeout.Branch('weightSMA', weightSMA, 'weightSMA/D')
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
  # lamda scan
  treeout.Branch('weightL0', weightL0, 'weightL0/D')
  treeout.Branch('weightL2p4', weightL2p4, 'weightL2p4/D')
  treeout.Branch('weightL3', weightL3, 'weightL3/D')
  treeout.Branch('weightL4', weightL4, 'weightL4/D')
  treeout.Branch('weightL5', weightL5, 'weightL5/D')
  treeout.Branch('weightL7', weightL7, 'weightL7/D')
  treeout.Branch('weightL10', weightL10, 'weightL10/D')
  treeout.Branch('weightL12p5', weightL12p5, 'weightL12p5/D')
  treeout.Branch('weightL15', weightL15, 'weightL15/D')
  treeout.Branch('weightL20', weightL20, 'weightL20/D')
  treeout.Branch('weightLm1', weightLm1, 'weightLm1/D')
  treeout.Branch('weightLm2p4', weightLm2p4, 'weightLm2p4/D')
  treeout.Branch('weightLm3', weightLm3, 'weightLm3/D')
  treeout.Branch('weightLm4', weightLm4, 'weightLm4/D')
  treeout.Branch('weightLm5', weightLm5, 'weightLm5/D')
  treeout.Branch('weightLm7', weightLm7, 'weightLm7/D')
  treeout.Branch('weightLm10', weightLm10, 'weightLm10/D')
  treeout.Branch('weightLm12p5', weightLm12p5, 'weightLm12p5/D')
  treeout.Branch('weightLm15', weightLm15, 'weightLm15/D')
  treeout.Branch('weightLm20', weightLm20, 'weightLm20/D')
#########################################################
normBench = [ 49976.6016382, 50138.2521798, 49990.0468825, 49993.1979924, 50041.0282539, 50038.5462286, 101.036904355, 50000.3090638, 50045.3506862, 49992.1242267, 50024.7055638, 50006.2937198]
normSM = 299803.461384
normSManal =  1.96357948093
##############################################################
# loop in all events
countevent=0
for ifile in range(0,14) : # len(files)  
  print path+files[ifile]+endfile
  file=ROOT.TFile(path+files[ifile]+endfile)
  tree=file.pair.Get("tree")
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
    # make tree for test
    if 1 > 0 :
      Genmhh[0] = GenPHH.M()
      #GenHHCost[0] =  CosThetaStar(GenPH1, GenPHH)
      #print GenPHH.M(), CosThetaStar(GenPH1, GenPHH)
      # find the bin the event belong
      bmhh = histSM.GetXaxis().FindBin(GenPHH.M())
      bcost = histSM.GetYaxis().FindBin(CosThetaStar(GenPH1, GenPHH))
      #print sumHBenchBin.GetBinContent(bmhh,bcost),bmhh,bcost 
      mergecostSum = 0
      for ii in range(1,11) : mergecostSum+= sumHBenchBin.GetBinContent(bmhh,ii) 
      if mergecostSum >0 : # to be done with all events
         weightSM[0] = (histSM.GetBinContent(bmhh,bcost) / mergecostSum)/normSM # 100k / 12 * 300k * what is needed to make the sum of weights to be 1
         weight1[0] = (bench[0].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[0] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1637128.75403) 
         weight2[0] = (bench[1].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[1] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1023280.0075)
         weight3[0] = (bench[2].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[2] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1277504.79631)  
         weight4[0] = (bench[3].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[3] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1500606.32315)  
         weight5[0] = (bench[4].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[4] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1227513.28444)  
         weight6[0] = (bench[5].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[5] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./2020945.7276)  
         weight7[0] = (bench[6].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[6] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./3019.80377538)  
         weight8[0] = (bench[7].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[7] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1496218.05353)  
         weight9[0] = (bench[8].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[8] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1185661.59471)  
         weight10[0] = (bench[9].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[9] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./2529136.36765)  
         weight11[0] = (bench[10].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[10] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1916322.26718) 
         weight12[0] = (bench[11].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[11] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1957763.10013)   
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
      # weight analytical 
      mhhcost= [GenPHH.M(),CosThetaStar(GenPH1, GenPHH)] # to store [mhh , cost] of that event
      bmhh = sumHAnalyticalBin.GetXaxis().FindBin(mhhcost[0])
      bcost = sumHAnalyticalBin.GetYaxis().FindBin(mhhcost[1])
      if sumHAnalyticalBin.GetBinContent(bmhh,bcost) >0 : # to be done with all events
         # find the Nevents from the sum of events on that bin
         effSumV0 = sumHAnalyticalBin.GetBinContent(bmhh,bcost)  # quantity of simulated events in that bin (without cuts)
         weightSMA[0] = model.getScaleFactor(mhhcost,1.0, 1.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         sumWSMA+=weightSMA[0]
         # lambda scan
         weightL0[0] = model.getScaleFactor(mhhcost,1.0, 0.01,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL2p4[0] = model.getScaleFactor(mhhcost,1.0, 2.4,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL3[0] = model.getScaleFactor(mhhcost,1.0, 3.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL4[0] = model.getScaleFactor(mhhcost,1.0, 4.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL5[0] = model.getScaleFactor(mhhcost,1.0, 5.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL7[0] = model.getScaleFactor(mhhcost,1.0, 7.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL10[0] = model.getScaleFactor(mhhcost,1.0, 10.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL12p5[0] = model.getScaleFactor(mhhcost,1.0, 12.5,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL15[0] = model.getScaleFactor(mhhcost,1.0, 15.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightL20[0] = model.getScaleFactor(mhhcost,1.0, 20.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm1[0] = model.getScaleFactor(mhhcost,1.0, -1.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm2p4[0] = model.getScaleFactor(mhhcost,1.0,-2.4,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm3[0] = model.getScaleFactor(mhhcost,1.0, -3.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm4[0] = model.getScaleFactor(mhhcost,1.0, -4.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm5[0] = model.getScaleFactor(mhhcost,1.0, -5.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm7[0] = model.getScaleFactor(mhhcost,1.0, -7.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm10[0] = model.getScaleFactor(mhhcost,1.0, -10.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm12p5[0] = model.getScaleFactor(mhhcost,1.0, -12.5,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm15[0] = model.getScaleFactor(mhhcost,1.0, -15.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         weightLm20[0] = model.getScaleFactor(mhhcost,1.0, -15.0,model.effSM,model.MHH,model.COSTS,model.A1,model.A3,model.A7, effSumV0) 
         sumL0=weightL0[0]
         sumL2p4=weightL2p4[0]
         sumL3=weightL3[0]
         sumL4=weightL4[0]
         sumL5=weightL5[0]
         sumL7=weightL7[0]
         sumL10=weightL10[0]
         sumL12p5=weightL12p5[0]
         sumL15=weightL15[0]
         sumL20=weightL20[0]
         sumLm1=weightLm1[0]
         sumLm2p4=weightLm2p4[0]
         sumLm3=weightLm3[0]
         sumLm4=weightLm4[0]
         sumLm5=weightLm5[0]
         sumLm7=weightLm7[0]
         sumLm10=weightLm10[0]
         sumLm12p5=weightLm12p5[0]
         sumLm15=weightLm15[0]
         sumLm20=weightLm20[0]
      treeout.Fill()
      # make histogram to test
      histmhhReA.Fill(GenPHH.M(),weightSMA[0])
      histmhhRe.Fill(GenPHH.M(),weightSM[0])
      histmhhBoxA.Fill(GenPHH.M(),weightL0[0])
      histmhhBench1.Fill(GenPHH.M(),weight1[0])
      histmhhL15.Fill(GenPHH.M(),weightL15[0])
      if ifile ==0 : histmhhSM.Fill(GenPHH.M())
      if ifile ==1 : histmhhBox.Fill(GenPHH.M())
      countevent+=1
  print counter
print countevent
# save tree of events
if 1 > 0 :
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
  print "WSMA",sumWSMA
  print "lambda scan:" 
  print sumL0
  print sumL2p4
  print sumL3
  print sumL4
  print sumL5
  print sumL7
  print sumL10
  print sumL12p5
  print sumL15
  print sumL20
  print sumLm1
  print sumLm2p4
  print sumLm3
  print sumLm4
  print sumLm5
  print sumLm7
  print sumLm10
  print sumLm12p5
  print sumLm15
  print sumLm20
  fileout.Write()
  fileout.Close()
  cs=ROOT.TCanvas("cs","cs",10,10,500,500)
  leg = ROOT.TLegend(0.5,0.60,0.99,0.99);
  histmhhRe.Scale(1./histmhhRe.Integral())
  histmhhRe.SetLineWidth(2)
  histmhhRe.SetLineColor(1)
  histmhhRe.Draw()
  leg.AddEntry(histmhhRe,"reweigted (from hist)")
  histmhhReA.Scale(1./histmhhReA.Integral())
  histmhhReA.SetLineWidth(2)
  histmhhReA.SetLineColor(2)
  histmhhReA.Draw("same")
  leg.AddEntry(histmhhReA,"reweigted (from analitical)")
  histmhhSM.Scale(1./histmhhSM.Integral())
  histmhhSM.SetLineWidth(2)
  histmhhSM.SetLineColor(8)
  histmhhSM.Draw("same")
  leg.AddEntry(histmhhSM,"SM")
 
  """
  histmhhSM3M.Scale(1./histmhhSM3M.Integral())
  histmhhSM3M.SetLineWidth(2)
  histmhhSM3M.SetLineColor(2)
  histmhhSM3M.Draw("same")
  leg.AddEntry(histmhhSM3M,"SM (from 3M ev)")
  """
  leg.Draw("same")
  cs.SaveAs("SMtest_afterCuts.png") 
  cs.Clear()
  leg.Clear()
  ###########################
  histmhhBox.Scale(1./histmhhBox.Integral())
  histmhhBox.SetLineWidth(2)
  histmhhBox.SetLineColor(8)
  histmhhBox.Draw()
  leg.AddEntry(histmhhBox,"#kappa_{#lambda} = 0")
  histmhhBoxA.Scale(1./histmhhBoxA.Integral())
  histmhhBoxA.SetLineWidth(2)
  histmhhBoxA.SetLineColor(1)
  histmhhBoxA.Draw("same")
  leg.AddEntry(histmhhBoxA,"reweigted (from analitical)")
  leg.Draw("same")
  cs.SaveAs("Boxtest_afterCuts.png") 
  cs.Clear()
  #################################################"
  histmhhBench1.Scale(1./histmhhBench1.Integral())
  histmhhBench1.Draw()
  cs.SaveAs("Bench1_afterCuts.png") 
  cs.Clear()
  #################################################"
  histmhhL15.Scale(1./histmhhL15.Integral())
  histmhhL15.Draw()
  cs.SaveAs("kl15_afterCuts.png") 

print "done "
print "Sig ",countSig



