import sys
import ROOT

label = sys.argv[1]
f_ref_path = sys.argv[2]
f_probe_path = sys.argv[3]

if not "eff" in label:
    print("you forgot eff in label")
    exit()

f_ref = ROOT.TFile.Open(f_ref_path, "READ")
f_probe = ROOT.TFile.Open(f_probe_path, "READ")

keys_ref = [key.GetName() for key in f_ref.GetListOfKeys()]
keys_probe = [key.GetName() for key in f_probe.GetListOfKeys()]

if not (keys_ref==keys_probe):
    print("keys in files are not similar")
    print("exiting ...")
    exit(1)

effs = []

for key in keys_ref:
    h_ref = f_ref.Get(key).Clone(key+"_ref")
    h_probe = f_probe.Get(key).Clone(key+"_probe")
    eff = ROOT.TEfficiency(h_probe,h_ref)
    #eff.Draw()
    #input("bla")
    eff.SetName("trig_eff_"+key)
    effs.append(eff)

f_ref.Close()
f_probe.Close()

print(effs)

f_out = ROOT.TFile(label+".root","RECREATE")
for eff in effs:
    f_out.WriteTObject(eff)

f_out.Close()
