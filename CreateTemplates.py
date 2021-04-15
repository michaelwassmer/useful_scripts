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
     default="(true)",
     help="ROOT selection string using branches in the used ROOT tree",
)
parser.add_option(
    "-1",
    "--variables_1D",
    dest="variables_1D",
    type="string",
    default="N_Jets",
    help="ROOT string for desired variables as comma separated list, e.g. var1,var2,var3,..."
)
parser.add_option(
    "-2",
    "--variables_2D",
    dest="variables_2D",
    type="string",
    default="",
    help="ROOT string for desired variables as comma separated list, e.g. varx1:vary1,varx2:vary2,..."
)
(options, args) = parser.parse_args()
print(options.variables_1D)
print(options.variables_2D)

import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)
from ROOT import RDataFrame as RDF

# ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.ROOT.EnableImplicitMT(options.nthreads)

data_frame = None
branches = [
"pt_pfmet_raw"
"pt_pfmet_raw_jes_up"
"pt_pfmet_raw_jes_down"
"pt_pfmet_raw_jer_up"
"pt_pfmet_raw_jer_down"
"pt_pfmet_raw_jersmear_up"
"pt_pfmet_raw_jersmear_down"
"pt_pfmet_t1"
"pt_pfmet_t1_jes_up"
"pt_pfmet_t1_jes_down"
"pt_pfmet_t1_jer_up"
"pt_pfmet_t1_jer_down"
"pt_pfmet_t1_jersmear_up"
"pt_pfmet_t1_jersmear_down"
"pt_pfmet_t1smear"
"pt_pfmet_t1smear_jes_up"
"pt_pfmet_t1smear_jes_down"
"pt_pfmet_t1smear_jer_up"
"pt_pfmet_t1smear_jer_down"
"pt_pfmet_t1smear_jersmear_up"
"pt_pfmet_t1smear_jersmear_down"
"pt_genmet"
]

branch_vec = ROOT.vector("string")()
[branch_vec.push_back(branch) for branch in branches]

if not options.is_dataframe:
    print ("No dataframe was given. Handling the arguments as trees and adding them to chain.")
    input_files = args
    input_chain = ROOT.TChain("METAnalyzer/MET_tree")
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
    print ("saving dataframe to disk as ", data_mc_string + "_" + names + "_dataframe.root")
    data_frame.Snapshot("tree", data_mc_string + "_" + names + "_dataframe.root", branch_vec)
    print ("saved dataframe to disk ...")

name = options.name

selection = options.selection

vars_1D = options.variables_1D.split(",")
vars_2D = options.variables_2D.split(",")

binning_x = [(0+10*i) for i in range(21)]

histos_1D={}
histos_2D={}

reference_events = data_frame.Filter(selection)
for var_1D in vars_1D:
    var,nbinsx,x_low,x_high = None,None,None,None
    Histo1D_argument = None
    if ";" in var_1D:
        var,nbinsx,x_low,x_high = var_1D.split(";")
        Histo1D_argument = ("{}".format(var), "title;{};arbitrary units".format(var), int(nbinsx), float(x_low), float(x_high))
    else:
        var = var_1D
        Histo1D_argument = ("{}".format(var), "title;{};arbitrary units".format(var), 50, 1, 1)
    print(var_1D)
    print(Histo1D_argument)
    histos_1D[var]=reference_events.Histo1D(
                                          Histo1D_argument,
                                          #("{}".format(var), "title;{};arbitrary units".format(var), int(nbinsx), float(x_low), float(x_high)),
                                          #("{}".format(var_1D), "title;{};arbitrary units".format(var_1D), len(binning_x)-1, array('d',binning_x)),
                                          var
                                          )

print(histos_1D)

for var_2D in vars_2D:
    vars = var_2D.split(":")
    histos_2D[var_2D]=reference_events.Histo2D(
                                          ("{}".format(var_2D), "title;{};{};arbitrary units".format(vars[0],vars[1]), len(binning_x)-1, array('d',binning_x), len(binning_x)-1, array('d',binning_x)),
                                          vars[0],vars[1]
                                          )

print(histos_2D)

output_file = ROOT.TFile(name + ".root", "RECREATE")
for histo_1D in histos_1D:
    output_file.WriteTObject(histos_1D[histo_1D].GetPtr())
for histo_2D in histos_2D:
    output_file.WriteTObject(histos_2D[histo_2D].GetPtr())
output_file.Close()
