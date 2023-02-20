import sys
import ROOT
from array import array

ROOT.gROOT.SetBatch(True)

file = sys.argv[1]

xtitle="Mediator mass m_{V}(GeV)"
ytitle="DM mass m_{#chi}(GeV)"
if len(sys.argv)>=3:
    xtitle = str(sys.argv[2])
if len(sys.argv)>=4:
    ytitle = str(sys.argv[3])

med_mass = []
dm_mass = []
relic_density = []

with open(file) as infile:
    for line in infile.readlines():
        line_as_list=line.split("\t")
        if float(line_as_list[2])<0.:
            continue
        med_mass.append(float(line_as_list[1]))
        dm_mass.append(float(line_as_list[2]))
        relic_density.append(float(line_as_list[3]))

graph=ROOT.TGraph2D(len(med_mass),array("f",med_mass),array("f",dm_mass),array("f",relic_density))
graph.SetTitle("Relic density as a function of model parameters;{};{};Relic density".format(xtitle,ytitle))

max = graph.GetHistogram().GetMaximum()
min = graph.GetHistogram().GetMinimum()
graph.GetHistogram().GetZaxis().SetRangeUser(min*0.1,max*10)
#graph.GetHistogram().GetZaxis().SetRangeUser(0.001,100)
#graph.GetHistogram().GetYaxis().SetRangeUser(0.,1250)
#graph.GetHistogram().GetXaxis().SetRangeUser(0.,2500)

graph_contour=graph.Clone()
contours = array('d',[0.1186,0.1186+0.002,0.1186-0.002])
graph_contour.GetHistogram().SetContour(3,contours)
graph_contour.SetLineWidth(2)
graph_contour.SetLineColor(ROOT.kBlack)


c=ROOT.TCanvas()

leg=ROOT.TLegend(0.15,0.76,0.45,0.84)
leg.SetMargin(0.15)
leg.AddEntry(graph_contour,"#Omega_{nbm}h^{2}=0.1186#pm 0.0020","l")

graph.Draw("colz")
ROOT.gPad.SetLogz(1)
ROOT.gPad.SetRightMargin(0.13)

graph_contour.Draw("cont3 same")
leg.Draw("same")

c.Print("relic_density_{}.pdf".format(file.replace(".txt","")))
