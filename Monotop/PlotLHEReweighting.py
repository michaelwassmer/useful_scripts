import sys
import ROOT

def PreparePad(pad):
    pad.SetLeftMargin(0.15)
    pad.SetRightMargin(0.1)
    pad.SetBottomMargin(0.1)
    pad.SetTopMargin(0.1)

color_list = [ROOT.kRed, ROOT.kBlue, ROOT.kOrange+1, ROOT.kMagenta, ROOT.kCyan]

ROOT.gROOT.SetBatch(True)

file=sys.argv[1]
var=sys.argv[2]
weight=sys.argv[3]
nweights=sys.argv[4]

coupling_list = None
with open("monotop_couplings.txt") as coupling_file:
    lines = coupling_file.readlines()
    coupling_list = [line.rstrip("\n") for line in lines]

print(coupling_list) 

# read file
file = ROOT.TFile.Open(file,"READ")

# split histos into groups
nplots = 4
groups = [[nplots*j+i for i in range(nplots)] for j in range(int(nweights)/nplots)]
ngroups = len(groups)
print(groups)

# read histos into group structure
histnom = file.Get(var).Clone()
histnom.SetLineStyle(2)
histnom.SetLineColor(ROOT.kBlack)
histnomnorm = histnom.Clone()
histnomnorm.Scale(1./histnomnorm.Integral())
rationom = histnomnorm.Clone()
rationom.SetTitle("")
rationom.GetYaxis().SetTitle("shape ratio to nominal")
rationom.Divide(histnomnorm)


histgroups = []
for group in groups:
    #print(group)
    histgroup = []
    for index in group:
        #print(index)
        histname = "{}_{}_{}".format(var,weight,index)
        #print(histname)
        histgroup.append(file.Get(histname).Clone())
    histgroups.append(histgroup)

# create canvas and divide it according to number of groups

# plot
c=None
for i,histgroup in enumerate(histgroups):
    if i%2==0:
        c=ROOT.TCanvas("lheweights"+str(i), "lheweights"+str(i), 1900, 1200)
        c.Divide(2,1)
    pad = c.cd((i%2)+1)
    PreparePad(pad)
    pad.Divide(1,2)
    subpad_o = pad.cd(1)
    subpad_o.SetLogy(1)
    histnom.Draw("histe")
    pad.cd(2)
    rationom.Draw("histe")
    if i==0:
        histnom.GetXaxis().SetLabelSize(1.0*histnom.GetXaxis().GetLabelSize())
        histnom.SetTitle("")
    leg = ROOT.TLegend(0.5,0.75,1.0,1.0)
    maximum = histnom.GetBinContent(histnom.GetMaximumBin())
    minimum = histnom.GetBinContent(histnom.GetMinimumBin())
    for j,hist in enumerate(histgroup):
        #hist.Scale(1./hist.Integral())
        hist.SetLineColor(color_list[j])
        pad.cd(1)
        hist.Draw("histesame")
        leg.AddEntry(hist, coupling_list[i*nplots+j], "l")
        maximum = max(maximum,hist.GetBinContent(hist.GetMaximumBin()))
        minimum = min(minimum,hist.GetBinContent(hist.GetMinimumBin()))
        ratio = hist.Clone()
        ratio.Scale(1./ratio.Integral())
        ratio.Divide(histnomnorm)
        pad.cd(2)
        ratio.DrawClone("histesame")
        
    histnom.GetYaxis().SetRangeUser(minimum,maximum)
    rationom.GetYaxis().SetRangeUser(0.0,5.0)
    #SetMaximum(maximum)
    #histnom.SetMinimum(minimum)
    leg.AddEntry(histnom, "gdmv_1p0_gdma_0_gv_0p25_ga_0", "l")
    leg.SetTextSize(0.025)
    pad.cd(1)
    leg.DrawClone("same")
    if i%2==1:
        c.Print("nanoweights"+"_"+var+"_"+str(i)+".pdf")
        c.Print("nanoweights"+"_"+var+"_"+str(i)+".png")

#first_hist.SetMaximum(10000)
#first_hist.SetMinimum(0.1)

#c.SetLogy(1)
#c.SetRangeUser(1,10000)

