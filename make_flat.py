import ROOT
import os
import sys

file_in = ROOT.TFile.Open(sys.argv[1])
file_out = ROOT.TFile(file_in.GetName().replace(".root","_flat.root"),"NEW")

for key in file_in.GetListOfKeys():
    dir = file_in.Get(key.GetName())
    for histo_key in dir.GetListOfKeys():
        print "looking at key: ", histo_key.GetName()
        histogram = dir.Get(histo_key.GetName())
        if isinstance(histogram,ROOT.TH1):
            histogram_clone = histogram.Clone()
            histogram_clone.SetName(key.GetName()+histo_key.GetName().replace("__","_"))
            histogram_clone = histogram.Write(key.GetName()+"_"+histo_key.GetName().replace("__","_"))
            
file_out.Close()
