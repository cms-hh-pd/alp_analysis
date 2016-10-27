
#pragma once

#ifndef ComposableSelector_h
#define ComposableSelector_h

#include <vector>
#include <string>
#include <memory>

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TSelector.h>
#include <TTreeReader.h>

#include "BaseOperator.h"




template <class EventClass> class ComposableSelector : public TSelector {

  public:

  long n_entries{0};
  long tot_entries{0};
  double n_genev_{-1};
  double w_xsecbr_{1.};
  double w_eff_{1.};
  double w_kfact_{1.};
  double lumiFb_{1.};

  // associated with a TTree
  TTreeReader reader_;
  // to save output 
  TFile * tfile_{ nullptr}; 

  // to save selector/event configuration
  json config_;

  // event class 
  EventClass ev_; 

  // vector of operations
  std::vector<std::unique_ptr<BaseOperator<EventClass>>> ops_;

  // human readable event origin
  std::string pName_ = "";



  ComposableSelector(TTree * /*tree*/ =0, const std::string & config_s = {}) :
    config_(json::parse(config_s)),
    ev_(reader_, config_)
    {
    }
  virtual ~ComposableSelector() {}

  // return BaseOperator ref so functions can be applied
  virtual BaseOperator<EventClass> & addOperator( BaseOperator<EventClass> * op ) { 
    ops_.emplace_back(op);
    return *ops_.back();
  }

  // TSelector functions
  virtual Int_t   Version() const { return 2; }
  virtual void    Begin(TTree *tree);
  virtual void    SlaveBegin(TTree *tree);
  virtual void    Init(TTree *tree);
  virtual bool    Notify();
  virtual bool    Process(Long64_t entry);
  virtual void    SetOption(const char *option) { fOption = option; }
  virtual void    SetObject(TObject *obj) { fObject = obj; }
  virtual void    SetInputList(TList *input) { fInput = input; }
  virtual TList  *GetOutputList() const { return fOutput; }
  virtual void    SlaveTerminate();
  virtual void    Terminate();

};

#endif

// each new tree is opened
template <class EventClass> void ComposableSelector<EventClass>::Init(TTree *tree)

{
  reader_.SetTree(tree);
  tot_entries = reader_.GetEntries(1);
}

// each new file is opened
template <class EventClass> bool ComposableSelector<EventClass>::Notify()
{

   return kTRUE;
}

/// start of query (executed on client)
template <class EventClass> void ComposableSelector<EventClass>::Begin(TTree * /*tree*/)
{

   std::string option = GetOption();


}

// right after begin (executed on slave)
template <class EventClass> void ComposableSelector<EventClass>::SlaveBegin(TTree * /*tree*/)
{

   std::string option = GetOption();
 
   std::string o_filename = "output.root";
   std::size_t i_ofile = option.find("ofile="); 
   if (i_ofile != std::string::npos) {
     std::size_t length = (option.find(";", i_ofile) -  option.find("=", i_ofile) - 1);
     o_filename = option.substr(option.find("=", i_ofile)+1 , length );
   } 

   pName_ = "";
   std::size_t i_pName = option.find("pName="); 
   if (i_pName != std::string::npos) {
     std::size_t length = (option.find(";", i_pName) -  option.find("=", i_pName) - 1);
     pName_ = option.substr(option.find("=", i_pName)+1 , length );
   } 


   tfile_ = new TFile(o_filename.c_str(), "RECREATE");
 
   // output folder handling
   auto root_dir = dynamic_cast<TDirectory *>(&(*tfile_));
   // use root by default
   auto curr_dir = root_dir;
   for (auto & op : ops_) {
     auto name = op->get_name();
     // if operator name is starts with folder_ use subsequent string 
     // as a name of the folder where to save further output
     if (name.find("folder_") == 0) {
      auto folder_name = name.substr(7);
      curr_dir = root_dir->mkdir(folder_name.c_str());
      if (curr_dir == nullptr) curr_dir = root_dir;
     }
     op->init(curr_dir);
   }

   //write histos with weights and generated events
   TH1D h_genev {"h_genEvts", "num of genrated events", 1, 0., 1.};
   TH1D h_w_XsBrEff {"h_w_XsBrEff", "event weight = xsec*BR*genEff", 1, 0., 1.};

   //hist with number of generated events
   if (config_.find("n_gen_events") != config_.end()) n_genev_ = config_.at("n_gen_events");
   h_genev.SetBinContent(1,n_genev_);

   //hist with event weight = xsec*BR*genEff
   if (config_.find("xsec_br") != config_.end()) w_xsecbr_ = config_.at("xsec_br");
   if (config_.find("matcheff") != config_.end()) w_eff_ = config_.at("matcheff");
   if (config_.find("kfactor") != config_.end()) w_kfact_ = config_.at("kfactor");
   h_w_XsBrEff.SetBinContent(1,w_xsecbr_*w_eff_*w_kfact_);

   //hist with event weight to 1 fb-1

   TH1F* h_w_oneInvFb = (TH1F*)h_w_XsBrEff.Clone("h_w_oneInvFb");
   if (config_.find("lumiFb") != config_.end()) lumiFb_ = config_.at("lumiFb");
   if(config_.at("isData")) h_w_oneInvFb->SetBinContent(1,1./lumiFb_); // isData -> 1/int.Lumi
   else h_w_oneInvFb->Scale(1000./(h_genev.GetBinContent(1))); // weight*1000/genEv -- pb to fb

   h_genev.Write();
   h_w_XsBrEff.Write();
   h_w_oneInvFb->Write();
}


// for each entry of the TTree
template <class EventClass> bool  ComposableSelector<EventClass>::Process(Long64_t entry)
{

  n_entries++;
  if (n_entries>300000 && (n_entries%((int)tot_entries/5)) == 0) std::cout << "processing " << n_entries << " entry" << std::endl; 

  // set TTreeReader entry
  reader_.SetLocalEntry(entry);
  // update event objects
  ev_.update();

  for (auto & op : ops_) {
    if (!op->process(ev_)) return false; 
  }

  return true;
}


// all entries have been processed (executed in slave)
template <class EventClass> void ComposableSelector<EventClass>::SlaveTerminate()
{


   for (auto & op : ops_) {                
     op->output(std::cout); 
   }

   
   for (auto & op : ops_) {                
     op->output(tfile_); 
   } 

   tfile_->Write();


}

// last function called (on client)
template <class EventClass> void ComposableSelector<EventClass>::Terminate()
{

}
