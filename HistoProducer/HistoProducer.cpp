#define HistoProducer_cxx
// The class definition in HistoProducer.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.


// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("HistoProducer.C")
// root> T->Process("HistoProducer.C","some options")
// root> T->Process("HistoProducer.C+")
//


#include "HistoProducer.hpp"


void HistoProducer::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
   output = new TFile("histograms.root","RECREATE");
}

void HistoProducer::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
   for(const auto& variable : variables){
        //std::unique_ptr<TH1D> histogram;
        //histogram.reset(new TH1D(variable,variable,20,0,0));
        //histogram->Sumw2();
        //GetOutputList()->Add(histogram.get());
        //histograms.push_back(std::move(histogram));
        if(fChain->GetBranch(variable)->GetLeaf(variable)->GetLeafCount()!=nullptr){
            variable_types.push_back(TString(fChain->GetBranch(variable)->GetLeaf(variable)->GetTypeName())+"|Array");
        }
        else {
            variable_types.push_back(TString(fChain->GetBranch(variable)->GetLeaf(variable)->GetTypeName())+"|Value");
        }
   }
   

}

Bool_t HistoProducer::Process(Long64_t entry)
{
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // When processing keyed objects with PROOF, the object is already loaded
   // and is available via the fObject pointer.
   //
   // This function should contain the \"body\" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.

   fReader.SetEntry(entry);
   
   for(size_t i=0;i<variables.size();i++){
       histograms[i]->Fill(1.);
   }

   return kTRUE;
}

void HistoProducer::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.

}

void HistoProducer::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

}

void HistoProducer::AddVariable(TString variable)
{
    variables.push_back(variable);
    
}
void HistoProducer::PrintVariables() const
{
   std::cout << "Registered Variables: " << std::endl;
   for(const auto& variable : variables){
       std::cout << variable << std::endl;
   }
}
void HistoProducer::AddWeight(TString weight)
{
    weights.push_back(weight);

}
void HistoProducer::PrintWeights() const
{
    std::cout << "Registered Weights: " << std::endl;
    for(const auto& weight : weights){
        std::cout << weight << std::endl;
    }
}
void HistoProducer::AddUncertainty(TString uncertainty)
{
    uncertainties.push_back(uncertainty);
}
void HistoProducer::PrintUncertainties() const
{
    std::cout << "Registered Uncertainties: " << std::endl;
    for(const auto& uncertainty : uncertainties){
        std::cout << uncertainty << std::endl;
    }
}
