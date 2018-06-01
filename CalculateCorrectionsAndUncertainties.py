import ROOT
import sys

ROOT.gROOT.SetBatch(True)

process = sys.argv[1]

str_dict = {1. : "u" , -1. : "d", 0. : "n"}

file_TH = ROOT.TFile.Open(process+".root")

#hists = {}

#for key in file_TH.GetListOfKeys():
    #hists[key.GetName()] = file_TH.Get(key.GetName())

def K_TH(QCD_ORDER,EW_ORDER,e_QCD=[],e_EW=[],e_MIX = 0.):
    Kappa_EW = file_TH.Get(process+"_pTV_kappa_"+EW_ORDER+"_EW").Clone()+file_TH.Get(process+"_pTV_kappa_NNLO_Sud").Clone()
    for i,e in enumerate(e_EW):
        dKappa_EW = file_TH.Get(process+"_pTV_d"+str(i+1)+"kappa_EW").Clone()
        dKappa_EW.Scale(e)
        Kappa_EW = Kappa_EW + dKappa_EW
    for i in range(Kappa_EW.GetNbinsX()):
        Kappa_EW.SetBinContent(i,1.+Kappa_EW.GetBinContent(i))
    K_QCD = file_TH.Get(process+"_pTV_K_"+QCD_ORDER).Clone()
    for i,e in enumerate(e_QCD):
        dK_QCD = file_TH.Get(process+"_pTV_d"+str(i+1)+"K_"+QCD_ORDER).Clone()
        dK_QCD.Scale(e)
        K_QCD = K_QCD + dK_QCD
    prod = K_QCD*Kappa_EW
    dK_MIX = file_TH.Get(process+"_pTV_dK_"+QCD_ORDER+"_mix").Clone()
    dK_MIX.Scale(e_MIX)
    return prod + dK_MIX

def sigma_TH(QCD_ORDER,EW_ORDER,e_QCD=[],e_EW=[],e_MIX = 0.):
    sigma_QCD_LO = file_TH.Get(process+"_pTV_"+"LO").Clone()
    sigma_TH = K_TH(QCD_ORDER,EW_ORDER,e_QCD,e_EW,e_MIX)*sigma_QCD_LO
    str_QCD = ""
    str_EW = ""
    str_MIX = ""
    for e in e_QCD:
        str_QCD+=str_dict[e]
    for e in e_EW:
        str_EW+=str_dict[e]
    str_MIX+=str_dict[e_MIX]
    sigma_TH.SetName(process+"_"+QCD_ORDER+"_"+EW_ORDER+"_"+str_QCD+"_"+str_EW+"_"+str_MIX)
    sigma_TH.SetTitle(process+"_"+QCD_ORDER+"_"+EW_ORDER+"_"+str_QCD+"_"+str_EW+"_"+str_MIX)
    # scale the theory prediction with 2 if the process is W->lv since the theory histograms only include one flavor (e or mu)
    if process=="evj":
        sigma_TH.Scale(2.)
    return sigma_TH

output = ROOT.TFile("TheoryXS_"+process+".root","RECREATE")


test = sigma_TH("NNLO","NLO",[0.,0.,0.],[0.,0.,0.],0.)

output_hists = [sigma_TH("NNLO","NLO",[e_QCD1,e_QCD2,e_QCD3],[e_EW1,e_EW2,e_EW3],e_MIX) for e_QCD1 in [1,0,-1] for e_QCD2 in [1,0,-1] for e_QCD3 in [1,0,-1] for e_EW1 in [1,0,-1] for e_EW2 in [1,0,-1] for e_EW3 in [1,0,-1] for e_MIX in [1,0,-1]]
print len(output_hists)


file_mc=None
hist_mc=None
if process=="vvj":
    file_mc = ROOT.TFile.Open("root_files/Z_boson_pt.root")
    hist_mc = file_mc.Get("Z_boson_pt")
elif process=="evj":
    file_mc = ROOT.TFile.Open("root_files/W_boson_pt.root")
    hist_mc = file_mc.Get("W_boson_pt")
else:
    print "wrong option"
    exit()

for hist in output_hists:
    hist.Divide(hist_mc)
    output.WriteTObject(hist)

output.Close()
