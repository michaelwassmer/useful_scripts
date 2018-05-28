import ROOT
import sys

ROOT.gROOT.SetBatch(True)

process = sys.argv[1]

file_TH = ROOT.TFile.Open(process+".root")

hists = {}

for key in file_TH.GetListOfKeys():
    hists[key.GetName()] = file_TH.Get(key.GetName())

def K_TH(QCD_ORDER,EW_ORDER,e_QCD=[],e_EW=[],e_MIX = 0.):
    Kappa_EW = file_TH.Get(process+"_pTV_kappa_"+EW_ORDER+"_EW")
    for i,e in enumerate(e_EW):
        dKappa_EW = file_TH.Get(process+"_pTV_d"+str(i+1)+"kappa_EW")
        dKappa_EW.Scale(e)
        Kappa_EW = Kappa_EW + dKappa_EW
    for i in range(Kappa_EW.GetNbinsX()):
        Kappa_EW.SetBinContent(i,1.+Kappa_EW.GetBinContent(i))
    K_QCD = file_TH.Get(process+"_pTV_K_"+QCD_ORDER)
    for i,e in enumerate(e_QCD):
        dK_QCD = file_TH.Get(process+"_pTV_d"+str(i+1)+"K_"+QCD_ORDER)
        dK_QCD.Scale(e)
        K_QCD = K_QCD + dK_QCD
    prod = K_QCD*Kappa_EW
    dK_MIX = file_TH.Get(process+"_pTV_dK_"+QCD_ORDER+"_mix")
    dK_MIX.Scale(e_MIX)
    return prod + dK_MIX

def sigma_TH(QCD_ORDER,EW_ORDER,e_QCD=[],e_EW=[],e_MIX = 0.):
    sigma_QCD_LO = file_TH.Get(process+"_pTV_"+"LO")
    return K_TH(QCD_ORDER,EW_ORDER,e_QCD,e_EW,e_MIX)*sigma_QCD_LO

test = sigma_TH("NNLO","NLO",[0.,0.,0.],[0.,0.,0.],0.)

c = ROOT.TCanvas()

test.Draw("histe")

c.SaveAs("test.pdf")
