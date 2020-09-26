import sys
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

label = sys.argv[1]
infile = sys.argv[2]

file=ROOT.TFile.Open(infile,"READ")

effs = ["loose_btagging_efficiency_outside_hadronic","medium_btagging_efficiency_leptonic"]

year = None
if "2018" in infile:
    year = "2018"
elif "2017" in infile:
    year = "2017"
elif "2016" in infile:
    year = "2016"

for eff in effs:
    c=ROOT.TCanvas()
    c.SetLeftMargin(0.1)
    c.SetRightMargin(0.15)
    c.SetBottomMargin(0.1)
    eff_hist = file.Get(eff).Project3D("xz")
    if "hadronic" in eff:
        eff_hist.SetTitle("hadronic analysis channel, "+year)
    elif "leptonic" in eff:
        eff_hist.SetTitle("leptonic analysis channel, "+year)
    else:
        eff_hist.SetTitle("")
    eff_hist.GetYaxis().SetTitle("p_{T}[GeV]")
    eff_hist.GetYaxis().SetTitleOffset(0.95)
    eff_hist.GetYaxis().SetTitleSize(0.05)
    eff_hist.GetYaxis().SetLabelSize(0.04)
    eff_hist.GetXaxis().SetTitleSize(0.05)
    eff_hist.GetXaxis().SetTitleOffset(0.9)
    eff_hist.GetXaxis().SetLabelSize(0.04)
    eff_hist.GetZaxis().SetTitle("b-tagging efficiency")
    eff_hist.GetZaxis().SetTitleSize(0.05)
    eff_hist.GetZaxis().SetTitleOffset(0.9)
    eff_hist.GetZaxis().SetLabelSize(0.04)
    eff_hist.Draw("colz")
    c.Print(eff+"_"+label+".pdf")
