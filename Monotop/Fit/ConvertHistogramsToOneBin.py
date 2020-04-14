# imports
from __future__ import print_function
import ROOT
import sys

# option parser
from optparse import OptionParser

usage = "Usage: %prog [options] input_file.root\n"
usage += "This script takes a root file containing histograms and converts each of the bins into a new histogram with only one bin."
parser = OptionParser(usage=usage)
parser.add_option(
    "-w",
    "--warnings_off",
    action="store_true",
    dest="warnings",
    help="set this option if you do not want to have the bins checked",
    default=False,
)
parser.add_option(
    "-d",
    "--drop",
    action="store_true",
    dest="drop",
    help="set this option if you want the problematic bins to be dropped",
    default=False,
)
parser.add_option(
    "-v",
    "--variable",
    action="store",
    dest="variable",
    help="string which has to occur in the histograms name so that it is considered",
    default="Hadr_Recoil_Pt",
)
parser.add_option(
    "-r",
    "--repair",
    action="store_true",
    dest="repair",
    help="set this options if you want to set the problematic bins to a default of 0.1",
    default=False
)
(options, args) = parser.parse_args()

# catch some errors
if(len(args)!=1):
    print("exactly one input root file has to be given as an argument!")
    print("exiting ...")
    exit()
input = args[0]
if ".root" not in input:
   print("given input file probably is not  a root file!")
   print("exiting ...")
   exit()
if options.drop and options.repair:
   print("you cannot drop and repair the bins at the same time!")
   print("exiting ...")
   exit()
# open root file read-only
input_file = ROOT.TFile.Open(input, "READ")

# create a new output root file
output_file = ROOT.TFile(
    input_file.GetName().replace(".root", "") + "_bins.root", "RECREATE"
)

# some bookkeeping numbers
n_keys = len(input_file.GetListOfKeys())
n_bins = 0
n_problematic_bins = 0
dirs = {}
# loop over the keys of the input root file (histograms)
for j, key in enumerate(input_file.GetListOfKeys()):
    # print(key.GetName())
    if j % 100 == 0:
        print (str(j) + "/" + str(n_keys))
    object = input_file.Get(key.GetName())
    # check if the opened object is a ROOT histogram
    if not isinstance(object, ROOT.TH1):
        print ("no TH1")
        print ("continuing ...")
        continue
    histo_name = object.GetName()
    # check if the opened object is one of the correct histograms
    if options.variable not in histo_name:
        print ("no ", options.variable, " in histogram name")
        print ("continuing ...")
        continue
    # get some information from the histogram
    histo_title = object.GetTitle()
    histo_nbins = object.GetNbinsX()
    # print("nbins: ",histo_nbins)
    # loop over the bins of the histogram
    for i in range(1,histo_nbins + 1):
        n_bins += 1
        if i not in dirs:
            dirs[i]=output_file.mkdir("bin_"+str(i))
        # get bin content and error
        bin_content = object.GetBinContent(i)
        bin_error = object.GetBinError(i)
        bin_ratio = None
        try:
            bin_ratio = bin_error / bin_content
        except ZeroDivisionError:
            bin_ratio = None
        # some sanity checks for the bins (optional)
        if not options.warnings and i > 0 and i <= histo_nbins:
            print_bin_info = False
            if bin_content < 1e-1 or bin_error < 1e-1:
                print ("bin content or error are very small, please check!")
                print_bin_info = True
            #if bin_ratio != None and bin_ratio > 1.0:
                #print ("ratio of bin error and content is very large, please check!")
                #print_bin_info = True
            if object.GetEntries() < 10.:
                print ("template has less than 10 entries, please check!")
                print_bin_info = True
            if print_bin_info:
                n_problematic_bins += 1
                print ("histo: ", object.GetName())
                print ("bin number: ", i)
                print ("bin content: ", round(bin_content, 4))
                print ("bin error: ", round(bin_error, 4))
                print (
                    "bin ratio: ",
                    round(bin_ratio, 4) if bin_ratio != None else bin_ratio,
                )
                print ("template entries: ", object.GetEntries())
                # drop a problematic bin (optional)
                if options.drop:
                    print ("bin dropped!")
                    continue
                elif options.repair:
                    print ("setting bin to default!")
                    bin_content = 0.1
                    bin_error = 0.0
        # create a new histogram with only one bin
        histo_one_bin = ROOT.TH1F(
            histo_name + "_" + "bin" + "_" + str(i),
            histo_title + "_" + "bin" + "_" + str(i),
            1,
            object.GetBinLowEdge(i),
            object.GetBinLowEdge(i) + object.GetBinWidth(i),
        )
        # write the bin content and error of the current bin of the histogram to the histogram with only one bin
        histo_one_bin.SetBinContent(1, bin_content)
        histo_one_bin.SetBinError(1, bin_error)
        # remove automatic memory handling of ROOT for the new one-bin histogram
        histo_one_bin.SetDirectory(0)
        # write the histogram to the output file
        dirs[i].WriteTObject(histo_one_bin)

# close the input and output root files
input_file.Close()
output_file.Close()
# print some information about the number of probematic bins
print ("# bins: ", n_bins)
print ("# problematic bins: ", n_problematic_bins)
