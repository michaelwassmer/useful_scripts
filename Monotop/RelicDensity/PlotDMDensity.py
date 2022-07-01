import sys
import ROOT
from array import array

ROOT.gROOT.SetBatch(True)

file = sys.argv[1]

med_mass = []
dm_mass = []
relic_density = []

with open(file) as infile:
    for line in infile.readlines():
        line_as_list=line.split("\t")
        med_mass.append(float(line_as_list[1]))
        dm_mass.append(float(line_as_list[2]))
        relic_density.append(float(line_as_list[3]))


graph=ROOT.TGraph2D(len(med_mass),array("f",med_mass),array("f",dm_mass),array("f",relic_density))
graph.SetTitle("Relic density as a function of model parameters;Mediator mass (GeV);DM mass (GeV);Relic density")

graph_contour=graph.Clone()
contours = array('d',[0.1186,0.1186+0.002,0.1186-0.002])
graph_contour.GetHistogram().SetContour(3,contours)
graph_contour.SetLineWidth(2)
graph_contour.SetLineColor(ROOT.kBlack)


c=ROOT.TCanvas()

leg=ROOT.TLegend(0.15,0.75,0.45,0.83)
leg.SetMargin(0.15)
leg.AddEntry(graph_contour,"#Omega_{nbm}h^{2}=0.1186#pm 0.0020","l")

graph.Draw("colz")
ROOT.gPad.SetLogz(1)
ROOT.gPad.SetRightMargin(0.13)

graph_contour.Draw("cont3 same")
leg.Draw("same")

c.Print("relic_density.pdf")
