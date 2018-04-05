//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Apr  3 21:21:49 2018 by ROOT version 6.06/01
// from TChain MVATree/
//////////////////////////////////////////////////////////

#ifndef HistoProducer_h
#define HistoProducer_h


#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TH1.h>
#include <TString.h>
#include <TH2.h>
#include <TStyle.h>
#include <TBranch.h>
#include <TLeaf.h>

// Headers needed by this particular selector


class HistoProducer : public TSelector {
public :
   TTreeReader     fReader;  //!the tree reader
   TTree          *fChain = 0;   //!pointer to the analyzed TTree or TChain
   TFile*          output = 0;
   TString         name = "";
   std::vector<std::unique_ptr<TH1D>> histograms;
   std::vector<TString> variables;
   std::vector<TString> variable_types;
   std::vector<TString> weights;
   std::vector<TString> uncertainties;

   // Readers to access the data (delete the ones you do not need).
   TTreeReaderValue<Float_t> Evt_Pt_MET = {fReader, "Evt_Pt_MET"};
   TTreeReaderArray<Float_t> Neutralino_Pt = {fReader, "Neutralino_Pt"};
   
   //std::vector<TTreeReaderArray<Float_t>> float_values;
   //std::vector<TTreeReaderArray<Long64_t>> int_values;

   HistoProducer(TTree * /*tree*/ =0) { }
   virtual ~HistoProducer() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();
   
   void AddVariable(TString variable);

   //ClassDef(HistoProducer,0);

};

#endif

#ifdef HistoProducer_cxx
void HistoProducer::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the reader is initialized.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   fReader.SetTree(tree);
}

Bool_t HistoProducer::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}


#endif // #ifdef HistoProducer_cxx
