from __future__ import print_function
from optparse import OptionParser
import numpy as np
import ROOT
ROOT.gROOT.SetBatch(True)

usage = "usage: %prog [options] file1.root file2.root"
parser = OptionParser()
parser.add_option(
    "-l", "--label", dest="label", type="string", default="unlabeled", help="label to recognize output files"
)
parser.add_option(
    "--mc_files",
    dest="mc_files",
    type="string",
    default="",
    help="string containing the comma separated files with the mc efficiencies"
)
parser.add_option(
    "--mc_labels",
    dest="mc_labels",
    type="string",
    default="",
    help="string containing the comma separated files with the mc labels"
)
parser.add_option(
    "--data_files",
    dest="data_files",
    type="string",
    default="",
    help="string containing the comma separated files with the data efficiencies"
)
parser.add_option(
    "--data_labels",
    dest="data_labels",
    type="string",
    default="",
    help="string containing the comma separated files with the data labels"
)
parser.add_option(
    "--variables", dest="variables", type="string", default="pt_pfmetnomu_t1", help="comma separated variables for which plots are supposed to be created"
)
parser.add_option(
    "--variables_labels", dest="variables_labels", type="string", default="PFMETNoMu", help="comma separated variable labels for which plots are supposed to be created"
)
parser.add_option(
    "--probe_triggers", dest="probe_triggers", type="string", default="HLT_blabla", help="trigger expression for which the efficiencies are shown"
)

(options, args) = parser.parse_args()

mc_files =  options.mc_files.split(",")
mc_labels =  options.mc_labels.split(",")
data_files =  options.data_files.split(",")
data_labels =  options.data_labels.split(",")
variables = options.variables.split(",")
variables_labels = options.variables_labels.split(",")
probe_triggers = options.probe_triggers

print("mc files:\n")
print(mc_files)
print("------------------------------------------")
print("data files:\n")
print(data_files)
print("------------------------------------------")
print("variables:\n")
print(variables)

mc_effs = []
data_effs = []

for mc_file,mc_label in zip(mc_files,mc_labels):
    print(mc_file)
    rfile = ROOT.TFile.Open(mc_file,"READ")
    effs = []
    for i, (var,var_label) in enumerate(zip(variables,variables_labels)):
        eff = rfile.Get(var).Clone(mc_label+"__"+var)
        eff.SetTitle("{};{};{}".format(mc_label,var_label,"#epsilon"))
        eff.SetLineWidth(2)
        effs.append(eff)
    mc_effs.append(effs)
    rfile.Close()

print(mc_effs)

for data_file,data_label in zip(data_files,data_labels):
    print(data_file)
    rfile = ROOT.TFile.Open(data_file,"READ")
    effs = []
    for i, (var,var_label) in enumerate(zip(variables,variables_labels)):
        eff = rfile.Get(var).Clone(data_label+"__"+var)
        eff.SetTitle("{};{};{}".format(data_label,var_label,"#epsilon"))
        eff.SetLineWidth(2)
        effs.append(eff)
    data_effs.append(effs)
    rfile.Close()

print(data_effs)

probe_triggers_label = ROOT.TLatex(0.2,1.15,probe_triggers)
probe_triggers_label.SetTextSize(0.025)

# plots for different variable in same region
for mc_eff_set,data_eff_set,mc_label,data_label in zip(mc_effs,data_effs,mc_labels,data_labels):
    c=ROOT.TCanvas()
    l=ROOT.TLegend(0.5,0.2,0.9,0.5)
    line = ROOT.TLine(0,0.95,500,0.95)
    line.SetLineStyle(ROOT.kDashed)
    dummy_eff = mc_eff_set[0].Clone("dummy")
    dummy_eff.SetLineColorAlpha(0,0)
    dummy_eff.SetTitle(";X;#epsilon")
    dummy_eff.Draw()
    ROOT.gPad.Update()
    dummy_eff.GetPaintedGraph().GetXaxis().SetRangeUser(0,500)
    for i,mc_eff in enumerate(mc_eff_set):
        mc_eff.SetLineColor(ROOT.kRed+1*i*(i%2==0)-1*i*(i%2==1))
        mc_eff.SetMarkerStyle(20+1*i)
        mc_eff.SetMarkerColor(ROOT.kRed+1*i*(i%2==0)-1*i*(i%2==1))
        mc_eff.Draw("same")
        ROOT.gPad.Update()
        l.AddEntry(mc_eff,"{}, X={}".format(mc_eff.GetTitle(),mc_eff.GetPaintedGraph().GetXaxis().GetTitle()),"lp")
    for i,data_eff in enumerate(data_eff_set):
        data_eff.SetLineColor(ROOT.kBlue+1*i*(i%2==0)-1*i*(i%2==1))
        data_eff.SetMarkerStyle(20+1*i)
        data_eff.SetMarkerColor(ROOT.kBlue+1*i*(i%2==0)-1*i*(i%2==1))
        data_eff.Draw("same")
        ROOT.gPad.Update()
        l.AddEntry(data_eff,"{}, X={}".format(data_eff.GetTitle(),data_eff.GetPaintedGraph().GetXaxis().GetTitle()),"lp")
    l.Draw("same")
    line.Draw("same")
    probe_triggers_label.Draw("same")
    c.Print(mc_label.replace(" ","")+"__"+data_label.replace(" ","")+".pdf")

# plots with same variable in different regions, therefore transpose lists
mc_effs_t = np.array(mc_effs).T.tolist()
data_effs_t = np.array(data_effs).T.tolist()
mc_labels_t = np.array(mc_labels).T.tolist()
data_labels_t = np.array(data_labels).T.tolist()

for mc_eff_set,data_eff_set,var_label in zip(mc_effs_t,data_effs_t,variables_labels):
    c=ROOT.TCanvas()
    l=ROOT.TLegend(0.5,0.2,0.9,0.5)
    line = ROOT.TLine(0,0.95,500,0.95)
    line.SetLineStyle(ROOT.kDashed)
    dummy_eff = mc_eff_set[0].Clone("dummy")
    dummy_eff.SetLineColorAlpha(0,0)
    dummy_eff.SetTitle(";X;#epsilon")
    dummy_eff.Draw()
    ROOT.gPad.Update()
    dummy_eff.GetPaintedGraph().GetXaxis().SetRangeUser(0,500)
    for i,mc_eff in enumerate(mc_eff_set):
        mc_eff.SetLineColor(ROOT.kRed+1*i*(i%2==0)-1*i*(i%2==1))
        mc_eff.SetMarkerStyle(20+1*i)
        mc_eff.SetMarkerColor(ROOT.kRed+1*i*(i%2==0)-1*i*(i%2==1))
        mc_eff.Draw("same")
        ROOT.gPad.Update()
        l.AddEntry(mc_eff,"{}, X={}".format(mc_eff.GetTitle(),mc_eff.GetPaintedGraph().GetXaxis().GetTitle()),"lp")
    for i,data_eff in enumerate(data_eff_set):
        data_eff.SetLineColor(ROOT.kBlue+1*i*(i%2==0)-1*i*(i%2==1))
        data_eff.SetMarkerStyle(20+1*i)
        data_eff.SetMarkerColor(ROOT.kBlue+1*i*(i%2==0)-1*i*(i%2==1))
        data_eff.Draw("same")
        ROOT.gPad.Update()
        l.AddEntry(data_eff,"{}, X={}".format(data_eff.GetTitle(),data_eff.GetPaintedGraph().GetXaxis().GetTitle()),"lp")
    l.Draw("same")
    line.Draw("same")
    probe_triggers_label.Draw("same")
    c.Print(var_label.replace(" ","").replace("(GeV)","")+".pdf")
