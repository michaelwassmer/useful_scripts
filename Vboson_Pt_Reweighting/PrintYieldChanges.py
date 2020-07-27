import ROOT
import sys

xs_file = ROOT.TFile.Open(sys.argv[1])
correction_file = ROOT.TFile.Open(sys.argv[2])
boson = sys.argv[3]
xs = xs_file.Get(boson+"_boson_pt")
boson_ = sys.argv[4]
correction = correction_file.Get(boson_+"_NNLO_NLO_nnn_nnn_n")
vpt_threshold = float(sys.argv[5])

bin_threshold = xs.FindBin(vpt_threshold)

total_xs_before = xs.GetBinContent(0)+xs.Integral()

total_xs_after = 0
for i in range(0,bin_threshold):
    total_xs_after += xs.GetBinContent(i)
for i in range(bin_threshold,xs.GetNbinsX()+1):
    total_xs_after += (xs.GetBinContent(i)*correction.GetBinContent(i))

print "xs before:",total_xs_before
print "xs after:",total_xs_after
print "xs after / xs before:", total_xs_after*1./total_xs_before
