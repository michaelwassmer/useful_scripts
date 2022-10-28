# imports
from __future__ import print_function
import ROOT
import sys
from array import array

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
parser.add_option(
    "-t",
    "--transferfactor",
    action="store_true",
    dest="transferfactor",
    help="set this option if you run over transfer factors",
    default=False,
)
(options, args) = parser.parse_args()

# catch some errors
if(len(args)!=1):
    print("exactly one input ROOT file has to be given as an argument!")
    print("exiting ...")
    exit()
input = args[0]
if ".root" not in input:
   print("given input file is probably not a ROOT file!")
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
keys = set()

x_binnumber = array("i",[-1])
y_binnumber = array("i",[-1])
z_binnumber = array("i",[-1])

# loop over the keys of the input root file (histograms)
for j, key in enumerate(input_file.GetListOfKeys()):
    # print(key.GetName())
    if j % 100 == 0:
        print (str(j) + "/" + str(n_keys))
    # read object
    object = input_file.Get(key.GetName())
    # check if the opened object is a ROOT histogram
    isTH1 = isinstance(object, ROOT.TH1) and (not isinstance(object, ROOT.TH2))
    isTH2 = isinstance(object, ROOT.TH2)
    if (not isTH1) and (not isTH2):
        #print ("no TH1")
        #print ("continuing ...")
        continue
    histo_name = object.GetName()
    # check if the opened object is one of the correct histograms
    if options.variable not in histo_name:
        #print ("no ", options.variable, " in histogram name")
        #print ("continuing ...")
        continue
    if "vectormonotop" in histo_name and "CR" in histo_name:
        #print ("signal template in control region, not necessary ...")
        #print ("continuing ...")
        continue
    if "signal" in histo_name and not "vectormonotop" in histo_name:
        #print ("signal uncertainty for background process, not necessary ...")
        #print ("continuing ...")
        continue
    if not options.transferfactor:
        if histo_name in keys:
            print ("double histos in file !")
            exit()
        else:
            keys.add(histo_name)
    # get some information from the histogram
    histo_title = object.GetTitle()
    histo_nbins = object.GetNcells()
    # print("nbins: ",histo_nbins)
    # loop over the bins of the histogram
    for i in range(0,histo_nbins):
        x_binnumber[0],y_binnumber[0],z_binnumber[0] = -1,-1,-1
        object.GetBinXYZ(i,x_binnumber,y_binnumber,z_binnumber)
        #print(x_binnumber[0],y_binnumber[0],z_binnumber[0])
        if isTH1 and (x_binnumber[0]==0 or x_binnumber[0]>object.GetNbinsX()):
            print("ignoring underflow/overflow bin ...")
            continue
        if isTH2 and ((x_binnumber[0]==0 or x_binnumber[0]>object.GetNbinsX()) or (y_binnumber[0]==0 or y_binnumber[0]>object.GetNbinsY())):
            print("ignoring underflow/overflow bin ...")
            continue
        n_bins += 1
        # get bin content and error
        bin_content = object.GetBinContent(i)
        bin_error = object.GetBinError(i)
        bin_ratio = None
        try:
            bin_ratio = bin_error / bin_content
        except ZeroDivisionError:
            bin_ratio = None
        # some sanity checks for the bins (optional)
        if not options.warnings:
            print_bin_info = False
            if bin_content <= 0.0:
                print ("bin content zero or negative, please check!")
                print_bin_info = True
            #if bin_ratio != None and bin_ratio > 1.0:
                #print ("ratio of bin error and content is very large, please check!")
                #print_bin_info = True
            if object.GetEntries() < 10 and not options.transferfactor:
                print ("template has less than 10 entries, please check!")
                print_bin_info = True
            if options.transferfactor:
                if bin_content > 100.:
                    print ("transfer factor greater than 100, please check!")
                    print_bin_info = True
                    #exit()
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
                    if not options.transferfactor:
                        print ("setting bin to default!")
                        bin_content = 0.1
                        bin_error = 0.1
                    else:
                        if bin_content <= 0.0:
                            print ("setting transfer factor to 0.01")
                            bin_content = 0.01
                            bin_error = 0.01
                        elif bin_content > 100.:
                            print ("transfer factor greater than 100, is this correct?")
                            #bin_content = 100.
                            #bin_error = 100.
        # create a new histogram with only one bin
        histo_label = None
        if isTH1:
            histo_label = "bin_{}".format(x_binnumber[0])
            histo_label_nice = "bin {}".format(x_binnumber[0])
            bin_label = "{} #leq x < {}".format(object.GetXaxis().GetBinLowEdge(x_binnumber[0]),object.GetXaxis().GetBinLowEdge(x_binnumber[0])+object.GetXaxis().GetBinWidth(x_binnumber[0]))
        elif isTH2:
            histo_label = "binx_{}_biny_{}".format(x_binnumber[0],y_binnumber[0])
            histo_label_nice = "binx {}, biny {}".format(x_binnumber[0],y_binnumber[0])
            bin_label = "#splitline{{{} #leq x < {}}}{{{} #leq y < {}}}".format(object.GetXaxis().GetBinLowEdge(x_binnumber[0]),object.GetXaxis().GetBinLowEdge(x_binnumber[0])+object.GetXaxis().GetBinWidth(x_binnumber[0]),object.GetYaxis().GetBinLowEdge(y_binnumber[0]),object.GetYaxis().GetBinLowEdge(y_binnumber[0])+object.GetYaxis().GetBinWidth(y_binnumber[0]))
        histo_one_bin = ROOT.TH1F(
            histo_name + "__" + histo_label,
            histo_title + " " + histo_label_nice,
            1,
            0,
            1,
        )
        histo_one_bin.GetXaxis().SetBinLabel(1,bin_label)
        # write the bin content and error of the current bin of the histogram to the histogram with only one bin
        histo_one_bin.SetBinContent(1, bin_content)
        histo_one_bin.SetBinError(1, bin_error)
        # remove automatic memory handling of ROOT for the new one-bin histogram
        histo_one_bin.SetDirectory(0)
        # write the histogram to the output file
        if isTH1:
            if x_binnumber[0] not in dirs:
                dirs[x_binnumber[0]]=output_file.mkdir("bin_"+str(x_binnumber[0]))
            dirs[x_binnumber[0]].WriteTObject(histo_one_bin)
        elif isTH2:
            if x_binnumber[0] not in dirs:
                dirs[x_binnumber[0]] = {}
                output_file.mkdir("binx_"+str(x_binnumber[0]))
            if y_binnumber[0] not in dirs[x_binnumber[0]]:
                output_file.Get("binx_"+str(x_binnumber[0])).mkdir("biny_"+str(y_binnumber[0]))
                dirs[x_binnumber[0]][y_binnumber[0]]=output_file.Get("binx_"+str(x_binnumber[0])).Get("biny_"+str(y_binnumber[0]))
            dirs[x_binnumber[0]][y_binnumber[0]].WriteTObject(histo_one_bin)

# close the input and output root files
input_file.Close()
output_file.Close()
# print some information about the number of probematic bins
print ("# bins: ", n_bins)
print ("# problematic bins: ", n_problematic_bins)
