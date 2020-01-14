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
    default="",
    help="ROOT selection string using branches in the used ROOT tree",
)
parser.add_option(
    "-R",
    "--ref_trigger",
    dest="ref_trigger",
    type="string",
    default="",
    help="ROOT selection string for reference trigger",
)
parser.add_option(
    "-T",
    "--trigger",
    dest="trigger",
    type="string",
    default="",
    help="ROOT selection string for desired trigger",
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
    "N_AK15Jets",
    "N_LooseMuons",
    "N_TightMuons",
    "Muon_Pt",
    "N_LooseElectrons",
    "N_TightElectrons",
    "Electron_Pt",
    "N_LoosePhotons",
    "Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_vX",
    "Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_vX",
    "Triggered_HLT_IsoMu27_vX",
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

binning = [200, 250, 300, 350, 400, 500, 700, 1500]
# Hadr_Recoil_Pt>200. && N_AK15Jets==1 && N_TightMuons<=2 && N_TightMuons>=1 && Muon_Pt[0]>29. && N_LooseElectrons==0 && N_LoosePhotons==0
# Triggered_HLT_IsoMu27_vX==1
# Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_vX == 1 || Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_vX == 1
reference_events = data_frame.Filter(options.selection + " && " + options.ref_trigger)
selected_events = reference_events.Filter(options.trigger)
reference_histo = reference_events.Histo1D(
    (options.variable+"_ref", options.variable, len(binning) - 1, array.array("d", binning)),
    options.variable,
)
selection_histo = selected_events.Histo1D(
    (options.variable+"_sel", options.variable, len(binning) - 1, array.array("d", binning)),
    options.variable,
)
efficiency = ROOT.TGraphAsymmErrors()
efficiency.Divide(selection_histo.GetPtr(), reference_histo.GetPtr())
efficiency.SetName("efficiency_" + data_mc_string + "_" + options.name)
efficiency.SetTitle("efficiency_" + data_mc_string + "_" + options.name)
# efficiency.Draw("ap")

output_file = ROOT.TFile("efficiency_" + data_mc_string + "_" + options.name + ".root", "RECREATE")
output_file.WriteTObject(efficiency)
