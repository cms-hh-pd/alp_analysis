#!/usr/bin/env python

histdone=0 # 0 = no
histo2D="HistSum2D_4b_v01_02_2017.root"
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
from HHStatAnalysis.AnalyticalModels.NonResonantModel import NonResonantModel
# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT, TTree
# custom ROOT classes 
from ROOT import alp
#import import_alp
#import ctypes
#libalp = ctypes.CDLL("../src/alp_objects_h.so")

#import ctypes
#my_test_lib = ctypes.cdll.LoadLibrary('../src/alp_objects_h.so')

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
path = "/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/alpha_ntuples/v01_02_2017/noSel/" 
outpath="/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/to_Reweighting/"
data="/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/CMSSW_7_4_7/src/HHStatAnalysis_git/AnalyticalModels/data/"
model = NonResonantModel()
dumb = model.ReadCoefficients("../../../HHStatAnalysis/AnalyticalModels/data/coefficientsByBin_klkt.txt")  
# to analytical re
# We sum SM + box + the benchmarks from 2-13 
# read the 2D histo referent to the sum of events
if histdone==1 :
  fileHH=ROOT.TFile(outpath+histo2D)
  sumHAnalyticalBin = fileHH.Get("SumV0_AnalyticalBin")
  sumHBenchBin = fileHH.Get("SumV0_AnalyticalBin") 
# read histograms to check lamda scan
# read the 2D histo referent to the sum of events
fileL=ROOT.TFile("/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/CMSSW_9_0_0_pre1/src/Support/NonResonant/Distros_5p_SM100k_toRecursive_13TeV.root") 

####################################################################################################
fileoutput = "events_SumV0.root"
files = []
endfile = ".root"
files.append("HHTo4B_SM") 
files.append("HHTo4B_BMbox")
for ifile in range(2,14) : files.append("HHTo4B_BM"+str(ifile))

countSig=np.zeros((15)) 
normSig= np.ones((15)) 
if histdone==0 :
  ###############################################################
  # to make the histograms to save the sum of FulSim Benchmarks
  binsx = array( 'f', [250.,270.,300.,330.,360.,390., 420.,450.,500.,550.,600.,700.,800.,1000. ] )
  #binsx = array( 'f', [250.,300.,350., 400.,450.,500.,550.,600.,700.,800.,900.,1000.] )
  binsy = array( 'f', [-1., -0.55,0.55,1.] )
  bincost=3
  binmhh=13
  histAnalytical = ROOT.TH2D('SumV0_AnalyticalBin', '', binmhh,binsx,bincost,binsy)
  histAnalytical.SetTitle('HistSum2D')
  histAnalytical.SetXTitle('M_{HH}')
  histAnalytical.SetYTitle('cost*')
  histBench = ROOT.TH2D('SumV0_BenchBin_coarse', '', 48,240.,1200.,5,-1,1. ) #13,binsxV0,3,binsyV0) # (to match20 GeV binning)
  histBench.SetTitle('HistSum2D')
  histBench.SetXTitle('M_{HH}')
  histBench.SetYTitle('cost*')
  histBench0 = ROOT.TH2D('SumV0_BenchBin', '', 90,0.,1800.,10,-1,1.) #  version of Moriond 2016
  histBench0.SetTitle('HistSum2D')
  histBench0.SetXTitle('M_{HH}')
  histBench0.SetYTitle('cost*')
##################################################
# to make the weights once the histograms are done
if histdone==1 :
  ################
  sumWSM=0
  sumWSMA=0
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
  # lamda scan
  sumL0=0
  sumL0p5=0
  sumL2=0
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
  fileHH=ROOT.TFile( "../../../Support/NonResonant/Hist2DSum_V0_SM_box.root")
  sumHBenchBin = fileHH.Get("SumV0_BenchBin")
  #sumHBenchBin.Draw("colz")
  sumHAnalyticalBin = fileHH.Get("SumV0_AnalyticalBin")
  print "Sum to Bench hist ",sumHBenchBin.GetNbinsX(),sumHBenchBin.GetNbinsY(),sumHBenchBin.Integral()
  # check mhh hist to SM
  histmhhReA = ROOT.TH1D('MhhReA', '', 30,240.,1000. )
  histmhhRe = ROOT.TH1D('MhhRe', '', 30,240.,1000. )
  histmhhSM = ROOT.TH1D('MhhSM', '', 30,240.,1000.) 
  histmhhBench1 = ROOT.TH1D('MhhBench1', '', 60,0,1800) 
  histmhhBench2 = ROOT.TH1D('MhhBench2', '', 60,0,1800)  
  histmhhBench3 = ROOT.TH1D('MhhBench3', '', 60,0,1800) 
  histmhhBench4 = ROOT.TH1D('MhhBench4', '', 60,50,1800) 
  histmhhBench5 = ROOT.TH1D('MhhBench5', '', 60,0,1800) 
  histmhhBench6 = ROOT.TH1D('MhhBench6', '', 60,0,1800) 
  histmhhBench7 = ROOT.TH1D('MhhBench7', '', 60,0,1800) 
  histmhhBench8 = ROOT.TH1D('MhhBench8', '', 60,0,1800) 
  histmhhBench9 = ROOT.TH1D('MhhBench9', '', 60,0,1800) 
  histmhhBench10 = ROOT.TH1D('MhhBench10', '', 60,0,1800) 
  histmhhBench11 = ROOT.TH1D('MhhBench11', '', 60,0,1800) 
  histmhhBench12 = ROOT.TH1D('MhhBench12', '', 60,0,1800) 
  histmhhBoxRe = ROOT.TH1D('MhhBoxRe', '', 30,250.,1000. )
  histmhhBox = ROOT.TH1D('MhhBox', '', 30,250.,1000.) 
  histmhhL15 = ROOT.TH1D('MhhL15', '',  30,250.,1000. ) 
  histmhhL2p4 = ROOT.TH1D('MhhL2p4', '', 30,250.,1000. )  
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
  histmhhSM3M0 = fileSM.Get("0_mhh") # binning 200,0.,1000.
  histmhhBM1 = fileH.Get("0_mhh") 
  histmhhBM2 = fileH.Get("1_mhh") 
  histmhhBM3 = fileH.Get("2_mhh") 
  histmhhBM40 = fileH.Get("3_mhh") 
  histmhhBM5 = fileH.Get("4_mhh") 
  histmhhBM6 = fileH.Get("5_mhh") 
  histmhhBM7 = fileH.Get("6_mhh") 
  histmhhBM8 = fileH.Get("7_mhh") 
  histmhhBM9 = fileH.Get("8_mhh") 
  histmhhBM10 = fileH.Get("9_mhh") 
  histmhhBM11 = fileH.Get("10_mhh") 
  histmhhBM12 = fileH.Get("11_mhh")
  #histSM = ROOT.TH2F("SMrebin","",48,240.,1200.,5,-1,1.)
  histmhhSM3M = ROOT.TH1F("histmhhSM3M","",30,240.,1000.)
  histmhhBM4 = ROOT.TH1F("BM4","",60,200,1800)
  """
  histmhhBM1 = ROOT.TH1F("BM1","",20,240.,1500.)
  histmhhBM2 = ROOT.TH1F("BM2","",20,240.,1800.)
  histmhhBM3 = ROOT.TH1F("BM3","",20,240.,1500.)

  histmhhBM5 = ROOT.TH1F("BM5","",20,240.,1500.)
  histmhhBM6 = ROOT.TH1F("BM6","",20,240.,1500.)
  histmhhBM7 = ROOT.TH1F("BM7","",20,240.,1500.)
  histmhhBM8 = ROOT.TH1F("BM8","",20,240.,1500.)
  histmhhBM9 = ROOT.TH1F("BM9","",20,240.,1500.)
  histmhhBM10 = ROOT.TH1F("BM10","",20,240.,1500.)
  histmhhBM11 = ROOT.TH1F("BM11","",20,240.,1500.)
  histmhhBM12 = ROOT.TH1F("BM12","",20,240.,1500.)
  """
  ######
  # to check analytical weight in lamda scan 
  fileL=ROOT.TFile("../../../Support/NonResonant/Distros_5p_SM100k_toRecursive_13TeV.root")
  histmhhoL150 = fileL.Get("65_mhh") 
  histmhhoL2p40 = fileL.Get("60_mhh")
  histmhhoL15 = ROOT.TH1F("L15","",  30,240.,1000. )# 20,240.,1500.)
  histmhhoL2p4 = ROOT.TH1F("L2p4","", 30,240.,1000. ) # 20,240.,1800.)

  for i in range(1,histmhhSM3M0.GetXaxis().GetNbins()+1) :
     histmhhSM3M.Fill(histmhhSM3M0.GetXaxis().GetBinCenter(i),histmhhSM3M0.GetBinContent(i));  # 24,240.,1200.,5,-1,1.
  for i in range(1,histmhhBM10.GetXaxis().GetNbins()+1) :
     histmhhBM4.Fill(histmhhBM40.GetXaxis().GetBinCenter(i),histmhhBM40.GetBinContent(i)); 
  """
     histmhhBM1.Fill(histmhhBM10.GetXaxis().GetBinCenter(i),histmhhBM10.GetBinContent(i)); 
     histmhhBM3.Fill(histmhhBM30.GetXaxis().GetBinCenter(i),histmhhBM30.GetBinContent(i)); 
     histmhhBM4.Fill(histmhhBM40.GetXaxis().GetBinCenter(i),histmhhBM40.GetBinContent(i)); 
     histmhhBM5.Fill(histmhhBM50.GetXaxis().GetBinCenter(i),histmhhBM50.GetBinContent(i)); 
     histmhhBM6.Fill(histmhhBM60.GetXaxis().GetBinCenter(i),histmhhBM60.GetBinContent(i)); 
     histmhhBM7.Fill(histmhhBM70.GetXaxis().GetBinCenter(i),histmhhBM70.GetBinContent(i)); 
     histmhhBM8.Fill(histmhhBM80.GetXaxis().GetBinCenter(i),histmhhBM80.GetBinContent(i)); 
     histmhhBM9.Fill(histmhhBM90.GetXaxis().GetBinCenter(i),histmhhBM90.GetBinContent(i)); 
     histmhhBM10.Fill(histmhhBM100.GetXaxis().GetBinCenter(i),histmhhBM100.GetBinContent(i)); 
     histmhhBM11.Fill(histmhhBM110.GetXaxis().GetBinCenter(i),histmhhBM110.GetBinContent(i)); 
     histmhhBM12.Fill(histmhhBM120.GetXaxis().GetBinCenter(i),histmhhBM120.GetBinContent(i)); 
  """
  for i in range(1,histmhhoL150.GetXaxis().GetNbins()+1) :
     histmhhoL15.Fill(histmhhoL150.GetXaxis().GetBinCenter(i),histmhhoL150.GetBinContent(i)); 
     histmhhoL2p4.Fill(histmhhoL2p40.GetXaxis().GetBinCenter(i),histmhhoL2p40.GetBinContent(i)); 
  """
  for i in range(1,histmhhBM20.GetXaxis().GetNbins()+1) :
     histmhhBM2.Fill(histmhhBM20.GetXaxis().GetBinCenter(i),histmhhBM20.GetBinContent(i));  # 24,240.,1200.,5,-1,1.
  """
  print histmhhBM1.GetIntegral()
  """
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
  # lambda scan
  weightL0 = np.zeros(1, dtype=float)
  weightL0p5 = np.zeros(1, dtype=float)
  weightL2 = np.zeros(1, dtype=float)
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
  treeout.Branch('weightL0p5', weightL0p5, 'weightL0p5/D')
  treeout.Branch('weightL2', weightL2, 'weightL2/D')
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
normBench = [ 49976.6016382, 50138.2521798, 49990.0468825, 573.0, 50041.0282539, 50038.5462286, 50001.0693263, 50000.3090638, 50045.3506862, 49992.1242267, 50024.7055638, 50006.2937198]
normSM = 299803.461384
normSManal =  0.96357948099
normBox = 1.15610629338
countweightbox=0
if histdone==1 :
  listLam=[0.0001,0.5,2, 2.5, 3.0, 4.0, 4.0, 5.0, 7.0, 10.0, 12.5, 15.0, 20.0, -1.0,-2.4, -3.0, -4.0, -5.0, -7.0, -10.0, -12.5, -15.0, -20.0]
  normL =[] #1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
  for ii in range(0,len(listLam)): normL.append(model.getNormalization(float(listLam[ii]),1.0,sumHAnalyticalBin))
##############################################################
# loop in all events
countevent=0
for ifile in range(0,14) : #  len(files)  
  print path+files[ifile]+endfile
  file=ROOT.TFile(path+files[ifile]+endfile)
  tree=file.Get("tree")
  nev = tree.GetEntries()
  print nev
  counter=0
  evrun=nev
  factor=nev/evrun
  #if ifile==16 : treeout.Fill()
  for iev in range(0, evrun) : # evrun): # nev) :     
    tree.GetEntry(iev)
    njets=tree.Jets.size()
    #genMhh = tree.TL_GenHH.p4_.M()
    #genCost=tree.TL_GenHH.costhst_
    GenPH1 = ROOT.TLorentzVector()
    GenPH1.SetPxPyPzE(tree.TL_GenHs.at(0).p4_.Px(),tree.TL_GenHs.at(0).p4_.Py(),tree.TL_GenHs.at(0).p4_.Pz(),tree.TL_GenHs.at(0).p4_.E())
    GenPH2 = ROOT.TLorentzVector()
    GenPH2.SetPxPyPzE(tree.TL_GenHs.at(1).p4_.Px(),tree.TL_GenHs.at(1).p4_.Py(),tree.TL_GenHs.at(1).p4_.Pz(),tree.TL_GenHs.at(1).p4_.E())
    GenPHH = ROOT.TLorentzVector()
    GenPHH = GenPH1 + GenPH2
    genMhh =  GenPHH.M()
    genCost=CosThetaStar(GenPH1, GenPHH)
    # make the 2D histogram
    if histdone==0 :
      histAnalytical.Fill(genMhh,genCost)
      histBench.Fill(genMhh,genCost) 
      histBench0.Fill(genMhh,genCost)
    # make tree for test
    if histdone==1 :
      Genmhh[0] =  genMhh  # GenPHH.M()
      #GenHHCost[0] =  CosThetaStar(GenPH1, GenPHH)
      #print GenPHH.M(), CosThetaStar(GenPH1, GenPHH)
      # find the bin the event belong
      bmhh = histSM.GetXaxis().FindBin(genMhh)
      bcost = histSM.GetYaxis().FindBin(genCost)
      #print sumHBenchBin.GetBinContent(bmhh,bcost),bmhh,bcost 
      mergecostSum = 0
      for ii in range(1,11) : mergecostSum+= sumHBenchBin.GetBinContent(bmhh,ii) 
      if mergecostSum >0 : # to be done with all events
         weightSM[0] = factor*(histSM.GetBinContent(bmhh,bcost) / mergecostSum)/normSM # 100k / 12 * 300k * what is needed to make the sum of weights to be 1
         weight1[0] = factor*(bench[0].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[0] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1637128.75403) 
         weight2[0] = factor*(bench[1].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[1] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1023280.0075)
         weight3[0] = factor*(bench[2].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[2] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1277504.79631)  
         weight4[0] = factor*(bench[3].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[3] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1500606.32315)  
         weight5[0] = factor*(bench[4].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[4] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1227513.28444)  
         weight6[0] = factor*(bench[5].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[5] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./2020945.7276)  
         weight7[0] = factor*(bench[6].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[6] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./3019.80377538)  
         weight8[0] = factor*(bench[7].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[7] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1496218.05353)  
         weight9[0] = factor*(bench[8].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[8] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1185661.59471)  
         weight10[0] = factor*(bench[9].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[9] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./2529136.36765)  
         weight11[0] = factor*(bench[10].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[10] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1916322.26718) 
         weight12[0] = factor*(bench[11].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[11] # (sumHBenchBin.GetBinContent(bmhh,bcost)))*(1./1957763.10013)  
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
      mhhcost= [genMhh,genCost] # to store [mhh , cost] of that event
      bmhh = sumHAnalyticalBin.GetXaxis().FindBin(mhhcost[0])
      bcost = sumHAnalyticalBin.GetYaxis().FindBin(mhhcost[1])
      weightbox=0
      if sumHAnalyticalBin.GetBinContent(bmhh,bcost) >0 : # to be done with all events
         # find the Nevents from the sum of events on that bin
         effSumV0 = sumHAnalyticalBin.GetBinContent(bmhh,bcost)  # quantity of simulated events in that bin (without cuts)
         weightSMA[0] = factor*model.getScaleFactor(mhhcost,1.0, 1.0, effSumV0)/ model.getNormalization(1.0, 1.0,sumHAnalyticalBin) #normSManal 
         weightbox = factor*model.getScaleFactor(mhhcost , 0.0001,1.0, effSumV0)/ model.getNormalization(0.0001,1.0,sumHAnalyticalBin) #normBox
         sumWSMA+=weightSMA[0]
         countweightbox+=weightbox

         # lambda scan
         weightL0[0] = factor*model.getScaleFactor(mhhcost, 0.0001,1.0, effSumV0) / normL[0]
         weightL0p5[0] = factor*model.getScaleFactor(mhhcost, 0.5,1.0, effSumV0) / normL[1]
         weightL2[0] = factor*model.getScaleFactor(mhhcost, 2,1.0, effSumV0) / normL[2]
         weightL2p4[0] = factor*model.getScaleFactor(mhhcost, 2.5,1.0, effSumV0) / normL[3]
         weightL3[0] = factor*model.getScaleFactor(mhhcost, 3.0,1.0, effSumV0) / normL[4]
         weightL4[0] = factor*model.getScaleFactor(mhhcost, 4.0,1.0, effSumV0) / normL[5]
         weightL5[0] = factor*model.getScaleFactor(mhhcost, 5.0,1.0, effSumV0) / normL[6]
         weightL7[0] = factor*model.getScaleFactor(mhhcost, 7.0,1.0, effSumV0) / normL[7]
         weightL10[0] = factor*model.getScaleFactor(mhhcost, 10.0,1.0, effSumV0) / normL[8]
         weightL12p5[0] = factor*model.getScaleFactor(mhhcost, 12.5,1.0, effSumV0) / normL[9]
         weightL15[0] = factor*model.getScaleFactor(mhhcost, 15.0,1.0, effSumV0) / normL[10]
         weightL20[0] = factor*model.getScaleFactor(mhhcost, 20.0,1.0, effSumV0) / normL[11]
         weightLm1[0] = factor*model.getScaleFactor(mhhcost, -1.0,1.0, effSumV0) / normL[12]
         weightLm2p4[0] = factor*model.getScaleFactor(mhhcost,-2.4,1.0, effSumV0) / normL[13] 
         weightLm3[0] = factor*model.getScaleFactor(mhhcost, -3.0,1.0, effSumV0) / normL[14]
         weightLm4[0] = factor*model.getScaleFactor(mhhcost, -4.0,1.0, effSumV0) / normL[15]
         weightLm5[0] = factor*model.getScaleFactor(mhhcost, -5.0,1.0, effSumV0) / normL[16]
         weightLm7[0] = factor*model.getScaleFactor(mhhcost, -7.0,1.0, effSumV0) / normL[17]
         weightLm10[0] = factor*model.getScaleFactor(mhhcost, -10.0,1.0, effSumV0) / normL[18]
         weightLm12p5[0] = factor*model.getScaleFactor(mhhcost, -12.5,1.0, effSumV0) / normL[19]
         weightLm15[0] = factor*model.getScaleFactor(mhhcost, -15.0,1.0, effSumV0) / normL[20]
         weightLm20[0] = factor*model.getScaleFactor(mhhcost, -20.0,1.0, effSumV0) / normL[21]
         sumL0+=weightL0[0]
         sumL0p5+=weightL0p5[0]
         sumL2+=weightL2[0]
         sumL2p4+=weightL2p4[0]
         sumL3+=weightL3[0]
         sumL4+=weightL4[0]
         sumL5+=weightL5[0]
         sumL7+=weightL7[0]
         sumL10+=weightL10[0]
         sumL12p5+=weightL12p5[0]
         sumL15+=weightL15[0]
         sumL20+=weightL20[0]
         sumLm1+=weightLm1[0]
         sumLm2p4+=weightLm2p4[0]
         sumLm3+=weightLm3[0]
         sumLm4+=weightLm4[0]
         sumLm5+=weightLm5[0]
         sumLm7+=weightLm7[0]
         sumLm10+=weightLm10[0]
         sumLm12p5+=weightLm12p5[0]
         sumLm15+=weightLm15[0]
         sumLm20+=weightLm20[0]
      treeout.Fill()
      # make histogram to test*
      histmhhBoxRe.Fill(GenPHH.M(),weightbox)
      histmhhRe.Fill(GenPHH.M(),weightSM[0])
      histmhhReA.Fill(GenPHH.M(),weightSMA[0])

      histmhhBench1.Fill(GenPHH.M(),weight1[0])
      histmhhBench2.Fill(GenPHH.M(),weight2[0])
      histmhhBench3.Fill(GenPHH.M(),weight3[0])
      histmhhBench4.Fill(GenPHH.M(),weight4[0])
      histmhhBench5.Fill(GenPHH.M(),weight5[0])
      histmhhBench6.Fill(GenPHH.M(),weight6[0])
      histmhhBench7.Fill(GenPHH.M(),weight7[0])
      histmhhBench8.Fill(GenPHH.M(),weight8[0])
      histmhhBench9.Fill(GenPHH.M(),weight9[0])
      histmhhBench10.Fill(GenPHH.M(),weight10[0])
      histmhhBench11.Fill(GenPHH.M(),weight11[0])
      histmhhBench12.Fill(GenPHH.M(),weight12[0])

      histmhhL2p4.Fill(GenPHH.M(),weightL2p4[0])
      histmhhL15.Fill(GenPHH.M(),weightL15[0])
      if ifile ==0 : histmhhSM.Fill(GenPHH.M())
      if ifile ==1 : histmhhBox.Fill(GenPHH.M())
      countevent+=1
  print counter
print countevent
# save tree of events
if histdone==1 :
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
  print "WBoxA",countweightbox
  print "lambda scan:" 
  print 0,sumL0
  print 0.5,sumL0p5
  print 2,sumL2
  print 2.5,sumL2p4
  print 3,sumL3
  print 4,sumL4
  print 5,sumL5
  print 6,sumL7
  print 10,sumL10
  print 12.5,sumL12p5
  print 15,sumL15
  print 20,sumL20
  print -1,sumLm1
  print -2.4,sumLm2p4
  print -3,sumLm3
  print -4,sumLm4
  print -5,sumLm5
  print -7,sumLm7
  print -10,sumLm10
  print -12.5,sumLm12p5
  print -15,sumLm15
  print -20,sumLm20

  fileout.Write()
  fileout.Close()
  cs=ROOT.TCanvas("cs","cs",10,10,500,500)
  leg = ROOT.TLegend(0.5,0.60,0.99,0.99);
  histmhhRe.Scale(1./histmhhRe.Integral())
  histmhhRe.SetLineWidth(2)
  histmhhRe.SetLineColor(2)
  histmhhRe.Draw("hist")
  leg.AddEntry(histmhhRe,"reweigted (from histogram)")

  histmhhReA.Scale(1./histmhhReA.Integral())
  histmhhReA.SetLineWidth(2)
  histmhhReA.SetLineColor(1)
  histmhhReA.Draw("same,hist")
  leg.AddEntry(histmhhReA,"reweigted (from analytical)")

  histmhhSM.Sumw2()
  histmhhSM.Scale(1./histmhhSM.Integral())
  histmhhSM.SetLineWidth(2)
  histmhhSM.SetLineColor(8)
  histmhhSM.Draw("same,E2")
  leg.AddEntry(histmhhSM,"SM (from 300k events)")
  
  histmhhSM3M.Scale(1./histmhhSM3M.Integral())
  histmhhSM3M.SetLineWidth(2)
  histmhhSM3M.SetLineColor(6)
  histmhhSM3M.Draw("same,hist")
  leg.AddEntry(histmhhSM3M,"SM (from 3M ev)")
  
  leg.Draw("same")
  cs.SaveAs("SMtest.png") 
  leg.Clear()
  #############
  histmhhBench1.Scale(1./histmhhBench1.Integral())
  histmhhBench1.SetLineWidth(2)
  histmhhBench1.SetLineColor(1)
  leg.AddEntry(histmhhBench1,"BM1 ; Reweighted")
  histmhhBench1.Draw("hist")
  histmhhBM1.Scale(1./histmhhBM1.Integral())
  histmhhBM1.SetLineWidth(2)
  histmhhBM1.SetLineColor(8)
  leg.AddEntry(histmhhBM1,"Simulated (from 50k ev)")
  histmhhBM1.Draw("same")
  leg.Draw("same") 
  cs.SaveAs("Bench1.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench2.Scale(1./histmhhBench2.Integral())
  histmhhBench2.SetLineWidth(2)
  histmhhBench2.SetLineColor(1)
  leg.AddEntry(histmhhBench2,"BM2 ; Reweighted")
  histmhhBench2.Draw("hist")
  histmhhBM2.Scale(1./histmhhBM2.Integral())
  histmhhBM2.SetLineWidth(2)
  histmhhBM2.SetLineColor(8)
  leg.AddEntry(histmhhBM1,"Simulated (from 50k ev)")
  histmhhBM2.Draw("same")
  leg.Draw("same,hist") 
  cs.SaveAs("Bench2.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench3.Scale(1./histmhhBench3.Integral())
  histmhhBench3.SetLineWidth(2)
  histmhhBench3.SetLineColor(1)
  leg.AddEntry(histmhhBench3,"BM3 ; Reweighted")
  histmhhBench3.Draw("hist")
  histmhhBM3.Scale(1./histmhhBM3.Integral())
  histmhhBM3.SetLineWidth(2)
  histmhhBM3.SetLineColor(8)
  leg.AddEntry(histmhhBM3,"Simulated (from 50k ev)")
  histmhhBM3.Draw("same")
  leg.Draw("same") 
  cs.SaveAs("Bench3.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench4.Scale(1./histmhhBench4.Integral())
  histmhhBench4.SetLineWidth(2)
  histmhhBench4.SetLineColor(1)
  leg.AddEntry(histmhhBench4,"BM2 ; Reweighted")
  histmhhBench4.Draw("hist")
  histmhhBM4.Scale(1./histmhhBM4.Integral())
  histmhhBM4.SetLineWidth(2)
  histmhhBM4.SetLineColor(8)
  leg.AddEntry(histmhhBM4,"Simulated (from 50k ev)")
  histmhhBM4.Draw("same,hist")
  leg.Draw("same") 
  cs.SaveAs("Bench4.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench5.Scale(1./histmhhBench5.Integral())
  histmhhBench5.SetLineWidth(2)
  histmhhBench5.SetLineColor(1)
  leg.AddEntry(histmhhBench5,"BM5 ; Reweighted")
  histmhhBench5.Draw("hist")
  histmhhBM5.Scale(1./histmhhBM5.Integral())
  histmhhBM5.SetLineWidth(2)
  histmhhBM5.SetLineColor(8)
  leg.AddEntry(histmhhBM5,"Simulated (from 50k ev)")
  histmhhBM5.Draw("same,hist")
  leg.Draw("same") 
  cs.SaveAs("Bench5.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench6.Scale(1./histmhhBench6.Integral())
  histmhhBench6.SetLineWidth(2)
  histmhhBench6.SetLineColor(1)
  leg.AddEntry(histmhhBench6,"BM2 ; Reweighted")
  histmhhBench6.Draw("hist")
  histmhhBM6.Scale(1./histmhhBM6.Integral())
  histmhhBM6.SetLineWidth(2)
  histmhhBM6.SetLineColor(8)
  leg.AddEntry(histmhhBM6,"Simulated (from 50k ev)")
  histmhhBM6.Draw("same")
  leg.Draw("same,hist") 
  cs.SaveAs("Bench6.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench7.Scale(7./histmhhBench7.Integral())
  histmhhBench7.SetLineWidth(2)
  histmhhBench7.SetLineColor(1)
  leg.AddEntry(histmhhBench7,"BM7 ; Reweighted")
  histmhhBench7.Draw("hist")
  histmhhBM7.Scale(7./histmhhBM7.Integral())
  histmhhBM7.SetLineWidth(2)
  histmhhBM7.SetLineColor(8)
  leg.AddEntry(histmhhBM7,"Simulated (from 50k ev)")
  histmhhBM7.Draw("same")
  leg.Draw("same") 
  cs.SaveAs("Bench7.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench8.Scale(7./histmhhBench8.Integral())
  histmhhBench8.SetLineWidth(2)
  histmhhBench8.SetLineColor(1)
  leg.AddEntry(histmhhBench8,"BM8 ; Reweighted")
  histmhhBench8.Draw("hist")
  histmhhBM8.Scale(7./histmhhBM8.Integral())
  histmhhBM8.SetLineWidth(2)
  histmhhBM8.SetLineColor(8)
  leg.AddEntry(histmhhBM7,"Simulated (from 50k ev)")
  histmhhBM8.Draw("same")
  leg.Draw("same,hist") 
  cs.SaveAs("Bench8.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench9.Scale(7./histmhhBench9.Integral())
  histmhhBench9.SetLineWidth(2)
  histmhhBench9.SetLineColor(1)
  leg.AddEntry(histmhhBench9,"BM9 ; Reweighted")
  histmhhBench9.Draw("hist")
  histmhhBM9.Scale(7./histmhhBM9.Integral())
  histmhhBM9.SetLineWidth(2)
  histmhhBM9.SetLineColor(8)
  leg.AddEntry(histmhhBM9,"Simulated (from 50k ev)")
  histmhhBM9.Draw("same")
  leg.Draw("same") 
  cs.SaveAs("Bench9.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench10.Scale(7./histmhhBench10.Integral())
  histmhhBench10.SetLineWidth(2)
  histmhhBench10.SetLineColor(1)
  leg.AddEntry(histmhhBench10,"BM8 ; Reweighted")
  histmhhBench10.Draw("hist")
  histmhhBM10.Scale(7./histmhhBM10.Integral())
  histmhhBM10.SetLineWidth(2)
  histmhhBM10.SetLineColor(8)
  leg.AddEntry(histmhhBM10,"Simulated (from 50k ev)")
  histmhhBM10.Draw("same")
  leg.Draw("same,hist") 
  cs.SaveAs("Bench10.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench11.Scale(7./histmhhBench11.Integral())
  histmhhBench11.SetLineWidth(2)
  histmhhBench11.SetLineColor(1)
  leg.AddEntry(histmhhBench11,"BM11 ; Reweighted")
  histmhhBench11.Draw("hist")
  histmhhBM11.Scale(7./histmhhBM11.Integral())
  histmhhBM11.SetLineWidth(2)
  histmhhBM11.SetLineColor(8)
  leg.AddEntry(histmhhBM11,"Simulated (from 50k ev)")
  histmhhBM11.Draw("same")
  leg.Draw("same") 
  cs.SaveAs("Bench11.png") 
  cs.Clear() 
  leg.Clear()
  #############
  histmhhBench12.Scale(7./histmhhBench12.Integral())
  histmhhBench12.SetLineWidth(2)
  histmhhBench12.SetLineColor(1)
  leg.AddEntry(histmhhBench12,"BM8 ; Reweighted")
  histmhhBench12.Draw("hist")
  histmhhBM12.Scale(7./histmhhBM12.Integral())
  histmhhBM12.SetLineWidth(2)
  histmhhBM12.SetLineColor(8)
  leg.AddEntry(histmhhBM12,"Simulated (from 50k ev)")
  histmhhBM12.Draw("same")
  leg.Draw("same,hist") 
  cs.SaveAs("Bench12.png") 
  cs.Clear() 
  leg.Clear()
  ######################################
  histmhhBoxRe.Scale(1./histmhhBoxRe.Integral())
  histmhhBoxRe.SetLineWidth(2)
  histmhhBoxRe.SetLineColor(1)
  histmhhBoxRe.Draw("hist")
  leg.AddEntry(histmhhReA,"reweigted (from analytical)")
  histmhhBox.Sumw2()
  histmhhBox.Scale(1./histmhhBox.Integral())
  histmhhBox.SetLineWidth(2)
  histmhhBox.SetLineColor(8)
  histmhhBox.Draw("same,E2")
  leg.AddEntry(histmhhBox,"Box (from 300k events)")
  leg.Draw("same") 
  cs.SaveAs("Box.png")
  cs.Clear()
  leg.Clear()
  #################################################"
  histmhhL15.Scale(1./histmhhL15.Integral())
  histmhhL15.SetLineWidth(2)
  histmhhL15.SetLineColor(1)
  histmhhL15.Draw("hist")

  histmhhoL15.Sumw2()
  histmhhoL15.Scale(1./histmhhoL15.Integral())
  histmhhoL15.SetLineWidth(2)
  histmhhoL15.SetLineColor(1)
  histmhhoL15.SetLineStyle(2)
  histmhhoL15.Draw("same,hist,E2")
  leg.AddEntry(histmhhL15,"#kappa_{#lambda} = 15")

  histmhhL2p4.Scale(1./histmhhL2p4.Integral())
  histmhhL2p4.SetLineWidth(2)
  histmhhL2p4.SetLineColor(8)
  histmhhL2p4.Draw("same,hist")

  histmhhoL2p4.Sumw2()
  histmhhoL2p4.Scale(1./histmhhoL2p4.Integral())
  histmhhoL2p4.SetLineWidth(2)
  histmhhoL2p4.SetLineColor(8)
  histmhhoL2p4.SetLineStyle(2)
  histmhhoL2p4.Draw("same,hist,E2")
  leg.AddEntry(histmhhL2p4,"#kappa_{#lambda} = 2.5")
  leg.AddEntry(histmhhoL15,"simulation (from 100k events)")
  leg.Draw("same") 
  cs.SaveAs("kl15.png") 
# save histogram
if histdone==0 :
  fileH=ROOT.TFile(outpath+histo2D,"recreate")
  fileH.cd()
  histAnalytical.Write()
  histBench.Write() # coarse binnig
  histBench0.Write()
  fileH.Close()


print "done "
print "Sig ",countSig
