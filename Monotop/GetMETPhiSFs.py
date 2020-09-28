import ROOT
import sys

input_file = sys.argv[1]

cats = ["lep_SR_Mu","lep_SR_El","lep_CR_WMu","lep_CR_WEl","lep_CR_ttbarMu","lep_CR_ttbarEl"]

variable =  "Evt_Phi_MET"

mc_processes = "pseudodata_obs"

data = "data_obs"

file=ROOT.TFile.Open(input_file,"READ")

outfile=ROOT.TFile.Open("METPhi_SFs.root","RECREATE")

for cat in cats:
    data_hist = file.Get(data+"_"+variable+"_"+cat).Clone()
    mc_hist = file.Get(mc_processes+"_"+variable+"_"+cat).Clone()
    data_hist.Scale(1./data_hist.Integral())
    mc_hist.Scale(1./mc_hist.Integral())
    ratio=data_hist.Clone()
    ratio.Divide(mc_hist)
    ratio.SetName(variable+"_"+cat+"_"+"SFs")
    ratio.SetTitle(variable+"_"+cat+"_"+"SFs")
    outfile.WriteTObject(ratio)

outfile.Close()
file.Close()
