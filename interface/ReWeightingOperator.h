
#pragma once

#include <algorithm>

#include "ComposableSelector.h"
#include "BaseOperator.h"
#include "Event.h"
#include "Utils.h"
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>

  template <class EventClass> class ReWeightingOperator : public BaseOperator<EventClass> {

    public:
      int a_;
      std::string filew_name_;
      std::string osample_;
      std::vector<std::string> sam_list_;
      std::vector<std::string> hist_list_;
      TFile filew_;
      std::vector<TH2F> bench;      
      TH2F normBench;
      TH2F normAnalitical;

      ReWeightingOperator(int a) :
      a_(a)
      {
        // benchmarks to reweight to ( not the ones we have)
        sam_list_ = {"SM","BM1","BM2","BM3","BM4","BM5","BM6",
                    "BM7","BM8","BM9","BM10","BM11","BM12"};

        //######
        //# path to histograms
        //######
	//vector<TH2D *> bench;
        //# to have the SM = the component 0 of the vector bench will be the SM
        TFile *fileSM = TFile::Open("../../../Support/NonResonant/Distros_5p_SM3M_sumBenchJHEP_13TeV.root");
        fileSM= new TFile("../../../Support/NonResonant/Distros_5p_SM3M_sumBenchJHEP_13TeV.root");
        TH2D* dumb = (TH2D* ) fileSM->Get("H0bin1"); //# fine binning (the H0bin2 is with the bin used to analytical);
        bench.push_back(dumb);
        //# Read histograms with JHEP benchmarks
        char htitle2[13];
        TFile *fileH = TFile::Open("../../../Support/NonResonant/Distros_5p_500000ev_12sam_13TeV_JHEP_500K.root");
        for(unsigned int ibench=0; ibench< 12; ibench++) {
             string samplename;
             samplename = std::to_string(ibench);
             sprintf (htitle2,"%s_bin1;1",samplename.c_str());
             TH2D* dumb = (TH2D* ) fileH->Get(htitle2);
             bench.push_back(dumb);
        }
        //# sum of events to normalization
        TFile *fileHH = TFile::Open("../../../Support/NonResonant/Hist2DSum_V0_SM_box.root");
        TH2D* normAnalitical = (TH2D* ) fileHH->Get("SumV0_AnalyticalBin;1");
        //bench.push_back(sumHAnalyticalBin);
        TH2D* normBench = (TH2D* ) fileHH->Get("SumV0_BenchBin;1");
        //bench.push_back(sumHAnalyticalBin);
      }

      virtual ~ReWeightingOperator() {}

      virtual bool process( EventClass & ev ) {

        // weight_map to save event weights for each sample
        std::map<std::string, float> weight_map;

        // inititialize all weights to 1.0 - safety
        for (const auto & sam : sam_list_) {
          // at(syst) would return exception when no element exists
          weight_map["ReWeighting_"+sam] = 1.0;
        }
        weight_map["Norm_Analytical"] = 1.0;
        //example on how to call ev variables
        float costh = ev.tl_genhh_.at(0).costhst();
        float mhh = ev.tl_genhh_.at(0).mass();
        for (unsigned int i=0; i<sam_list_.size(); i++) {

            //code to get weight
            float weight = 1.;
            float mergecostSum = 0;
            int bmhh = normBench.GetXaxis().FindBin(mhh);
            int bcost = normBench.GetYaxis().FindBin(costh);
            for (unsigned int icost=1; icost< 11; icost++)  { mergecostSum+= normBench.GetBinContent(bmhh,icost); }// flat in costS
            if (mergecostSum >0) {
                weight = (bench.at(i).GetBinContent(mhh,costh) / mergecostSum);
            }
            weight_map.at("ReWeighting_"+sam_list_.at(i)) *= weight;           
        }
        int bmhha = normAnalitical.GetXaxis().FindBin(mhh);
        int bcosta = normAnalitical.GetYaxis().FindBin(costh);
        weight_map.at("Norm_Analytical") *= normAnalitical.GetBinContent(bmhha,bcosta);
        // add weights to event info
        for (const auto & weight_pair : weight_map) {
          ev.eventInfo_.weightPairs_.emplace_back(weight_pair);
        }

        return true;
      }

      virtual std::string get_name() {
        auto name = "reweighting";
        return name;
      } 
};
