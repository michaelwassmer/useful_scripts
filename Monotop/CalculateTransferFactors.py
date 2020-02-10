# imports
from __future__ import print_function
import ROOT

# option parser
from optparse import OptionParser

usage = "Usage: %prog [options] input_file.root\n"
usage += "This script takes a root file containing histograms and calculates transfer factors between signal regions/processes and background regions/processes"
usage += "A one-to-one correspondence is assumed for the lists given in the options."
parser = OptionParser(usage=usage)

parser.add_option("--signal_processes", action="append", dest="signal_processes", help="identifiers for the signal processes", default=[])

parser.add_option(
    "--background_processes", action="append", dest="background_processes", help="identifiers for the background processes", default=[]
)

parser.add_option("--signal_regions", action="append", dest="signal_regions", help="identifiers for the signal regions", default=[])

parser.add_option(
    "--background_regions", action="append", dest="background_regions", help="identifiers for the background regions", default=[]
)

parser.add_option("--variable", action="store", dest="variable", help="variable name of the histograms", default="Hadr_Recoil_Pt")

(options, args) = parser.parse_args()

print ("Signal processes: ", options.signal_processes)
print ("Signal regions: ", options.signal_regions)
print ("Background processes: ", options.background_processes)
print ("Background regions: ", options.background_regions)

# catch some errors
if len(args) != 1:
    print ("exactly one input root file has to be given as an argument!")
    print ("exiting ...")
    exit()
input = args[0]
if ".root" not in input:
    print ("given input file probably is not a root file!")
    print ("exiting ...")
    exit()
if not (
    len(options.signal_processes) == len(options.background_processes) == len(options.signal_regions) == len(options.background_regions)
):
    print ("lists are not correct")
    print ("exiting ...")
    exit()

# open root file read-only
input_file = ROOT.TFile.Open(input, "READ")

# create a new output root file
output_file = ROOT.TFile(input_file.GetName().replace(".root", "") + "_TFs.root", "RECREATE")

list_of_keys = input_file.GetListOfKeys()
n_keys = len(list_of_keys)

variable = options.variable

for i in range(len(options.signal_processes)):
    signal_process = options.signal_processes[i]
    signal_region = options.signal_regions[i]
    background_process = options.background_processes[i]
    background_region = options.background_regions[i]
    histo_signal_name = signal_process + "_" + variable + "_" + signal_region
    histo_background_name = background_process + "_" + variable + "_" + background_region
    if not (list_of_keys.Contains(histo_signal_name) and list_of_keys.Contains(histo_background_name)):
        print ("nominal histograms were not found")
        exit()
    histo_signal_nominal = input_file.Get(histo_signal_name)
    histo_background_nominal = input_file.Get(histo_background_name)
    print (histo_signal_nominal)
    print (histo_background_nominal)
    print ("histo signal name: ", histo_signal_name)
    print ("histo background name: ", histo_background_name)
    transfer_factors_nominal_name = (
        "TF" + "_" + background_process + "_" + background_region + "_" + signal_process + "_" + signal_region + "_" + variable
    )
    transfer_factors_nominal = histo_background_nominal.Clone()
    transfer_factors_nominal.SetName(transfer_factors_nominal_name)
    transfer_factors_nominal.SetTitle(transfer_factors_nominal_name)
    transfer_factors_nominal.Divide(histo_signal_nominal)
    transfer_factors_nominal.SetDirectory(0)
    output_file.WriteTObject(transfer_factors_nominal)
    for j, key in enumerate(list_of_keys):
        if j % 100 == 0:
            print (str(j) + "/" + str(n_keys))
        if not isinstance(input_file.Get(key.GetName()), ROOT.TH1):
            print ("no TH1")
            print ("continuing ...")
            continue
        histo_background = None
        histo_signal = None
        systematic = None
        if histo_background_name in key.GetName():
            histo_background = input_file.Get(key.GetName())
            if list_of_keys.Contains(key.GetName().replace(histo_background_name, histo_signal_name)):
                histo_signal = input_file.Get(key.GetName().replace(histo_background_name, histo_signal_name))
            else:
                histo_signal = histo_signal_nominal
            systematic = key.GetName().replace(histo_background_name, "")
        elif histo_signal_name in key.GetName():
            histo_signal = input_file.Get(key.GetName())
            if list_of_keys.Contains(key.GetName().replace(histo_signal_name, histo_background_name)):
                histo_background = input_file.Get(key.GetName().replace(histo_signal_name, histo_background_name))
            else:
                histo_background = histo_background_nominal
            systematic = key.GetName().replace(histo_signal_name, "")
        else:
            continue
        transfer_factors_name = transfer_factors_nominal_name + systematic
        transfer_factors = histo_background.Clone()
        transfer_factors.SetName(transfer_factors_name)
        transfer_factors.SetTitle(transfer_factors_name)
        transfer_factors.Divide(histo_signal)
        transfer_factors.SetDirectory(0)
        output_file.WriteTObject(transfer_factors)

input_file.Close()
output_file.Close()
