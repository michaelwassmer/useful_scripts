import ROOT

ROOT.gROOT.SetBatch(True)

file_TH = ROOT.TFile.Open("evj.root")



hist_K_LO = file_TH.Get("evj_pTV_K_LO")
hist_kappa_NLO = file_TH.Get("evj_pTV_kappa_NLO_EW")
hist_kappa_NNLO = file_TH.Get("evj_pTV_kappa_NNLO_Sud")
hist_K_NNLO = file_TH.Get("evj_pTV_K_NNLO")
hist_QCD_LO = file_TH.Get("evj_pTV_LO")

hist_K_TH = hist_K_NNLO + ((hist_kappa_NNLO+hist_kappa_NLO)*hist_K_LO)

hist_sigma_TH = hist_K_TH*hist_QCD_LO
hist_sigma_TH.Scale(2.)#theory predictions are only made for one lepton flavor

print "test"

file_MC = ROOT.TFile.Open("root_files/W_boson_pt.root")
hist_MC = file_MC.Get("W_boson_pt")

print "test"

print hist_MC.GetBinContent(1)
print hist_sigma_TH.GetBinContent(1)

ratio = hist_sigma_TH.Clone("clone")

ratio.Divide(hist_MC)

print ratio.GetBinContent(1)

ratio.GetXaxis().SetRangeUser(100.,1000.)
c = ROOT.TCanvas()

ratio.Draw("histe")

c.SaveAs("CompareTHwithMC_evj.pdf")