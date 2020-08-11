import sys
import ROOT

label = sys.argv[1]

zvv_th_xs_file = sys.argv[2]
zll_th_xs_file = sys.argv[3]
w_th_xs_file = sys.argv[4]
g_th_xs_file = sys.argv[5]

zvv_sample_xs_file = sys.argv[6]
zll_sample_xs_file = sys.argv[7]
w_sample_xs_file = sys.argv[8]
g_sample_xs_file = sys.argv[9]

# open root files containing theory cross sections
zvv_th_xs = ROOT.TFile.Open(zvv_th_xs_file,"READ")
zll_th_xs = ROOT.TFile.Open(zll_th_xs_file,"READ")
w_th_xs = ROOT.TFile.Open(w_th_xs_file,"READ")
g_th_xs = ROOT.TFile.Open(g_th_xs_file,"READ")

# open root files containing sample cross sections
zvv_sample_xs = ROOT.TFile.Open(zvv_sample_xs_file,"READ")
zll_sample_xs = ROOT.TFile.Open(zll_sample_xs_file,"READ")
w_sample_xs = ROOT.TFile.Open(w_sample_xs_file,"READ")
g_sample_xs = ROOT.TFile.Open(g_sample_xs_file,"READ")

# get cross sections for zvv
zvv_lo_xs = zvv_th_xs.Get("vvj_pTV_LO")
zvv_nlo_xs = zvv_th_xs.Get("vvj_pTV_NLO")
zvv_nnlo_xs = zvv_th_xs.Get("vvj_pTV_NNLO")
zvv_mc_xs = zvv_sample_xs.Get("Zvv_boson_pt")

# get cross sections for zll
zll_lo_xs = zll_th_xs.Get("eej_pTV_LO")
zll_nlo_xs = zll_th_xs.Get("eej_pTV_NLO")
zll_nnlo_xs = zll_th_xs.Get("eej_pTV_NNLO")
zll_mc_xs = zll_sample_xs.Get("Zll_boson_pt")

# get cross sections for w
w_lo_xs = w_th_xs.Get("evj_pTV_LO")
w_nlo_xs = w_th_xs.Get("evj_pTV_NLO")
w_nnlo_xs = w_th_xs.Get("evj_pTV_NNLO")
w_mc_xs = w_sample_xs.Get("W_boson_pt")

# get cross sections for gamma
g_lo_xs = g_th_xs.Get("aj_pTV_LO")
g_nlo_xs = g_th_xs.Get("aj_pTV_NLO")
g_nnlo_xs = g_th_xs.Get("aj_pTV_NNLO")
g_mc_xs = g_sample_xs.Get("G_boson_pt")

# scale cross section with factor 3 since the theory cross sections are only calculated for one lepton generation
for xs in [zll_lo_xs, zll_nlo_xs, zll_nnlo_xs, w_lo_xs, w_nlo_xs, w_nnlo_xs]:
    xs.Scale(3)

if "2016" in label:
    zvv_mc_xs.Scale(3)

output_file = ROOT.TFile.Open("QCDXSvsSampleXS_"+label+".root","RECREATE")

all_xs = [zvv_lo_xs, zvv_nlo_xs, zvv_nnlo_xs, zvv_mc_xs, zll_lo_xs, zll_nlo_xs, zll_nnlo_xs, zll_mc_xs, w_lo_xs, w_nlo_xs, w_nnlo_xs, w_mc_xs, g_lo_xs, g_nlo_xs, g_nnlo_xs, g_mc_xs]

for xs in all_xs:
    output_file.WriteTObject(xs)

output_file.Close()

for file in [zvv_th_xs, zll_th_xs, w_th_xs, g_th_xs, zvv_sample_xs, zll_sample_xs, w_sample_xs, g_sample_xs]:
    file.Close()
