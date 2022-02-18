from __future__ import print_function
from optparse import OptionParser
from array import array

usage = "usage: %prog [options] file1.root file2.root"
parser = OptionParser()
parser.add_option(
    "-n", "--name", dest="name", type="string", default="", help="name to recognize output"
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
    default="((Hadr_Recoil_Pt>250.) || (Evt_Pt_MET>100.)) && (N_Jets>=1) && (N_Taus==0)",
    help="ROOT selection string using branches in the used ROOT tree",
)
parser.add_option(
    "-X",
    "--variable_x",
    dest="variable_x",
    type="string",
    default="N_Jets",
    help="ROOT string for desired variable in which the efficiency should be calculated"
)
(options, args) = parser.parse_args()
print(options.variable_x)

import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)
from ROOT import RDataFrame as RDF

# ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.ROOT.EnableImplicitMT(options.nthreads)

data_frame = None
branches = [
    "Hadr_Recoil_Pt",
    "N_AK15Jets",
    "N_Jets",
    "N_Taus",
    "N_HEM_Jets",
    "N_HEM_AK15Jets",
    "N_HEM_METS",
    "HT_AK4Jets",
    "DeltaPhi_AK15Jet_Hadr_Recoil",
    "AK15Jet_Pt",
    "Jet_Pt",
    "Evt_Pt_MET",
    "Weight_XS",
    "Weight_GEN_nom",
    "BosonWeight_nominal",
    "Weight_pu69p2",
    "Weight_CSV",
    "Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_vX",
    "Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_vX",
    "Triggered_HLT_Ele32_WPTight_Gsf_vX",
    "Triggered_HLT_Ele35_WPTight_Gsf_vX",
    "Triggered_HLT_Ele27_WPTight_Gsf_vX",
    "Triggered_HLT_Photon200_vX",
    "Triggered_HLT_Photon175_vX",
    "Triggered_HLT_IsoMu27_vX",
    "Triggered_HLT_IsoMu24_vX",
    "Triggered_HLT_IsoTkMu24_vX",
    "N_LooseElectrons",
    "N_LooseMuons",
    "N_LoosePhotons",
    "N_TightElectrons",
    "N_TightMuons",
    "N_BTagsM",
    "CaloMET_PFMET_ratio",
    "DeltaPhi_AK4Jet_MET",
    "M_W_transverse",
    "AK15Jet_PuppiSoftDropMass",
    "AK15Jet_DeepAK15_TvsQCD",
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

binning_x = [250+(10*i) for i in range(101)]

reference_events = data_frame.Filter(options.selection).Define("M_W_transverse_0","M_W_transverse[0]").Define("AK15Jet_Pt_0","AK15Jet_Pt[0]")
histo = None
histo = reference_events.Define("WEIGHT1", "Weight_XS*Weight_GEN_nom").Histo1D(
    (options.variable_x, options.variable_x, len(binning_x)-1, array('d',binning_x)),
    options.variable_x,
    "WEIGHT1"
    )

output_file = ROOT.TFile("Binning" + "_" + options.name + ".root", "RECREATE")
output_file.WriteTObject(histo.GetPtr())
output_file.Close()
