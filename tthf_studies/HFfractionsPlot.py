import ROOT
import sys
import os
from math import sqrt

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--ttlf", dest="ttlf", default="0", type="float", help="number of ttlf events")
parser.add_option("--ttcc", dest="ttcc", default="0", type="float", help="number of ttcc events")
parser.add_option("--ttb", dest="ttb", default="0", type="float", help="number of ttb events")
parser.add_option("--tt2b", dest="tt2b", default="0", type="float", help="number of tt2b events")
parser.add_option("--ttbb", dest="ttbb", default="0", type="float", help="number of ttbb events")
parser.add_option("--name", dest="name", default="test", type="str", help="name of root file")
(options, args) = parser.parse_args()

hist = ROOT.TH1D("entries","entries",5,0,5)

hist.GetXaxis().SetBinLabel(1,"ttlf")
hist.SetBinContent(1,options.ttlf)
hist.SetBinError(1,sqrt(options.ttlf))
hist.GetXaxis().SetBinLabel(2,"ttcc")
hist.SetBinContent(2,options.ttcc)
hist.SetBinError(2,sqrt(options.ttcc))
hist.GetXaxis().SetBinLabel(3,"ttb")
hist.SetBinContent(3,options.ttb)
hist.SetBinError(3,sqrt(options.ttb))
hist.GetXaxis().SetBinLabel(4,"tt2b")
hist.SetBinContent(4,options.tt2b)
hist.SetBinError(4,sqrt(options.tt2b))
hist.GetXaxis().SetBinLabel(5,"ttbb")
hist.SetBinContent(5,options.ttbb)
hist.SetBinError(5,sqrt(options.ttbb))

print hist.GetBinError(5)/hist.GetBinContent(5)

hist.Scale(1./(options.ttlf+options.ttcc+options.ttb+options.tt2b+options.ttbb))

c = ROOT.TCanvas()
c.SetLogy()

print hist.GetBinError(5)/hist.GetBinContent(5)
hist.GetXaxis().SetLabelSize(0.1)
hist.GetYaxis().SetLabelSize(0.05)
hist.SetLineWidth(2)
hist.SetTitle("2017/2016 ratio of fractions")
hist.Draw("histe")

raw_input("bla")

f=ROOT.TFile.Open(options.name+".root","RECREATE")
f.WriteTObject(hist)
f.Close()

