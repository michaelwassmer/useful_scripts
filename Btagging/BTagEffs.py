import ROOT
import sys
from array import array

label = sys.argv[1]

input_files = sys.argv[2:]

chain = ROOT.TChain("MVATree")

for file in input_files:
    chain.Add(file)

# drop all branches
chain.SetBranchStatus("*",0)

# use only branches which are actually needed
chain.SetBranchStatus("N_AK15Jets",1)
chain.SetBranchStatus("N_Jets",1)
chain.SetBranchStatus("N_BTagsL",1)

chain.SetBranchStatus("Hadr_Recoil_Pt",1)
chain.SetBranchStatus("Jet_Pt",1)
chain.SetBranchStatus("Jet_Eta",1)
chain.SetBranchStatus("Jet_Flav",1)

chain.SetBranchStatus("LooseTaggedJet_Pt",1)
chain.SetBranchStatus("LooseTaggedJet_Eta",1)
chain.SetBranchStatus("LooseTaggedJet_Flav",1)

chain.SetBranchStatus("MediumTaggedJet_Pt",1)
chain.SetBranchStatus("MediumTaggedJet_Eta",1)
chain.SetBranchStatus("MediumTaggedJet_Flav",1)

chain.SetBranchStatus("JetLooseTagged_outside_lead_AK15Jet_Pt",1)
chain.SetBranchStatus("JetLooseTagged_outside_lead_AK15Jet_Eta",1)
chain.SetBranchStatus("JetLooseTagged_outside_lead_AK15Jet_Flav",1)

chain.SetBranchStatus("JetLooseUntagged_outside_lead_AK15Jet_Pt",1)
chain.SetBranchStatus("JetLooseUntagged_outside_lead_AK15Jet_Eta",1)
chain.SetBranchStatus("JetLooseUntagged_outside_lead_AK15Jet_Flav",1)

chain.SetBranchStatus("JetMediumTagged_outside_lead_AK15Jet_Pt",1)
chain.SetBranchStatus("JetMediumTagged_outside_lead_AK15Jet_Eta",1)
chain.SetBranchStatus("JetMediumTagged_outside_lead_AK15Jet_Flav",1)

N_Jets = array('i',[-1])
N_Jets_AK15 = array('i',[-1])
N_BTagsL = array('i',[-1])
N_BTagsM = array('i',[-1])

Hadr_Recoil_Pt = array('f',[-1])
Jet_Pt = array('f',30*[-1])
Jet_Eta = array('f',30*[-1])
Jet_Flav = array('f',30*[-1])

LooseTaggedJet_Pt = array('f',30*[-1])
LooseTaggedJet_Eta = array('f',30*[-1])
LooseTaggedJet_Flav = array('f',30*[-1])

TaggedJet_Pt = array('f',30*[-1])
TaggedJet_Eta = array('f',30*[-1])
TaggedJet_Flav = array('f',30*[-1])

chain.SetBranchAddress("N_AK15Jets",N_Jets_AK15)
chain.SetBranchAddress("Hadr_Recoil_Pt",Hadr_Recoil_Pt)
chain.SetBranchAddress("N_Jets",N_Jets)
chain.SetBranchAddress("N_BTagsL",N_BTagsL)
chain.SetBranchAddress("N_BTagsM",N_BTagsM)

chain.SetBranchAddress("Jet_Pt",Jet_Pt)
chain.SetBranchAddress("Jet_Eta",Jet_Eta)
chain.SetBranchAddress("Jet_Flav",Jet_Flav)

chain.SetBranchAddress("LooseTaggedJet_Pt",LooseTaggedJet_Pt)
chain.SetBranchAddress("LooseTaggedJet_Eta",LooseTaggedJet_Eta)
chain.SetBranchAddress("LooseTaggedJet_Flav",LooseTaggedJet_Flav)

chain.SetBranchAddress("MediumTaggedJet_Pt",TaggedJet_Pt)
chain.SetBranchAddress("MediumTaggedJet_Eta",TaggedJet_Eta)
chain.SetBranchAddress("MediumTaggedJet_Flav",TaggedJet_Flav)

# Jets outside of AK15
N_BTagsM_outside = array('i',[-1])
N_BTagsL_outside = array('i',[-1])
N_untagged_loose_outside = array('i',[-1])
chain.SetBranchAddress("N_JetsLooseUntagged_outside_lead_AK15Jet",N_untagged_loose_outside)
chain.SetBranchAddress("N_JetsMediumTagged_outside_lead_AK15Jet",N_BTagsM_outside)
chain.SetBranchAddress("N_JetsLooseTagged_outside_lead_AK15Jet",N_BTagsL_outside)

# Jet_Pt_outside = array('f',30*[-1])
# Jet_Eta_outside = array('f',30*[-1])
# Jet_Flav_outside = array('f',30*[-1])
# chain.SetBranchAddress("Jet_Pt",Jet_Pt_outside)
# chain.SetBranchAddress("Jet_Eta",Jet_Eta_outside)
# chain.SetBranchAddress("Jet_Flav",Jet_Flav_outside)

JetLooseTagged_outside_lead_AK15Jet_Pt = array('f',30*[-1])
JetLooseTagged_outside_lead_AK15Jet_Eta = array('f',30*[-1])
JetLooseTagged_outside_lead_AK15Jet_Flav = array('f',30*[-1])

JetLooseUntagged_outside_lead_AK15Jet_Pt = array('f',30*[-1])
JetLooseUntagged_outside_lead_AK15Jet_Eta = array('f',30*[-1])
JetLooseUntagged_outside_lead_AK15Jet_Flav = array('f',30*[-1])

JetMediumTagged_outside_lead_AK15Jet_Pt = array('f',30*[-1])
JetMediumTagged_outside_lead_AK15Jet_Eta = array('f',30*[-1])
JetMediumTagged_outside_lead_AK15Jet_Flav = array('f',30*[-1])

chain.SetBranchAddress("JetLooseTagged_outside_lead_AK15Jet_Pt",JetLooseTagged_outside_lead_AK15Jet_Pt)
chain.SetBranchAddress("JetLooseTagged_outside_lead_AK15Jet_Eta",JetLooseTagged_outside_lead_AK15Jet_Eta)
chain.SetBranchAddress("JetLooseTagged_outside_lead_AK15Jet_Flav",JetLooseTagged_outside_lead_AK15Jet_Flav)

chain.SetBranchAddress("JetLooseUntagged_outside_lead_AK15Jet_Pt",JetLooseUntagged_outside_lead_AK15Jet_Pt)
chain.SetBranchAddress("JetLooseUntagged_outside_lead_AK15Jet_Eta",JetLooseUntagged_outside_lead_AK15Jet_Eta)
chain.SetBranchAddress("JetLooseUntagged_outside_lead_AK15Jet_Flav",JetLooseUntagged_outside_lead_AK15Jet_Flav)

chain.SetBranchAddress("JetMediumTagged_outside_lead_AK15Jet_Pt",JetMediumTagged_outside_lead_AK15Jet_Pt)
chain.SetBranchAddress("JetMediumTagged_outside_lead_AK15Jet_Eta",JetMediumTagged_outside_lead_AK15Jet_Eta)
chain.SetBranchAddress("JetMediumTagged_outside_lead_AK15Jet_Flav",JetMediumTagged_outside_lead_AK15Jet_Flav)

binning_pt = [20.,30.,50.,70.,100.,140.,200.,300.,600.,1000.]
# binning_eta = [0.,1.4,2.0,2.5]
binning_eta = [0.,2.5]
binning_flavor = [-0.5,3.5,4.5,5.5]

all_jets = ROOT.TH3D("all_jets","all_jets",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
loose_btagged_jets = ROOT.TH3D("loose_btagged_jets","loose_btagged_jets",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
medium_btagged_jets = ROOT.TH3D("medium_btagged_jets","medium_btagged_jets",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))

all_jets_outside = ROOT.TH3D("all_jets_outside","all_jets_outside",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
loose_btagged_jets_outside = ROOT.TH3D("loose_btagged_jets_outside","loose_btagged_jets_outside",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
medium_btagged_jets_outside = ROOT.TH3D("medium_btagged_jets_outside","medium_btagged_jets_outside",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))


print "looping over",chain.GetEntries(),"events"
n_all = chain.GetEntries()
for i in range(n_all):
    if i % 100000 == 0:
        print("{n}/{all} = {frac:.2f} % done".format(n=i, all=n_all, frac=float(i)/float(n_all)*100 ))
    chain.GetEntry(i)
    if N_Jets_AK15[0] == 0:
        continue
    if Hadr_Recoil_Pt[0] < 250:
        continue
    for k in range(N_Jets[0]):
        all_jets.Fill(Jet_Pt[k],abs(Jet_Eta[k]),Jet_Flav[k])
    for l in range(N_BTagsL[0]):
        loose_btagged_jets.Fill(LooseTaggedJet_Pt[l],abs(LooseTaggedJet_Eta[l]),LooseTaggedJet_Flav[l])
    for m in range(N_BTagsM[0]):
        medium_btagged_jets.Fill(TaggedJet_Pt[m],abs(TaggedJet_Eta[m]),TaggedJet_Flav[m])
    # jets outside of AK15
    for m in range(N_BTagsM_outside[0]):
        medium_btagged_jets_outside.Fill(JetMediumTagged_outside_lead_AK15Jet_Pt[m],abs(JetMediumTagged_outside_lead_AK15Jet_Eta[m]),JetMediumTagged_outside_lead_AK15Jet_Flav[m])
    for m in range(N_BTagsL_outside[0]):
        loose_btagged_jets_outside.Fill(JetLooseTagged_outside_lead_AK15Jet_Pt[m],abs(JetLooseTagged_outside_lead_AK15Jet_Eta[m]),JetLooseTagged_outside_lead_AK15Jet_Flav[m])
        all_jets_outside.Fill(JetLooseTagged_outside_lead_AK15Jet_Pt[m],abs(JetLooseTagged_outside_lead_AK15Jet_Eta[m]),JetLooseTagged_outside_lead_AK15Jet_Flav[m])
    for k in range(N_untagged_loose_outside[0]):
        all_jets_outside.Fill(JetLooseUntagged_outside_lead_AK15Jet_Pt[k],abs(JetLooseUntagged_outside_lead_AK15Jet_Eta[k]),JetLooseUntagged_outside_lead_AK15Jet_Flav[k])

loose_btagging_efficiency = loose_btagged_jets.Clone()
loose_btagging_efficiency.SetName("loose_btagging_efficiency")
loose_btagging_efficiency.SetTitle("loose_btagging_efficiency")
loose_btagging_efficiency.Divide(all_jets)

medium_btagging_efficiency = medium_btagged_jets.Clone()
medium_btagging_efficiency.SetName("medium_btagging_efficiency")
medium_btagging_efficiency.SetTitle("medium_btagging_efficiency")
medium_btagging_efficiency.Divide(all_jets)

loose_btagging_efficiency_outside = loose_btagged_jets_outside.Clone()
loose_btagging_efficiency_outside.SetName("loose_btagging_efficiency_outside")
loose_btagging_efficiency_outside.SetTitle("loose_btagging_efficiency_outside")
loose_btagging_efficiency_outside.Divide(all_jets_outside)

medium_btagging_efficiency_outside = medium_btagged_jets_outside.Clone()
medium_btagging_efficiency_outside.SetName("medium_btagging_efficiency_outside")
medium_btagging_efficiency_outside.SetTitle("medium_btagging_efficiency_outside")
medium_btagging_efficiency_outside.Divide(all_jets_outside)

output_file = ROOT.TFile.Open("btag_efficiencies_"+label+".root","RECREATE")

for hist3D in [ all_jets,loose_btagged_jets,medium_btagged_jets,loose_btagging_efficiency,medium_btagging_efficiency,
                all_jets_outside,loose_btagged_jets_outside,medium_btagged_jets_outside,loose_btagging_efficiency_outside,medium_btagging_efficiency_outside]:
    hist3D.GetXaxis().SetTitle("p_{T}")
    hist3D.GetYaxis().SetTitle("|#eta|")
    hist3D.GetZaxis().SetTitle("hadron flavor")
    output_file.WriteTObject(hist3D)

output_file.Close()
