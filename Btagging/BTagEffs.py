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
chain.SetBranchStatus("N_Jets",1)
chain.SetBranchStatus("N_BTagsL",1)

chain.SetBranchStatus("Jet_Pt",1)
chain.SetBranchStatus("Jet_Eta",1)
chain.SetBranchStatus("Jet_Flav",1)

chain.SetBranchStatus("LooseTaggedJet_Pt",1)
chain.SetBranchStatus("LooseTaggedJet_Eta",1)
chain.SetBranchStatus("LooseTaggedJet_Flav",1)

N_Jets = array('i',[-1])
N_BTagsL = array('i',[-1])
N_BTagsM = array('i',[-1])

Jet_Pt = array('f',30*[-1])
Jet_Eta = array('f',30*[-1])
Jet_Flav = array('f',30*[-1])

LooseTaggedJet_Pt = array('f',30*[-1])
LooseTaggedJet_Eta = array('f',30*[-1])
LooseTaggedJet_Flav = array('f',30*[-1])

TaggedJet_Pt = array('f',30*[-1])
TaggedJet_Eta = array('f',30*[-1])
TaggedJet_Flav = array('f',30*[-1])

chain.SetBranchAddress("N_Jets",N_Jets)
chain.SetBranchAddress("N_BTagsL",N_BTagsL)
chain.SetBranchAddress("N_BTagsM",N_BTagsM)

chain.SetBranchAddress("Jet_Pt",Jet_Pt)
chain.SetBranchAddress("Jet_Eta",Jet_Eta)
chain.SetBranchAddress("Jet_Flav",Jet_Flav)

chain.SetBranchAddress("LooseTaggedJet_Pt",LooseTaggedJet_Pt)
chain.SetBranchAddress("LooseTaggedJet_Eta",LooseTaggedJet_Eta)
chain.SetBranchAddress("LooseTaggedJet_Flav",LooseTaggedJet_Flav)

chain.SetBranchAddress("TaggedJet_Pt",TaggedJet_Pt)
chain.SetBranchAddress("TaggedJet_Eta",TaggedJet_Eta)
chain.SetBranchAddress("TaggedJet_Flav",TaggedJet_Flav)

binning_pt = [20.,30.,50.,70.,100.,140.,200.,300.,600.,1000.]
binning_eta = [0.,1.4,2.0,2.5]
binning_flavor = [-0.5,3.5,4.5,5.5]

all_jets = ROOT.TH3D("all_jets","all_jets",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
loose_btagged_jets = ROOT.TH3D("loose_btagged_jets","loose_btagged_jets",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
medium_btagged_jets = ROOT.TH3D("medium_btagged_jets","medium_btagged_jets",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))

print "looping over",chain.GetEntries(),"events"

for i in range(chain.GetEntries()):
    if i % 10000 == 0:
        print i
    chain.GetEntry(i)
    for k in range(N_Jets[0]):
        all_jets.Fill(Jet_Pt[k],abs(Jet_Eta[k]),Jet_Flav[k])
    for l in range(N_BTagsL[0]):
        loose_btagged_jets.Fill(LooseTaggedJet_Pt[l],abs(LooseTaggedJet_Eta[l]),LooseTaggedJet_Flav[l])
    for m in range(N_BTagsM[0]):
        medium_btagged_jets.Fill(TaggedJet_Pt[m],abs(TaggedJet_Eta[m]),TaggedJet_Flav[m])

loose_btagging_efficiency = loose_btagged_jets.Clone()
loose_btagging_efficiency.SetName("loose_btagging_efficiency")
loose_btagging_efficiency.SetTitle("loose_btagging_efficiency")
loose_btagging_efficiency.Divide(all_jets)

medium_btagging_efficiency = medium_btagged_jets.Clone()
medium_btagging_efficiency.SetName("medium_btagging_efficiency")
medium_btagging_efficiency.SetTitle("medium_btagging_efficiency")
medium_btagging_efficiency.Divide(all_jets)

output_file = ROOT.TFile.Open("btag_efficiencies_"+label+".root","RECREATE")

for hist3D in [all_jets,loose_btagged_jets,medium_btagged_jets,loose_btagging_efficiency,medium_btagging_efficiency]:
    hist3D.GetXaxis().SetTitle("p_{T}")
    hist3D.GetYaxis().SetTitle("|#eta|")
    hist3D.GetZaxis().SetTitle("hadron flavor")
    output_file.WriteTObject(hist3D)

output_file.Close()
