from __future__ import print_function
import ROOT
from ROOT import RDataFrame as RDF
from optparse import OptionParser
import array

ROOT.ROOT.EnableImplicitMT(4)

parser = OptionParser()

(options, args) = parser.parse_args()

input_files = args
input_chain = ROOT.TChain("MVATree")

for input_file in input_files:
    input_chain.Add(input_file)

print("Finished chain with ",input_chain.GetEntries()," entries")

data_frame = RDF(input_chain)

print("Finished converting the chain to RDataFrame")

binning = [200,250,300,350,400,500,700,1500]

reference_events = data_frame.Filter("Hadr_Recoil_Pt>200. && N_AK15Jets==1 && N_TightMuons<=2 && N_LooseElectrons==0 && N_LoosePhotons==0 && (Triggered_HLT_Ele35_WPTight_Gsf_vX==1 || Triggered_HLT_Photon200_vX==1 || Triggered_HLT_DoublePhoton70_vX==1)")
selected_events = reference_events.Filter("Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_vX == 1 || Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_vX == 1")
reference_histo = reference_events.Histo1D(("Hadr_Recoil_Pt_ref","Hadronic recoil",len(binning)-1,array.array("d",binning)),"Hadr_Recoil_Pt")
selection_histo = selected_events.Histo1D(("Hadr_Recoil_Pt_sel","Hadronic recoil",len(binning)-1,array.array("d",binning)),"Hadr_Recoil_Pt")
efficiency = ROOT.TGraphAsymmErrors()
efficiency.Divide(selection_histo.GetPtr(),reference_histo.GetPtr())
efficiency.SetName("efficiency")
efficiency.SetTitle("efficiency")
#efficiency.Draw("ap")

output_file = ROOT.TFile("efficiency.root","RECREATE")
output_file.WriteTObject(efficiency)
