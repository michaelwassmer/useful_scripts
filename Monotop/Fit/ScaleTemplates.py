# imports
from __future__ import print_function
import ROOT

# option parser
from optparse import OptionParser

usage = "Usage: %prog [options] input_file.root\n"
parser = OptionParser(usage=usage)
parser.add_option("--template_id", action="store", dest="template_id", help="this script only looks at templates that have this substring in them", default="pseudodata_obs")
parser.add_option("--scalefactor", action="store", dest="scalefactor", help="factor used to scale the histograms")

(options, args) = parser.parse_args()

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

template_wildcard = options.template_id
scalefactor = float(options.scalefactor)

# open root file read-only
input_file = ROOT.TFile.Open(input, "UPDATE")

#output_file = ROOT.TFile.Open(input.replace(".root","")+"_scaled.root", "RECREATE")

keys = input_file.GetListOfKeys()
n_keys = str(len(keys))

for j,key in enumerate(keys):
    if j % 100 == 0:
        print (str(j) + "/" + n_keys)
    if not template_wildcard in key.GetName():
        continue
    if "scaled" in key.GetName():
        continue
    hist = input_file.Get(key.GetName()).Clone()
    hist.SetName(hist.GetName()+"_scaled_"+options.scalefactor.replace(".","p"))
    hist.Scale(scalefactor)
    input_file.WriteTObject(hist)


input_file.Close()
#output_file.Close()
