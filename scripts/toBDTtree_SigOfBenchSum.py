#!/usr/bin/env python

histdone=1 # 0 = no
histo2D="HistSum2D_4b_v01_02_2017.root"
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

def CosThetaStar(diphoton, DiJets):
  boost_H = -DiJets.BoostVector()
  diphoton.Boost(boost_H)
  diphoton_vect = diphoton.Vect().Unit()
  #fCSaxis = CSaxis(DiJets)
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
#path = "/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/alpha_ntuples/v01_02_2017/def_cmva/" # signal
#path = "/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/alpha_ntuples/v01_02_2017/def_cmva_mixed/" 
#path = "/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/alpha_ntuples/v01_02_2017/def_cmva_JESup/" 


#path = "/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/alpha_ntuples/v01_02_2017/def_cmva_moriond/"
path = "/afs/cern.ch/work/a/acarvalh/codeCMSHHH4b/toHH4b/alpha_ntuples/v01_02_2017/def_cmva_moriond_mixed/"

data="../../../HHStatAnalysis/AnalyticalModels/data/"
model = NonResonantModel()
# obtaining BSM/SM coeficients
dumb = model.ReadCoefficients("../../../HHStatAnalysis/AnalyticalModels/data/coefficientsByBin_klkt.txt")  

"""
Data = 1
fileoutput = "HHTo4B_SM_tree.root"
files = []
endfile = ".root"
files.append("HHTo4B_SM")
#files.append("HHTo4B_BMbox")
#for ifile in range(2,14) : files.append("HHTo4B_BM"+str(ifile))
########## add TCheins instead of loop in events
fileout=ROOT.TFile(path+fileoutput,"recreate")
cdtof = fileout.mkdir("pair")
#cdtof.cd()
tchain = TChain("pair/tree")    
for ifile in range(0,1) : tchain.Add(path+files[ifile]+endfile)
clone = tchain.CloneTree(0)


Data = 0
fileoutput = "HHTo4B_SM_tree.root"
files = []
endfile = ".root"
files.append("HHTo4B_SM")
#files.append("HHTo4B_BMbox")
#for ifile in range(2,14) : files.append("HHTo4B_BM"+str(ifile))
########## add TCheins instead of loop in events
fileout=ROOT.TFile(path+fileoutput,"recreate")
cdtof = fileout.mkdir("pair")
#cdtof.cd()
tchain = TChain("pair/tree")    
for ifile in range(0,14) : tchain.Add(path+files[ifile]+endfile)
clone = tchain.CloneTree(0)
"""

Data = 1
fileoutput = "BTagCSVRun2016_moriond_weight.root"
files = []
endfile = ".root"
files.append("BTagCSVRun2016_")
########## add TCheins instead of loop in events
fileout=ROOT.TFile(path+fileoutput,"recreate")
cdtof = fileout.mkdir("pair")
#cdtof.cd()
tchain = TChain("pair/tree")    
tchain.Add(path+files[0]+endfile)
clone = tchain.CloneTree(0)


# balanced samples to the BDT training
balanceSM=0.02734
balanceData=184879   
#balanceData=66281 #53140

# to analytical re
# We sum SM + box + the benchmarks from 2-13 
# read the 2D histo referent to the sum of events
fileHH=ROOT.TFile("../../../Support/NonResonant/Hist2DSum_V0_SM_box.root") # outpath+histo2D ) #
sumHAnalyticalBin = fileHH.Get("SumV0_AnalyticalBin")
sumHBenchBin = fileHH.Get("SumV0_AnalyticalBin")

countSig=np.zeros((15)) 
normSig= np.ones((15)) 
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
  sumData=0
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
  sumHBenchBin = fileHH.Get("SumV0_BenchBin")
  sumHAnalyticalBin = fileHH.Get("SumV0_AnalyticalBin")
  print "Sum to Bench hist ",sumHBenchBin.GetNbinsX(),sumHBenchBin.GetNbinsY(),sumHBenchBin.Integral()
  # check mhh hist to SM
  histmhhRe = ROOT.TH1D('MhhRe', '', 30,200.,1000.) 
  histmhhSM = ROOT.TH1D('MhhSM', '', 30,200.,1000.) 
  histmhhReA = ROOT.TH1D('MhhSMA', '', 30,200.,1000.) 
  histmhhBox = ROOT.TH1D('MhhBox', '', 30,200.,1000.) 
  histmhhBoxA = ROOT.TH1D('MhhBoxA', '', 30,200.,1000.) 

  histmhhRecoRe = ROOT.TH1D('MhhRecoRe', '', 20,50.,1000.) 
  histmhhRecoSM = ROOT.TH1D('MhhRecoSM', '', 20,50.,1000.) 
  histmhhRecoReA = ROOT.TH1D('MhhSMRecoA', '', 20,50.,1000.) 
  histmhhRecoBox = ROOT.TH1D('MhhBoxReco', '', 20,50.,1000.) 
  histmhhRecoBoxA = ROOT.TH1D('MhhBoxRecoA', '', 20,50.,1000.) 

  histptRecoRe = ROOT.TH1D('pthhRecoRe', '', 20,0.,700.) 
  histptRecoSM = ROOT.TH1D('pthhRecoSM', '', 20,0.,700.) 
  histptRecoReA = ROOT.TH1D('pthhSMRecoA', '', 20,0.,700.) 
  histptRecoBox = ROOT.TH1D('pthhBoxReco', '', 20,0.,700.) 
  histptRecoBoxA = ROOT.TH1D('pthhBoxRecoA', '', 20,0.,700.) 

  histmhhL15 = ROOT.TH1D('MhhL15', '', 30,200.,1000.) 
  histmhhBench1 = ROOT.TH1D('MhhBench1', '', 30,0.,1000.) 

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
  print "SM hist ",histSM.GetNbinsX(),histSM.GetNbinsY(),histSM.Integral(),histSM.GetXaxis().GetBinLowEdge(1),histSM.GetXaxis().GetBinUpEdge(xaxis.GetNbins())
  print "Sum hist ",sumHBenchBin.GetNbinsX(),sumHBenchBin.GetNbinsY(),sumHBenchBin.Integral(),sumHBenchBin.GetXaxis().GetBinLowEdge(1),sumHBenchBin.GetXaxis().GetBinUpEdge(sumHBenchBin.GetXaxis().GetNbins())
  print "Sum hist Analytical ",sumHAnalyticalBin.GetNbinsX(),sumHAnalyticalBin.GetNbinsY(),sumHAnalyticalBin.Integral(),sumHAnalyticalBin.GetXaxis().GetBinLowEdge(1),sumHAnalyticalBin.GetXaxis().GetBinUpEdge(sumHAnalyticalBin.GetXaxis().GetNbins())
  #histSM.Draw("colz")
  ##############################################
  # do one file with events to proceed
  #auto & weightPairs = EventInfo.weightPairs_
  #weightPairs.emplace_back("XXXWeight", XXXWeight);
  Genmhh = np.zeros(1, dtype=float)
  GenHHCost = np.zeros(1, dtype=float) 
  # weight benchmarks JHEP
  effSumV0AnalyticalBin = np.zeros(1, dtype=float)
  weightBtag = np.zeros(1, dtype=float)
  weightPU = np.zeros(1, dtype=float)
  HHmx = np.zeros(1, dtype=float)
  HHmhh = np.zeros(1, dtype=float)
  HHpt = np.zeros(1, dtype=float)
  HHcosts = np.zeros(1, dtype=float)

  H1mass = np.zeros(1, dtype=float)
  H2mass = np.zeros(1, dtype=float)
  H1dr = np.zeros(1, dtype=float)
  H2dr = np.zeros(1, dtype=float)
  H1costs = np.zeros(1, dtype=float)
  H2costs = np.zeros(1, dtype=float)
  H1Dphi = np.zeros(1, dtype=float)
  H2Dphi = np.zeros(1, dtype=float)

  j1eta = np.zeros(1, dtype=float)
  j2eta = np.zeros(1, dtype=float)
  j3eta = np.zeros(1, dtype=float)
  j4eta = np.zeros(1, dtype=float)

  j1pt = np.zeros(1, dtype=float)
  j2pt = np.zeros(1, dtype=float)
  j3pt = np.zeros(1, dtype=float)
  j4pt = np.zeros(1, dtype=float)

  HTfull = np.zeros(1, dtype=float)
  HTrest = np.zeros(1, dtype=float)
  CMVA3 = np.zeros(1, dtype=float)
  CMVA4 = np.zeros(1, dtype=float)

  ################################################################

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
  #################################################
  clone.Branch('weightBtag', weightBtag, 'weightBtag/D')
  clone.Branch('weightPU', weightPU, 'weightPU/D')
  clone.Branch('HHmx', HHmx, 'HHmx/D')
  clone.Branch('HHmhh', HHmhh, 'HHmhh/D')
  clone.Branch('HHpt', HHpt, 'HHpt/D')
  clone.Branch('HHcosts', HHmhh, 'HHcosts/D')

  clone.Branch('H1mass', H1mass, 'H1mass/D')
  clone.Branch('H2mass', H2mass, 'H2mass/D')
  clone.Branch('H2costs', H2costs, 'H2costs/D')
  clone.Branch('H1dr', H1dr, 'H1dr/D')
  clone.Branch('H2dr', H2dr, 'H2dr/D')
  clone.Branch('H1costs', H1costs, 'H1costs/D')
  clone.Branch('H2costs', H2costs, 'H2costs/D')
  clone.Branch('H1Dphi', H1Dphi, 'H1Dphi/D')
  clone.Branch('H2Dphi', H2Dphi, 'H2Dphi/D')

  clone.Branch('j1eta', j1eta, 'j1eta/D')
  clone.Branch('j2eta', j2eta, 'j2eta/D')
  clone.Branch('j3eta', j3eta, 'j3eta/D')
  clone.Branch('j4eta', j4eta, 'j4eta/D')

  clone.Branch('j1pt', j1pt, 'j1pt/D')
  clone.Branch('j2pt', j2pt, 'j2pt/D')
  clone.Branch('j3pt', j3pt, 'j3pt/D')
  clone.Branch('j4pt', j4pt, 'j4pt/D')

  clone.Branch('HTfull', HTfull, 'HTfull/D')
  clone.Branch('HTrest', HTrest, 'HTrest/D')
  clone.Branch('CMVA3', CMVA3, 'CMVA3/D')
  clone.Branch('CMVA4', CMVA4, 'CMVA4/D')

  #auto & weightPairs = EventInfo.weightPairs_
  #weightPairs.emplace_back("weightSM", weightSM)
  clone.Branch('Genmhh', Genmhh, 'Genmhh/D')
  clone.Branch('GenHHCost', GenHHCost, 'GenHHCost/D')
  clone.Branch('effSumV0AnalyticalBin', effSumV0AnalyticalBin, 'effSumV0AnalyticalBin/D') # I could save the bin here
  clone.Branch('weightSM', weightSM, 'weightSM/D')
  clone.Branch('weightSMA', weightSMA, 'weightSMA/D')
  clone.Branch('weight1', weight1, 'weight1/D')
  clone.Branch('weight2', weight2, 'weight2/D')
  clone.Branch('weight3', weight3, 'weight3/D')
  clone.Branch('weight4', weight4, 'weight4/D')
  clone.Branch('weight5', weight5, 'weight5/D')
  clone.Branch('weight6', weight6, 'weight6/D')
  clone.Branch('weight7', weight7, 'weight7/D')
  clone.Branch('weight8', weight8, 'weight8/D')
  clone.Branch('weight9', weight9, 'weight9/D')
  clone.Branch('weight10', weight10, 'weight10/D')
  clone.Branch('weight11', weight11, 'weight11/D')
  clone.Branch('weight12', weight12, 'weight12/D')
  # lamda scan
  clone.Branch('weightL0', weightL0, 'weightL0/D')
  clone.Branch('weightL0p5', weightL0p5, 'weightL0p5/D')
  clone.Branch('weightL2', weightL2, 'weightL2/D')
  clone.Branch('weightL2p4', weightL2p4, 'weightL2p4/D')
  clone.Branch('weightL3', weightL3, 'weightL3/D')
  clone.Branch('weightL4', weightL4, 'weightL4/D')
  clone.Branch('weightL5', weightL5, 'weightL5/D')
  clone.Branch('weightL7', weightL7, 'weightL7/D')
  clone.Branch('weightL10', weightL10, 'weightL10/D')
  clone.Branch('weightL12p5', weightL12p5, 'weightL12p5/D')
  clone.Branch('weightL15', weightL15, 'weightL15/D')
  clone.Branch('weightL20', weightL20, 'weightL20/D')
  clone.Branch('weightLm1', weightLm1, 'weightLm1/D')
  clone.Branch('weightLm2p4', weightLm2p4, 'weightLm2p4/D')
  clone.Branch('weightLm3', weightLm3, 'weightLm3/D')
  clone.Branch('weightLm4', weightLm4, 'weightLm4/D')
  clone.Branch('weightLm5', weightLm5, 'weightLm5/D')
  clone.Branch('weightLm7', weightLm7, 'weightLm7/D')
  clone.Branch('weightLm10', weightLm10, 'weightLm10/D')
  clone.Branch('weightLm12p5', weightLm12p5, 'weightLm12p5/D')
  clone.Branch('weightLm15', weightLm15, 'weightLm15/D')
  clone.Branch('weightLm20', weightLm20, 'weightLm20/D')
#########################################################
normBench = [ 49976.6016382, 50138.2521798, 49990.0468825, 49993.1979924, 50041.0282539, 50038.5462286, 101.036904355, 50000.3090638, 50045.3506862, 49992.1242267, 50024.7055638, 50006.2937198]
normSM = 299803.461384
normSManal =  1.0
if histdone==1 :
  listLam=[0.0001,0.5,2, 2.5, 3.0, 4.0, 4.0, 5.0, 7.0, 10.0, 12.5, 15.0, 20.0, -1.0,-2.4, -3.0, -4.0, -5.0, -7.0, -10.0, -12.5, -15.0, -20.0]
  normL =[] 
  for ii in range(0,len(listLam)): normL.append(model.getNormalization(float(listLam[ii]),1.0,sumHAnalyticalBin))

##############################################################
# loop in all events
countevent=0
if 1 > 0 :  
  nev = tchain.GetEntries()
  print nev
  counter=0
  #if ifile==16 : treeout.Fill()
  for iev in range(0,nev) :    
    tchain.LoadTree(iev);
    tchain.GetEntry(iev)
    njets=tchain.Jets.size()
    if Data == 0 :
      #genMhh = tchain.TL_GenHH.p4_.M()
      #genCost=tchain.TL_GenHH.costhst_
      GenPH1 = ROOT.TLorentzVector()
      GenPH1.SetPxPyPzE(tchain.TL_GenHs.at(0).p4_.Px(),tchain.TL_GenHs.at(0).p4_.Py(),tchain.TL_GenHs.at(0).p4_.Pz(),tchain.TL_GenHs.at(0).p4_.E())
      GenPH2 = ROOT.TLorentzVector()
      GenPH2.SetPxPyPzE(tchain.TL_GenHs.at(1).p4_.Px(),tchain.TL_GenHs.at(1).p4_.Py(),tchain.TL_GenHs.at(1).p4_.Pz(),tchain.TL_GenHs.at(1).p4_.E())
      GenPHH = ROOT.TLorentzVector()
      GenPHH = GenPH1 + GenPH2
      genMhh =  GenPHH.M()
      genCost=CosThetaStar(GenPH1, GenPHH)
    elif Data == 1 :
      genMhh = -100
      genCost=-100
    ####################################
    if Data == 0 :
      weightBtag[0] = tchain.EventInfo.getWeightC("BTagWeight") 
      # in Tbrowser: tchain.Scan("EventInfo.getWeightC(\"PUWeight\")")
      weightPU[0] = tchain.EventInfo.getWeightC("PUWeight" ) 
    elif Data == 1 :
      weightBtag[0] = 1
      weightPU[0] = 1 


    H1mass[0] = tchain.DiJets[0].mass()
    H2mass[0] = tchain.DiJets[1].mass()

    HHmx[0] = tchain.DiHiggs[0].p4_.mass() - H1mass[0] - H2mass[0]+ 250
    HHmhh[0] = tchain.DiHiggs[0].p4_.mass()
    HHpt[0] = tchain.DiHiggs[0].p4_.pt()
    HHcosts[0] = tchain.DiHiggs[0].costhst()

    H1dr[0] = tchain.DiJets[0].dr()
    H2dr[0] = tchain.DiJets[1].dr()
    H1costs[0] = tchain.DiJets[0].costhst()
    H2costs[0] = tchain.DiJets[1].costhst()
    H1Dphi[0] = tchain.DiJets[0].dphi()
    H2Dphi[0] = tchain.DiJets[1].dphi()

    j1eta[0] = tchain.Jets[0].eta()
    j2eta[0] = tchain.Jets[1].eta()
    j3eta[0] = tchain.Jets[2].eta()
    j4eta[0] = tchain.Jets[3].eta()

    j1pt[0] = tchain.Jets[0].pt()
    j2pt[0] = tchain.Jets[1].pt()
    j3pt[0] = tchain.Jets[2].pt()
    j4pt[0] = tchain.Jets[3].pt()

    HTfull[0] = 1 #Sum$(Jets.pt())
    HTrest[0] = 1 #Sum$(Jets.pt())
    CMVA3[0] = tchain.Jets[2].CMVA()
    CMVA4[0] = tchain.Jets[3].CMVA()

    # make weights to benchmarks
    Genmhh[0] = genMhh
    if Data == 0 :
      # find the bin the event belong
      bmhh = histSM.GetXaxis().FindBin(genMhh)
      bcost = histSM.GetYaxis().FindBin(genCost)
      #print sumHBenchBin.GetBinContent(bmhh,bcost),bmhh,bcost 
      mergecostSum = 0
      for ii in range(1,11) : mergecostSum+= sumHBenchBin.GetBinContent(bmhh,ii) 
      if mergecostSum >0 : # to be done with all events
         weightSM[0] = ((histSM.GetBinContent(bmhh,bcost) / mergecostSum)/normSM ) / balanceSM
         weight1[0] = (bench[0].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[0]  
         weight2[0] = (bench[1].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[1] 
         weight3[0] = (bench[2].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[2]   
         weight4[0] = (bench[3].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[3]   
         weight5[0] = (bench[4].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[4]   
         weight6[0] = (bench[5].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[5]   
         weight7[0] = (bench[6].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[6]   
         weight8[0] = (bench[7].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[7]   
         weight9[0] = (bench[8].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[8]   
         weight10[0] = (bench[9].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[9]   
         weight11[0] = (bench[10].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[10]  
         weight12[0] = (bench[11].GetBinContent(bmhh,bcost) / mergecostSum)/normBench[11]    
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
      if sumHAnalyticalBin.GetBinContent(bmhh,bcost) >0 : # to be done with all events
         # find the Nevents from the sum of events on that bin
         effSumV0 = sumHAnalyticalBin.GetBinContent(bmhh,bcost)  # quantity of simulated events in that bin (without cuts)
         weightSMA[0] = ( model.getScaleFactor(mhhcost,1.0, 1.0, effSumV0) ) / balanceSM
         sumWSMA+=weightSMA[0]
         # lambda scan
         weightL0[0] = model.getScaleFactor(mhhcost, 0.0001,1.0, effSumV0) / normL[0]
         weightL0p5[0] = model.getScaleFactor(mhhcost, 0.5,1.0, effSumV0) / normL[1]
         weightL2[0] = model.getScaleFactor(mhhcost, 2,1.0, effSumV0) / normL[2]
         weightL2p4[0] = model.getScaleFactor(mhhcost, 2.5,1.0, effSumV0) / normL[3]
         weightL3[0] = model.getScaleFactor(mhhcost, 3.0,1.0, effSumV0) / normL[4]
         weightL4[0] = model.getScaleFactor(mhhcost, 4.0,1.0, effSumV0) / normL[5]
         weightL5[0] = model.getScaleFactor(mhhcost, 5.0,1.0, effSumV0) / normL[6]
         weightL7[0] = model.getScaleFactor(mhhcost, 7.0,1.0, effSumV0) / normL[7]
         weightL10[0] = model.getScaleFactor(mhhcost, 10.0,1.0, effSumV0) / normL[8]
         weightL12p5[0] = model.getScaleFactor(mhhcost, 12.5,1.0, effSumV0) / normL[9]
         weightL15[0] = model.getScaleFactor(mhhcost, 15.0,1.0, effSumV0) / normL[10]
         weightL20[0] = model.getScaleFactor(mhhcost, 20.0,1.0, effSumV0) / normL[11]
         weightLm1[0] = model.getScaleFactor(mhhcost, -1.0,1.0, effSumV0) / normL[12]
         weightLm2p4[0] = model.getScaleFactor(mhhcost,-2.4,1.0, effSumV0) / normL[13] 
         weightLm3[0] = model.getScaleFactor(mhhcost, -3.0,1.0, effSumV0) / normL[14]
         weightLm4[0] = model.getScaleFactor(mhhcost, -4.0,1.0, effSumV0) / normL[15]
         weightLm5[0] = model.getScaleFactor(mhhcost, -5.0,1.0, effSumV0) / normL[16]
         weightLm7[0] = model.getScaleFactor(mhhcost, -7.0,1.0, effSumV0) / normL[17]
         weightLm10[0] = model.getScaleFactor(mhhcost, -10.0,1.0, effSumV0) / normL[18]
         weightLm12p5[0] = model.getScaleFactor(mhhcost, -12.5,1.0, effSumV0) / normL[19]
         weightLm15[0] = model.getScaleFactor(mhhcost, -15.0,1.0, effSumV0) / normL[20]
         weightLm20[0] = model.getScaleFactor(mhhcost, -20.0,1.0, effSumV0) / normL[21]
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
      # make histogram to test
      histmhhReA.Fill(genMhh,weightSMA[0])
      histmhhRe.Fill(genMhh,weightSM[0])
      histmhhBoxA.Fill(genMhh,weightL0[0])
      histmhhBench1.Fill(genMhh,weight1[0])
      histmhhL15.Fill(genMhh,weightL15[0])
      countevent+=1

      histmhhRecoReA.Fill(HHmhh[0],weightSMA[0])
      histmhhRecoRe.Fill(HHmhh[0],weightSM[0])
      histmhhRecoBoxA.Fill(HHmhh[0],weightL0[0])
      histptRecoReA.Fill(HHpt[0],weightSMA[0])
      histptRecoRe.Fill(HHpt[0],weightSM[0])
      histptRecoBoxA.Fill(HHpt[0],weightL0[0])
    elif Data ==1 :
         weightSMA[0] = 1./balanceData
         weightSM[0] = 1./balanceData 
         sumData+=weightSM[0]
         weight1[0] = 1./balanceData 
         weight2[0] = 1./balanceData 
         weight3[0] = 1./balanceData   
         weight4[0] = 1./balanceData   
         weight5[0] = 1./balanceData   
         weight6[0] = 1./balanceData   
         weight7[0] = 1./balanceData  
         weight8[0] = 1./balanceData   
         weight9[0] = 1./balanceData  
         weight10[0] = 1./balanceData   
         weight11[0] = 1./balanceData 
         weight12[0] = 1./balanceData   
    clone.Fill()
  print counter
print countevent
############# make histograms with SM and BOx simulated to check
if Data == 0 :
 for ifile in range(0,2) : #  len(files)  
  print path+files[ifile]+endfile
  file=ROOT.TFile(path+files[ifile]+endfile)
  tree=file.pair.Get("tree")
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
    bmhh = histSM.GetXaxis().FindBin(GenPHH.M())
    bcost = histSM.GetYaxis().FindBin(CosThetaStar(GenPH1, GenPHH))
    mergecostSum = 0
    for ii in range(1,11) : mergecostSum+= sumHBenchBin.GetBinContent(bmhh,ii) 
    if mergecostSum >0 : # to be done with all events
         weightSM[0] = (histSM.GetBinContent(bmhh,bcost) / mergecostSum)/normSM 
    if sumHAnalyticalBin.GetBinContent(bmhh,bcost) >0 : # to be done with all events
         # find the Nevents from the sum of events on that bin
         effSumV0 = sumHAnalyticalBin.GetBinContent(bmhh,bcost)  # quantity of simulated events in that bin (without cuts)
         weightSMA[0] = model.getScaleFactor(mhhcost,1.0, 1.0, effSumV0) 
         weightL0[0] = model.getScaleFactor(mhhcost, 0.0001,1.0, effSumV0) / normL[0]
    ### reco variables to test 
    PH1 = ROOT.TLorentzVector()
    PH1.SetPxPyPzE(tree.DiJets.at(0).p4_.Px(),tree.DiJets.at(0).p4_.Py(),tree.DiJets.at(0).p4_.Pz(),tree.DiJets.at(0).p4_.E())
    PH2 = ROOT.TLorentzVector()
    PH2.SetPxPyPzE(tree.DiJets.at(1).p4_.Px(),tree.DiJets.at(1).p4_.Py(),tree.DiJets.at(1).p4_.Pz(),tree.DiJets.at(1).p4_.E())
    PHH = ROOT.TLorentzVector()
    PHH = PH1 + PH2
    if ifile ==0 : 
       histmhhSM.Fill(GenPHH.M())
       histmhhRecoSM.Fill(PHH.M())
       histptRecoSM.Fill(PHH.Pt())
    if ifile ==1 : 
       histmhhBox.Fill(GenPHH.M())
       histmhhRecoBox.Fill(PHH.M())
       histptRecoBox.Fill(PHH.Pt())

# save tree of events
fileout.pair.WriteTObject(clone) #.Write("",ROOT.TObject::kOverwrite)
fileout.Write()
fileout.Close()
print sumData
# make histograms
if Data == 0 :
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
  #fileout = clone.GetCurrentFile()
  # Write selected data to output disk file
  #print  clone.GetEntries()
  cs=ROOT.TCanvas("cs","cs",10,10,500,500)
  leg = ROOT.TLegend(0.5,0.60,0.99,0.99);
  ########################
  histmhhRe.Scale(1./histmhhRe.Integral())
  histmhhRe.SetLineWidth(2)
  histmhhRe.SetLineColor(1)
  histmhhRe.GetXaxis().SetTitle("SM Gen Mhh ")
  histmhhRe.Draw()
  leg.AddEntry(histmhhRe,"reweigted (from hist)")
  histmhhReA.Scale(1./histmhhReA.Integral())
  histmhhReA.SetLineWidth(2)
  histmhhReA.SetLineColor(2)
  histmhhReA.Draw("same")
  leg.AddEntry(histmhhReA,"reweigted (from analitical)")
  histmhhSM.Sumw2()
  histmhhSM.Scale(1./histmhhSM.Integral())
  histmhhSM.SetLineWidth(2)
  histmhhSM.SetLineColor(8)
  histmhhSM.Draw("same,E")
  leg.AddEntry(histmhhSM,"SM")
  leg.Draw("same")
  cs.SaveAs("SM_Gen_MHH_afterCuts.png") 
  cs.Clear()
  leg.Clear()
  ########################
  histmhhRecoRe.Scale(1./histmhhRecoRe.Integral())
  histmhhRecoRe.SetLineWidth(2)
  histmhhRecoRe.SetLineColor(1)
  histmhhRecoRe.GetXaxis().SetTitle("SM Reco Mhh ")
  histmhhRecoRe.Draw()
  leg.AddEntry(histmhhRecoRe,"reweigted (from hist)")
  histmhhRecoReA.Scale(1./histmhhRecoReA.Integral())
  histmhhRecoReA.SetLineWidth(2)
  histmhhRecoReA.SetLineColor(2)
  histmhhRecoReA.Draw("same")
  leg.AddEntry(histmhhRecoReA,"reweigted (from analitical)")
  histmhhRecoSM.Sumw2()
  histmhhRecoSM.Scale(1./histmhhRecoSM.Integral())
  histmhhRecoSM.SetLineWidth(2)
  histmhhRecoSM.SetLineColor(8)
  histmhhRecoSM.Draw("same,E")
  leg.AddEntry(histmhhRecoSM,"SM")
  leg.Draw("same")
  cs.SaveAs("SM_Reco_MHH_afterCuts.png") 
  cs.Clear()
  leg.Clear()
  ########################
  histptRecoRe.Scale(1./histptRecoRe.Integral())
  histptRecoRe.SetLineWidth(2)
  histptRecoRe.SetLineColor(1)
  histptRecoRe.GetXaxis().SetTitle("SM Reco pthh ")
  histptRecoRe.Draw()
  leg.AddEntry(histptRecoRe,"reweigted (from hist)")
  histptRecoReA.Scale(1./histptRecoReA.Integral())
  histptRecoReA.SetLineWidth(2)
  histptRecoReA.SetLineColor(2)
  histptRecoReA.Draw("same")
  leg.AddEntry(histptRecoReA,"reweigted (from analitical)")
  histptRecoSM.Sumw2()
  histptRecoSM.Scale(1./histptRecoSM.Integral())
  histptRecoSM.SetLineWidth(2)
  histptRecoSM.SetLineColor(8)
  histptRecoSM.Draw("same,E")
  leg.AddEntry(histmhhRecoSM,"SM")
  leg.Draw("same")
  cs.SaveAs("SM_Reco_ptHH_afterCuts.png") 
  cs.Clear()
  leg.Clear()
  ###########################
  histmhhBox.Sumw2()
  histmhhBox.Scale(1./histmhhBox.Integral())
  histmhhBox.SetLineWidth(2)
  histmhhBox.SetLineColor(8)
  histmhhBox.GetXaxis().SetTitle("Gen Mhh ")
  histmhhBox.Draw("E")
  leg.AddEntry(histmhhBox,"#kappa_{#lambda} = 0")
  histmhhBoxA.Scale(1./histmhhBoxA.Integral())
  histmhhBoxA.SetLineWidth(2)
  histmhhBoxA.SetLineColor(1)
  histmhhBoxA.Draw("same")
  leg.AddEntry(histmhhBoxA,"reweigted (from analitical)")
  leg.Draw("same")
  cs.SaveAs("Box_Gen_MHH_afterCuts.png") 
  cs.Clear()
  leg.Clear()
  ###########################
  histmhhRecoBox.Sumw2()
  histmhhRecoBox.Scale(1./histmhhRecoBox.Integral())
  histmhhRecoBox.SetLineWidth(2)
  histmhhRecoBox.SetLineColor(8)
  histmhhRecoBox.GetXaxis().SetTitle("Reco Mhh ")
  histmhhRecoBox.Draw("E")
  leg.AddEntry(histmhhRecoBox,"#kappa_{#lambda} = 0")
  histmhhRecoBoxA.Scale(1./histmhhRecoBoxA.Integral())
  histmhhRecoBoxA.SetLineWidth(2)
  histmhhRecoBoxA.SetLineColor(1)
  histmhhRecoBoxA.Draw("same")
  leg.AddEntry(histmhhRecoBoxA,"reweigted (from analitical)")
  leg.Draw("same")
  cs.SaveAs("Box_Reco_mHH_afterCuts.png") 
  cs.Clear()
  leg.Clear()
  ###########################
  histptRecoBox.Sumw2()
  histptRecoBox.Scale(1./histptRecoBox.Integral())
  histptRecoBox.SetLineWidth(2)
  histptRecoBox.SetLineColor(8)
  histptRecoBox.GetXaxis().SetTitle("Reco pthh ")
  histptRecoBox.Draw("E")
  leg.AddEntry(histmhhRecoBox,"#kappa_{#lambda} = 0")
  histptRecoBoxA.Scale(1./histptRecoBoxA.Integral())
  histptRecoBoxA.SetLineWidth(2)
  histptRecoBoxA.SetLineColor(1)
  histptRecoBoxA.Draw("same")
  leg.AddEntry(histmhhRecoBoxA,"reweigted (from analitical)")
  leg.Draw("same")
  cs.SaveAs("Box_Reco_ptHH_afterCuts.png") 
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
  ######## save the chain


print "done "
print "Sig ",countSig



