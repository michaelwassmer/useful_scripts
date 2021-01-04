import ROOT
import sys

xs_file = ROOT.TFile.Open(sys.argv[1])
correction_file = ROOT.TFile.Open(sys.argv[2])
boson = sys.argv[3]

xs = xs_file.Get(boson+"_boson_pt")
xs_muRUp = xs_file.Get(boson+"_boson_pt"+"_"+"Weight_scale_variation_muR_2p0_muF_1p0")
xs_muRDown = xs_file.Get(boson+"_boson_pt"+"_"+"Weight_scale_variation_muR_0p5_muF_1p0")
xs_muFUp = xs_file.Get(boson+"_boson_pt"+"_"+"Weight_scale_variation_muR_1p0_muF_2p0")
xs_muFDown = xs_file.Get(boson+"_boson_pt"+"_"+"Weight_scale_variation_muR_1p0_muF_0p5")

boson_ = sys.argv[4]

correction = correction_file.Get(boson_+"_NNLO_NLO_nnn_nnn_n")
correction_muRUp = correction_file.Get(boson_+"_NNLO_NLO_nnn_nnn_n"+"_"+"Weight_scale_variation_muR_2p0_muF_1p0")
correction_muRDown = correction_file.Get(boson_+"_NNLO_NLO_nnn_nnn_n"+"_"+"Weight_scale_variation_muR_0p5_muF_1p0")
correction_muFUp = correction_file.Get(boson_+"_NNLO_NLO_nnn_nnn_n"+"_"+"Weight_scale_variation_muR_1p0_muF_2p0")
correction_muFDown = correction_file.Get(boson_+"_NNLO_NLO_nnn_nnn_n"+"_"+"Weight_scale_variation_muR_1p0_muF_0p5")

vpt_threshold = float(sys.argv[5])

bin_threshold = xs.FindBin(vpt_threshold)

#total_xs_before = xs.GetBinContent(0)+xs.Integral()
#total_xs_before_muRUp = xs_muRUp.GetBinContent(0)+xs_muRUp.Integral()
#total_xs_before_muRDown = xs_muRDown.GetBinContent(0)+xs_muRDown.Integral()
#total_xs_before_muFUp = xs_muFUp.GetBinContent(0)+xs_muFUp.Integral()
#total_xs_before_muFDown = xs_muFDown.GetBinContent(0)+xs_muFDown.Integral()

for cross_sec,corr,label in zip([xs,xs_muRUp,xs_muRDown,xs_muFUp,xs_muFDown],[correction,correction_muRUp,correction_muRDown,correction_muFUp,correction_muFDown],["nominal","muRUp","muRDown","muFUp","muFDown"]):
    total_xs_after = 0
    total_xs_before = 0
    #print cross_sec
    for i in range(0,bin_threshold):
        #print cross_sec.GetBinContent(i)
        total_xs_after += cross_sec.GetBinContent(i)
        total_xs_before += cross_sec.GetBinContent(i)
    for i in range(bin_threshold,cross_sec.GetNbinsX()+1):
        total_xs_after += (cross_sec.GetBinContent(i)*corr.GetBinContent(i))
        total_xs_before += cross_sec.GetBinContent(i)
    
    print label+" "+"xs before:",round(total_xs_before,3)
    print label+" "+"xs after:",round(total_xs_after,3)
    print label+" "+"xs after / xs before:", round(total_xs_after*1./total_xs_before,3)
