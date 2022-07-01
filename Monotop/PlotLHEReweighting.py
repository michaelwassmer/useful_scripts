import sys
import ROOT

def PreparePad(pad):
    pad.SetLeftMargin(0.15)
    pad.SetRightMargin(0.01)
    pad.SetBottomMargin(0.1)
    pad.SetTopMargin(0.1)

ROOT.gROOT.SetBatch(True)

# save some colors to choose from later
color_list = [ROOT.kRed, ROOT.kBlue, ROOT.kOrange+1, ROOT.kMagenta, ROOT.kCyan, ROOT.kGray+1, ROOT.kYellow+2, ROOT.kViolet]

# read input args
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
#groups = [[nplots*j+i for i in range(nplots)] for j in range(int(nweights)/nplots)]
groups = [ [0,1,2,3,4,5,6], [7,8,9,10,11,12,13,14], [15,16,17,18,19], [20,21,22,23,24], [25,26,27,28,29], [30,31,32,33,34], [35,36,37,38,39] ]
print(groups)

# nominal histogram
histnom = file.Get(var).Clone()
histnom.SetLineStyle(2)
histnom.SetLineColor(ROOT.kBlack)
histnom.GetXaxis().SetLabelSize(1.3*histnom.GetXaxis().GetLabelSize())
histnom.GetXaxis().SetTitleSize(1.3*histnom.GetXaxis().GetTitleSize())
histnom.GetYaxis().SetLabelSize(1.2*histnom.GetYaxis().GetLabelSize())
histnom.GetYaxis().SetTitle("yield (arbitrary units)")
histnom.GetYaxis().SetTitleSize(1.2*histnom.GetYaxis().GetTitleSize())
histnom.SetTitle("")

histnomnorm = histnom.Clone()
histnomnorm.Scale(1./histnomnorm.Integral())
rationom = histnomnorm.Clone()
rationom.SetTitle("")
rationom.GetYaxis().SetTitle("shape ratio to nominal")
rationom.GetYaxis().SetLabelSize(1.7*rationom.GetYaxis().GetLabelSize())
rationom.GetYaxis().SetTitleSize(1.6*rationom.GetYaxis().GetTitleSize())
rationom.GetXaxis().SetLabelSize(1.7*rationom.GetXaxis().GetLabelSize())
rationom.GetXaxis().SetTitleSize(1.7*rationom.GetXaxis().GetTitleSize())
rationom.Divide(histnomnorm)

# read histos into group structure
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
label_cms = ROOT.TText()
label_cms.SetTextFont(63)
label_cms.SetTextSizePixels(30)
label_wip = ROOT.TText()
label_wip.SetTextFont(63)
label_wip.SetTextSizePixels(22)

c=None
for i,histgroup in enumerate(histgroups):
    if i%2==0:
        c=ROOT.TCanvas("lheweights"+str(i), "lheweights"+str(i), 1900, 1200)
        c.Divide(2,1)
    pad = c.cd((i%2)+1)
    PreparePad(pad)
    pad.Divide(1,2)
    subpad_o = pad.cd(1)
    subpad_o.SetPad(subpad_o.GetX1(),0.35,subpad_o.GetX2(),subpad_o.GetY2())
    subpad_o.SetBottomMargin(0.0)
    subpad_o.SetLogy(1)
    histnom.Draw("histe")
    subpad_u = pad.cd(2)
    subpad_u.SetPad(subpad_u.GetX1(),subpad_u.GetY1(),subpad_u.GetX2(),0.35)
    subpad_u.SetTopMargin(0.0)
    subpad_u.SetBottomMargin(0.17)
    rationom.Draw("histe")
    leg = ROOT.TLegend(0.39,0.75,1.0,1.0)
    leg.SetMargin(0.15)
    maximum = histnom.GetBinContent(histnom.GetMaximumBin())
    minimum = histnom.GetBinContent(histnom.GetMinimumBin())
    for j,hist in enumerate(histgroup):
        #hist.Scale(1./hist.Integral())
        hist.SetLineColor(color_list[j])
        pad.cd(1)
        hist.Draw("histesame")
        leg.AddEntry(hist, coupling_list[groups[i][j]], "l")
        maximum = max(maximum,hist.GetBinContent(hist.GetMaximumBin()))
        minimum = min(minimum,hist.GetBinContent(hist.GetMinimumBin()))
        ratio = hist.Clone()
        ratio.Scale(1./ratio.Integral())
        ratio.Divide(histnomnorm)
        pad.cd(2)
        ratio.DrawClone("histesame")
        
    histnom.GetYaxis().SetRangeUser(0.01,10000)
    rationom.GetYaxis().SetRangeUser(0.0,5.0)
    #SetMaximum(maximum)
    #histnom.SetMinimum(minimum)
    leg.AddEntry(histnom, "gdmv_1p0_gdma_0_gv_0p25_ga_0 (nominal)", "l")
    leg.SetTextSize(0.03)
    pad.cd(1)
    leg.DrawClone("same")
    label_cms.DrawTextNDC(0.1, 0.96, "CMS simulation")
    label_wip.DrawTextNDC(0.1, 0.92, "work in progress")
    if i%2==1:
        c.Print("nanoweights"+"_"+var+"_"+str(i)+".pdf")
        c.Print("nanoweights"+"_"+var+"_"+str(i)+".png")

#first_hist.SetMaximum(10000)
#first_hist.SetMinimum(0.1)

#c.SetLogy(1)
#c.SetRangeUser(1,10000)

