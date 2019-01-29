import ROOT
import sys
from optparse import OptionParser
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

parser = OptionParser(usage="usage: %prog [options] SLfile DLfile FHfile")
parser.add_option("--SL", dest="SL",help="give SL file",type="string",default="test")
parser.add_option("--DL", dest="DL",help="give DL file",type="string",default="test")
parser.add_option("--FH", dest="FH",help="give FH file",type="string",default="test")
parser.add_option("--tthf", dest="tthf",help="give tthf type (ttbb,tt2b,ttb)",type="string",default="test")


(options, args) = parser.parse_args()

f_SL=ROOT.TFile.Open(options.SL)
f_DL=ROOT.TFile.Open(options.DL)
f_FH=ROOT.TFile.Open(options.FH)

graph_SL = f_SL.Get("eff_"+options.tthf)
graph_DL = f_DL.Get("eff_"+options.tthf)
graph_FH = f_FH.Get("eff_"+options.tthf)

c=ROOT.TCanvas()

graph_ratio_FH_SL = ROOT.TH1D("FH_SL","",graph_SL.GetTotalHistogram().GetNbinsX(),graph_SL.GetTotalHistogram().GetXaxis().GetXmin(),graph_SL.GetTotalHistogram().GetXaxis().GetXmax())
graph_ratio_DL_SL = ROOT.TH1D("DL_SL","",graph_SL.GetTotalHistogram().GetNbinsX(),graph_SL.GetTotalHistogram().GetXaxis().GetXmin(),graph_SL.GetTotalHistogram().GetXaxis().GetXmax())
graph_ratio_SL_SL = ROOT.TH1D("SL_SL","",graph_SL.GetTotalHistogram().GetNbinsX(),graph_SL.GetTotalHistogram().GetXaxis().GetXmin(),graph_SL.GetTotalHistogram().GetXaxis().GetXmax())


for i in range(1,graph_SL.GetTotalHistogram().GetNbinsX()+1):
    graph_ratio_FH_SL.SetBinContent(i,graph_FH.GetEfficiency(i))
    graph_ratio_FH_SL.SetBinError(i,(abs(graph_FH.GetEfficiencyErrorUp(i))+abs(graph_FH.GetEfficiencyErrorLow(i)))/2.)
    graph_ratio_DL_SL.SetBinContent(i,graph_DL.GetEfficiency(i))
    graph_ratio_DL_SL.SetBinError(i,(abs(graph_DL.GetEfficiencyErrorUp(i))+abs(graph_DL.GetEfficiencyErrorLow(i)))/2.)
    graph_ratio_SL_SL.SetBinContent(i,graph_SL.GetEfficiency(i))
    graph_ratio_SL_SL.SetBinError(i,(abs(graph_SL.GetEfficiencyErrorUp(i))+abs(graph_SL.GetEfficiencyErrorLow(i)))/2.)



graph_ratio_FH_SL.Divide(graph_ratio_SL_SL)
graph_ratio_DL_SL.Divide(graph_ratio_SL_SL)
graph_ratio_SL_SL.Divide(graph_ratio_SL_SL)
graph_ratio_FH_SL.SetMinimum(0.7)
graph_ratio_FH_SL.SetMaximum(1.3)

graph_ratio_FH_SL.GetXaxis().SetTitle("p_{T} of softest gen bjet")
graph_ratio_FH_SL.GetYaxis().SetTitle("ratio to SL sample")

graph_ratio_FH_SL.SetLineColor(ROOT.kOrange)
graph_ratio_DL_SL.SetLineColor(ROOT.kBlue)
graph_ratio_SL_SL.SetLineColor(ROOT.kRed)

graph_ratio_FH_SL.SetMarkerColor(ROOT.kOrange)
graph_ratio_DL_SL.SetMarkerColor(ROOT.kBlue)
graph_ratio_SL_SL.SetMarkerColor(ROOT.kRed)

graph_ratio_FH_SL.SetMarkerStyle(20)
graph_ratio_DL_SL.SetMarkerStyle(20)
graph_ratio_SL_SL.SetMarkerStyle(20)

legend=ROOT.TLegend(0.15,0.15,0.35,0.35," ","NDC")
legend.AddEntry(graph_ratio_SL_SL,"SL","p")
legend.AddEntry(graph_ratio_DL_SL,"DL","p")
legend.AddEntry(graph_ratio_FH_SL,"FH","p")
legend.SetTextSize(0.05)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
#legend.SetEntrySeparation(5.0)
tthf = ROOT.TLatex()


graph_ratio_FH_SL.Draw("pe")
graph_ratio_DL_SL.Draw("pesame")
graph_ratio_SL_SL.Draw("phistesame")
legend.Draw("same")
tthf.DrawLatexNDC(0.75,0.8,options.tthf)

c.Print("ratio_diff_tthf_effs_"+options.tthf+".pdf")
