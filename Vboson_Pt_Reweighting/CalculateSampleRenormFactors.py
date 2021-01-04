from __future__ import print_function
from optparse import OptionParser
import array

usage = "usage: %prog [options] file1.root file2.root"
parser = OptionParser()
parser.add_option(
    "-n", "--name", dest="name", type="string", default="", help="name to recognize output"
)
parser.add_option(
    "-d",
    "--data",
    dest="is_data",
    action="store_true",
    default=False,
    help="set this flag if you are processing real data",
)
parser.add_option(
    "-f",
    "--dataframe",
    dest="is_dataframe",
    action="store_true",
    default=False,
    help="set this flag if you want to pass a dataframe directly as an argument",
)
parser.add_option(
    "-s",
    "--save",
    dest="save",
    action="store_true",
    default=False,
    help="set this flag if you want to save the generated dataframe to disk",
)
parser.add_option(
    "-j", "--nthreads", dest="nthreads", type="int", default=4, help="number of threads to use"
)
parser.add_option(
    "-S",
    "--selection",
    dest="selection",
    type="string",
    default="(Hadr_Recoil_Pt>=250.) && (N_AK15Jets>=1) && (N_Taus==0) && (N_AK15Jets_SoftDrop==N_AK15Jets)",
    #default="(Evt_Pt_MET>100.) && (N_LoosePhotons==0) && ((N_LooseElectrons+N_LooseMuons)==1) && ((N_TightElectrons+N_TightMuons)==1) && (N_Jets>0) && (Jet_Pt[0]>50.) && (M_W_transverse[0]>=40.) && (DeltaPhi_AK4Jet_MET[0]>1.5)",
    help="ROOT selection string using branches in the used ROOT tree",
)
parser.add_option(
    "-V",
    "--variable",
    dest="variable",
    type="string",
    default="Hadr_Recoil_Pt",
    help="ROOT string for desired variable in which the efficiency should be calculated"
)
(options, args) = parser.parse_args()

data_mc_string = "data" if options.is_data else "mc"

import ROOT
from ROOT import RDataFrame as RDF

# ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.ROOT.EnableImplicitMT(options.nthreads)

data_frame = None
branches = [
    "Hadr_Recoil_Pt",
    "Evt_Pt_MET",
    "M_W_transverse",
    "N_Jets",
    "N_AK15Jets",
    "N_AK15Jets_SoftDrop",
    "N_LooseMuons",
    "N_TightMuons",
    #"Muon_Pt",
    "N_LooseElectrons",
    "N_TightElectrons",
    #"Electron_Pt",
    "N_LoosePhotons",
    #"Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_vX",
    #"Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_vX",
    #"Triggered_HLT_IsoMu27_vX",
    #"DeltaPhi_AK15Jet_Hadr_Recoil",
    #"AK15Jet_CHF",
    #"AK15Jet_NHF",
    #"N_AK4JetsLooseTagged_outside_AK15Jets",
    "Weight_XS",
    "Weight_GEN_nom",
    "BosonWeight_nominal",
    "Jet_Pt",
    #"Jet_Phi",
    #"Jet_Eta",
    "N_Taus",
    "N_HEM_Jets",
    "DeltaPhi_AK4Jet_Hadr_Recoil",
    "DeltaPhi_AK4Jet_MET",
    "W_Pt",
    "Z_Pt",
    "DeltaR_AK4Jet_LooseElectron",
    "DeltaR_AK4Jet_LooseMuon"
]
branch_vec = ROOT.vector("string")()
[branch_vec.push_back(branch) for branch in branches]

if not options.is_dataframe:
    print ("No dataframe was given. Handling the arguments as trees and adding them to chain.")
    input_files = args
    input_chain = ROOT.TChain("MVATree")
    for input_file in input_files:
        input_chain.Add(input_file)
    print ("Finished loading chain with ", input_chain.GetEntries(), " entries")
    data_frame = RDF(input_chain, branch_vec)
else:
    print ("Dataframe flag was set. Handling argument as dataframe.")
    input_file = args[0]
    data_frame = RDF("tree", input_file)

print ("Finished converting the chain to RDataFrame")

if not options.is_dataframe and options.save:
    print ("saving dataframe to disk as ", data_mc_string + "_" + options.name + "_dataframe.root")
    data_frame.Snapshot("tree", data_mc_string + "_" + options.name + "_dataframe.root", branch_vec)
    print ("saved dataframe to disk ...")

#binning = [200, 250, 300, 350, 400, 500, 700, 1500]
# Hadr_Recoil_Pt>200. && N_AK15Jets==1 && N_TightMuons<=2 && N_TightMuons>=1 && Muon_Pt[0]>29. && N_LooseElectrons==0 && N_LoosePhotons==0
# Triggered_HLT_IsoMu27_vX==1
# Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_vX == 1 || Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_vX == 1
events = data_frame.Filter(options.selection)

events = events.Filter(
    """
    //std::cout << \"I'm at entry \" << tdfentry_ << std::endl;
    bool dphi_crit = true;
    for(int i=0;i<N_Jets;i++){
        dphi_crit = dphi_crit && DeltaPhi_AK4Jet_Hadr_Recoil[i]>0.8;
    }
    return dphi_crit;"""
)

#events = events.Filter(
#    """
#    //std::cout << \"I'm at entry \" << tdfentry_ << std::endl;
#    bool dr_crit = true;
#    for(int j=0;j<N_LooseElectrons;j++){
#        for(int i=0;i<N_Jets;i++){
#            dr_crit = dr_crit && DeltaR_AK4Jet_LooseElectron[i*N_LooseElectrons+j]<3.4;
#        }
#    }
#    for(int j=0;j<N_LooseMuons;j++){
#        for(int i=0;i<N_Jets;i++){
#            dr_crit = dr_crit && DeltaR_AK4Jet_LooseMuon[i*N_LooseMuons+j]<3.4;
#        }
#    }
#    return dr_crit;"""
#)

reference_histo = None
selection_histo = None
if options.is_data:
    reference_histo = events.Histo1D(
        (options.variable+"_ref", options.variable, 1, -9999., 9999.),
        options.variable,
        )
    selection_histo = events.Histo1D(
        (options.variable+"_sel", options.variable, 1, -9999., 9999.),
        options.variable,
        )
else:
    reference_histo = events.Define("WEIGHT1", "Weight_XS*Weight_GEN_nom").Histo1D(
        (options.variable+"_ref", options.variable, 1, -9999., 9999.),
        options.variable,
        "WEIGHT1"
        )
    selection_histo = events.Define("WEIGHT2", "Weight_XS*Weight_GEN_nom*((W_Pt>=30. || Z_Pt>=100. || Gamma_Pt>=100.)*BosonWeight_nominal+(W_Pt<30. && Z_Pt<100. && Gamma_Pt<100.)*1.)").Histo1D(
        (options.variable+"_sel", options.variable, 1, -9999., 9999.),
        options.variable,
        "WEIGHT2"
        )
reference_histo.SetLineColor(ROOT.kBlue)
selection_histo.SetLineColor(ROOT.kRed)
#reference_histo.Draw("hist")
#selection_histo.Draw("histsame")
#raw_input("")
print("ratio reweighted/unreweighted: ",round(selection_histo.Integral()/reference_histo.Integral(),2))
print("renorm factor: ",round(reference_histo.Integral()/selection_histo.Integral(),2))
output_file = ROOT.TFile("Vboson_Reweighting_" + data_mc_string + "_" + options.name + ".root", "RECREATE")
output_file.WriteTObject(reference_histo.GetPtr())
output_file.WriteTObject(selection_histo.GetPtr())
output_file.Close()
