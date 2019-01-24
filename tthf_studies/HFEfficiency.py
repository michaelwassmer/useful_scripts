import ROOT
import sys
from optparse import OptionParser
from array import array

ROOT.gROOT.SetBatch(True)
#ROOT.ROOT.EnableImplicitMT()

parser = OptionParser(usage="usage: %prog [options] file1 file2")
parser.add_option("-c", "--channel", dest="channel",help="give the channel (SL,DL,FH)",type="string",default="test")
parser.add_option("-y", "--year", dest="year",help="give the year (2016,2017)",type="string",default="test")
parser.add_option("-p", "--ptmin", dest="ptmin",help="minimal pt value",type="float",default=10)
parser.add_option("-P", "--ptmax", dest="ptmax",help="maximal pt value",type="float",default=200)
parser.add_option("-n", "--nbins", dest="nbins",help="number of bins",type="int",default=19)


(options, args) = parser.parse_args()
files = [str(filename) for filename in args]
#print files
chain=ROOT.TChain("MVATree")
for file in files:
    chain.Add(file)

tthf_flag = array('i',[-1])
n_add_b_genjets = array('i',[-1])
last_b_genjet_pt = array('f',[-1.]*20)

eff_ttbb = ROOT.TEfficiency("eff_ttbb","tthf efficiencies;p_{T} of softest gen bjet;efficiency",options.nbins,options.ptmin,options.ptmax)
eff_tt2b = ROOT.TEfficiency("eff_tt2b","tthf efficiencies;p_{T} of softest gen bjet;efficiency",options.nbins,options.ptmin,options.ptmax)
eff_ttb = ROOT.TEfficiency("eff_ttb","tthf efficiencies;p_{T} of softest gen bjet;efficiency",options.nbins,options.ptmin,options.ptmax)

#chain.SetImplicitMT(True)

print chain.GetEntries()

chain.SetBranchStatus("*",0)
chain.SetBranchStatus("N_AdditionalGenBJets",1)
chain.SetBranchStatus("AdditionalGenBJet_Pt",1)
chain.SetBranchStatus("GenEvt_I_TTPlusBB",1)

chain.SetBranchAddress("GenEvt_I_TTPlusBB",tthf_flag)
chain.SetBranchAddress("N_AdditionalGenBJets",n_add_b_genjets)
chain.SetBranchAddress("AdditionalGenBJet_Pt",last_b_genjet_pt)

print ROOT.TSeqUL(chain.GetEntries())

for i in range(chain.GetEntries()):
    if i%10000==0:
        print i
    chain.GetEntry(i)
    #print tthf_flag[0]
    #print n_add_b_genjets[0]
    #print last_b_genjet_pt[0]
    passed_ttbb = (tthf_flag[0]==3)
    passed_tt2b = (tthf_flag[0]==2)
    passed_ttb = (tthf_flag[0]==1)
    if n_add_b_genjets[0]==0:
        eff_ttbb.Fill(passed_ttbb,0.)
        eff_tt2b.Fill(passed_tt2b,0.)
        eff_ttb.Fill(passed_ttb,0.)
    else:
        eff_ttbb.Fill(passed_ttbb,last_b_genjet_pt[n_add_b_genjets[0]-1])
        eff_tt2b.Fill(passed_tt2b,last_b_genjet_pt[n_add_b_genjets[0]-1])
        eff_ttb.Fill(passed_ttb,last_b_genjet_pt[n_add_b_genjets[0]-1])

for i in range(1,(eff_ttbb.GetTotalHistogram().GetNbinsX())+1):
    eff_ttbb.SetTotalEvents(i,chain.GetEntries())
for i in range(1,(eff_tt2b.GetTotalHistogram().GetNbinsX())+1):
    eff_tt2b.SetTotalEvents(i,chain.GetEntries())
for i in range(1,(eff_ttb.GetTotalHistogram().GetNbinsX())+1):
    eff_ttb.SetTotalEvents(i,chain.GetEntries())

c=ROOT.TCanvas()
c.SetLogy()    
eff_ttbb.SetFillStyle(3005)
eff_ttbb.SetFillColor(ROOT.kBlue)
eff_ttbb.SetLineColor(ROOT.kBlue)
eff_tt2b.SetFillStyle(3005)
eff_tt2b.SetFillColor(ROOT.kRed)
eff_tt2b.SetLineColor(ROOT.kRed)
eff_ttb.SetFillStyle(3005)
eff_ttb.SetFillColor(ROOT.kGreen)
eff_ttb.SetLineColor(ROOT.kGreen)
eff_ttbb.Draw()
c.Update()
eff_ttbb.GetPaintedGraph().SetMinimum(0.000001)
eff_ttbb.GetPaintedGraph().SetMaximum(0.1)
#eff_ttbb.GetPaintedGraph().GetXaxis().SetTitle("p_{T} of softest gen bjet")
#eff_ttbb.GetPaintedGraph().GetYaxis().SetTitle("efficieny")
c.Update()
eff_tt2b.Draw("same")
eff_ttb.Draw("same")
legend=ROOT.TLegend(0.15,0.15,0.35,0.35," ","NDC")
legend.AddEntry("eff_ttbb","ttbb","lep")
legend.AddEntry("eff_tt2b","tt2b","lep")
legend.AddEntry("eff_ttb","ttb","lep")
legend.SetTextSize(0.05)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
#legend.SetEntrySeparation(5.0)
legend.Draw("same")
year_channel = ROOT.TLatex()
year_channel.DrawLatexNDC(0.75,0.8,options.year+" "+options.channel)
#raw_input("bla")
c.Print(options.year+"_"+options.channel+"_ptmin"+str(options.ptmin)+"_"+"differential_tthf_effs.pdf")
f=ROOT.TFile.Open(options.year+"_"+options.channel+"_ptmin"+str(options.ptmin)+"_"+"differential_tthf_effs.root","RECREATE")
f.WriteTObject(eff_ttbb)
f.WriteTObject(eff_tt2b)
f.WriteTObject(eff_ttb)
f.Close()
#c.Clear()        
#graph = eff_ttbb.CreateGraph()
#print graph.GetN()
#print graph.GetX()[0]
#print graph.GetY()[0]


