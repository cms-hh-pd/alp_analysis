
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

      std::string w_fname_SM_;
      std::string w_fname_BM_; 
      std::string w_fname_HH_;
      std::vector<std::string> sam_list_;
      std::vector<double> sam_norm_;
      std::vector<std::string> hist_list_;
      TFile * wfile_SM_;
      TFile * wfile_BM_;
      TFile * wfile_HH_;
      std::vector<TH2D*> hw_;
      TH2D * normAnalitical_;
      TH2D * normBench_;     
      TH2D * h_;  

      ReWeightingOperator(const std::string & w_fname_SM, const std::string & w_fname_BM, const std::string & w_fname_HH) : 
       w_fname_SM_(w_fname_SM),
       w_fname_BM_(w_fname_BM),
       w_fname_HH_(w_fname_HH)
      {           
	    sam_list_ = {"SM","BM1","BM2","BM3","BM4","BM5", "BM6",
                     "BM7","BM8","BM9","BM10","BM11","BM12"}; //"BM6", "BMbox"
            sam_norm_ = {299803.461384, 49976.6016382, 50138.2521798, 49990.0468825, 573.0, 50041.0282539, 50038.5462286, 50001.0693263, 50000.3090638, 50045.3506862, 49992.1242267, 50024.7055638, 50006.2937198};

        //get histogram related to sample
        wfile_SM_ = TFile::Open(w_fname_SM_.c_str());
        if (!wfile_SM_) std::cout << "ERROR: file " << w_fname_SM_ << " does not exist" << std::endl;
	    wfile_BM_ = TFile::Open(w_fname_BM_.c_str());
        if (!wfile_BM_) std::cout << "ERROR: file " << w_fname_BM_ << " does not exist" << std::endl;
     	wfile_HH_ = TFile::Open(w_fname_HH_.c_str());
        if (!wfile_HH_) std::cout << "ERROR: file " << w_fname_HH_ << " does not exist" << std::endl;

        h_ = (TH2D*)wfile_SM_->Get("H0bin1");
        if(!h_) std::cout << "ERROR: H0bin1 does not exist" << std::endl;
        hw_.push_back(h_);
        for (unsigned int i=0; i<12; i++) { //#debug
          std::string st = std::to_string(i)+"_bin1";
	      h_ = (TH2D*)wfile_BM_->Get(st.c_str());
          if(!h_) std::cout << "ERROR: bm h does not exist" << std::endl;
          hw_.push_back(h_); 
    	}
	    normBench_ = (TH2D*)wfile_HH_->Get("SumV0_BenchBin");
        if(!normBench_) std::cout << "ERROR: SumV0_BenchBin does not exist" << std::endl;
    	normAnalitical_ = (TH2D*)wfile_HH_->Get("SumV0_AnalyticalBin");
        if(!normAnalitical_) std::cout << "ERROR: SumV0_AnalyticalBin does not exist" << std::endl;

        wfile_SM_->Close();
        wfile_BM_->Close();
        wfile_HH_->Close();
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

        // get variables and bins value
        float costh, mhh;
        int bin, bin_a; 
        //std::cout << ev.tl_genhh_.size() << std::endl;
        if(ev.tl_genhh_.size()){
          mhh = ev.tl_genhh_.at(0).mass();
          costh = ev.tl_genhh_.at(0).costhst();
          bin   = normBench_->FindBin(mhh,costh);
          bin_a = normAnalitical_->FindBin(mhh,costh);
          //std::cout << "bin " << bin << std::endl;
          //std::cout << "mass " << mhh << std::endl;
          //std::cout << "costhst " << costh << std::endl;

        }
        else {
          std::cout << "ERROR: null size of ev.tl_genhh_" << std::endl;
          return false;
        }

        //code to get weight
        for (unsigned int i=0; i<sam_list_.size(); i++) {
            float weight = 1.;
            float mergecostSum = 0;
            for (unsigned int icost=1; icost< 11; icost++){
 	          int binx_c = normBench_->GetXaxis()->FindBin(mhh);
              mergecostSum+= normBench_->GetBinContent(binx_c, icost);
            }
            if (mergecostSum>0) {
              float w = hw_.at(i)->GetBinContent(bin);
              weight = (w / mergecostSum)/sam_norm_.at(i);
              //std::cout << "w " << w << std::endl;
              //std::cout << "mergecostSum " << mergecostSum << std::endl;
              //std::cout << "weight " << weight << std::endl;
            }
            weight_map.at("ReWeighting_"+sam_list_.at(i)) *= weight;  //DEBUG - weight 1 for SM         
        }
        //std::cout << normAnalitical_->GetBinContent(bin_a) << std::endl;
        weight_map.at("Norm_Analytical") *= normAnalitical_->GetBinContent(bin_a);

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
