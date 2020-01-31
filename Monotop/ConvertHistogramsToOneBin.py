# imports
from __future__ import print_function
import ROOT
import sys

# option parser 
input = sys.argv[1]

input_file = ROOT.TFile.Open(input,"READ")
    
output_file = ROOT.TFile(input_file.GetName().replace(".root","")+"_bins.root","RECREATE")

n_keys = len(input_file.GetListOfKeys())
for j,key in enumerate(input_file.GetListOfKeys()):
    #print(key.GetName())
    if j%100==0:
        print(str(j)+"/"+str(n_keys))
    object = input_file.Get(key.GetName())
    #print(object)
    if not isinstance(object,ROOT.TH1):
        print("no TH1")
        print("continuing ...")
        continue
    histo_name = object.GetName()
    if "Hadr_Recoil_Pt" not in histo_name:
        print("no Hadr_Recoil_Pt histogram")
        print("continuing ...")
        continue
    histo_title = object.GetTitle()
    histo_nbins = object.GetNbinsX()
    #print("nbins: ",histo_nbins)
    for i in range(histo_nbins+1):
        bin_content = object.GetBinContent(i)
        bin_error = object.GetBinError(i)
        bin_ratio = None
        try:
            bin_ratio = bin_error/bin_content
        except ZeroDivisionError:
            bin_ratio = None
        if i > 0 and i <= histo_nbins:
            print_bin_info = False
            if bin_content < 1e-1 or bin_error < 1e-1:
                print("bin content or error are very small, please check!")
                print_bin_info = True
            if bin_ratio!=None and bin_ratio > 1.:
                print("ratio of bin error and content is very large, please check!")
                print_bin_info = True
            if print_bin_info:
                print("histo: ",object.GetName())
                print("bin number: ",i)
                print("bin content: ",round(bin_content,4))
                print("bin error: ",round(bin_error,4))
                print("bin ratio: ",round(bin_ratio,4) if bin_ratio!=None else bin_ratio)
        histo_one_bin = ROOT.TH1F(histo_name+"_"+"bin"+"_"+str(i),histo_title+"_"+"bin"+"_"+str(i),1,object.GetBinLowEdge(i),object.GetBinLowEdge(i)+object.GetBinWidth(i))
        histo_one_bin.SetBinContent(1,bin_content)
        histo_one_bin.SetBinError(1,bin_error)
        histo_one_bin.SetDirectory(0)
        output_file.WriteTObject(histo_one_bin)

input_file.Close()
output_file.Close()
