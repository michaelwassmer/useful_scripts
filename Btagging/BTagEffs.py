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

# number of jets
chain.SetBranchStatus("N_AK15Jets",1)
chain.SetBranchStatus("N_Jets",1)
N_Jets = array('i',[-1])
N_Jets_AK15 = array('i',[-1])
chain.SetBranchAddress("N_AK15Jets",N_Jets_AK15)
chain.SetBranchAddress("N_Jets",N_Jets)

# number of btags
chain.SetBranchStatus("N_BTagsL",1)
chain.SetBranchStatus("N_BTagsM",1)
chain.SetBranchStatus("N_JetsLooseUntagged_outside_lead_AK15Jet",1)
chain.SetBranchStatus("N_JetsMediumTagged_outside_lead_AK15Jet",1)
chain.SetBranchStatus("N_JetsLooseTagged_outside_lead_AK15Jet",1)
N_BTagsL = array('i',[-1])
N_BTagsM = array('i',[-1])
N_untagged_loose_outside = array('i',[-1])
N_BTagsM_outside = array('i',[-1])
N_BTagsL_outside = array('i',[-1])
chain.SetBranchAddress("N_BTagsL",N_BTagsL)
chain.SetBranchAddress("N_BTagsM",N_BTagsM)
chain.SetBranchAddress("N_JetsLooseUntagged_outside_lead_AK15Jet",N_untagged_loose_outside)
chain.SetBranchAddress("N_JetsMediumTagged_outside_lead_AK15Jet",N_BTagsM_outside)
chain.SetBranchAddress("N_JetsLooseTagged_outside_lead_AK15Jet",N_BTagsL_outside)

# number of leptons
chain.SetBranchStatus("N_Taus",1)
chain.SetBranchStatus("N_LooseElectrons",1)
chain.SetBranchStatus("N_LoosePhotons",1)
chain.SetBranchStatus("N_LooseMuons",1)
chain.SetBranchStatus("N_TightMuons",1)
chain.SetBranchStatus("N_TightElectrons",1)
N_Taus = array('i',[-1])
N_LooseElectrons = array('i',[-1])
N_LoosePhotons = array('i',[-1])
N_LooseMuons = array('i',[-1])
N_TightMuons = array('i',[-1])
N_TightElectrons = array('i',[-1])
chain.SetBranchAddress("N_Taus",N_Taus)
chain.SetBranchAddress("N_LooseElectrons",N_LooseElectrons)
chain.SetBranchAddress("N_LoosePhotons",N_LoosePhotons)
chain.SetBranchAddress("N_LooseMuons",N_LooseMuons)
chain.SetBranchAddress("N_TightMuons",N_TightMuons)
chain.SetBranchAddress("N_TightElectrons",N_TightElectrons)

# number of HEM jets (only important for 2018)
N_HEM_Jets = array('i',[-1])
if "2018" in label:
    chain.SetBranchStatus("N_HEM_Jets",1)
    chain.SetBranchAddress("N_HEM_Jets",N_HEM_Jets)
else:
    N_HEM_Jets[0] = 0

# jet properties important for btagging efficienies ...

# ... for all jets
chain.SetBranchStatus("Jet_Pt",1)
chain.SetBranchStatus("Jet_Eta",1)
chain.SetBranchStatus("Jet_Flav",1)
Jet_Pt = array('f',30*[-1])
Jet_Eta = array('f',30*[-1])
Jet_Flav = array('f',30*[-1])
chain.SetBranchAddress("Jet_Pt",Jet_Pt)
chain.SetBranchAddress("Jet_Eta",Jet_Eta)
chain.SetBranchAddress("Jet_Flav",Jet_Flav)

# ... for all loose tagged jets
chain.SetBranchStatus("LooseTaggedJet_Pt",1)
chain.SetBranchStatus("LooseTaggedJet_Eta",1)
chain.SetBranchStatus("LooseTaggedJet_Flav",1)
LooseTaggedJet_Pt = array('f',30*[-1])
LooseTaggedJet_Eta = array('f',30*[-1])
LooseTaggedJet_Flav = array('f',30*[-1])
chain.SetBranchAddress("LooseTaggedJet_Pt",LooseTaggedJet_Pt)
chain.SetBranchAddress("LooseTaggedJet_Eta",LooseTaggedJet_Eta)
chain.SetBranchAddress("LooseTaggedJet_Flav",LooseTaggedJet_Flav)

# ... for all medium tagged jets
chain.SetBranchStatus("MediumTaggedJet_Pt",1)
chain.SetBranchStatus("MediumTaggedJet_Eta",1)
chain.SetBranchStatus("MediumTaggedJet_Flav",1)
MediumTaggedJet_Pt = array('f',30*[-1])
MediumTaggedJet_Eta = array('f',30*[-1])
MediumTaggedJet_Flav = array('f',30*[-1])
chain.SetBranchAddress("MediumTaggedJet_Pt",MediumTaggedJet_Pt)
chain.SetBranchAddress("MediumTaggedJet_Eta",MediumTaggedJet_Eta)
chain.SetBranchAddress("MediumTaggedJet_Flav",MediumTaggedJet_Flav)

# ... for all loose tagged jets outside of the leading ak15 jet
chain.SetBranchStatus("JetLooseTagged_outside_lead_AK15Jet_Pt",1)
chain.SetBranchStatus("JetLooseTagged_outside_lead_AK15Jet_Eta",1)
chain.SetBranchStatus("JetLooseTagged_outside_lead_AK15Jet_Flav",1)
JetLooseTagged_outside_lead_AK15Jet_Pt = array('f',30*[-1])
JetLooseTagged_outside_lead_AK15Jet_Eta = array('f',30*[-1])
JetLooseTagged_outside_lead_AK15Jet_Flav = array('f',30*[-1])
chain.SetBranchAddress("JetLooseTagged_outside_lead_AK15Jet_Pt",JetLooseTagged_outside_lead_AK15Jet_Pt)
chain.SetBranchAddress("JetLooseTagged_outside_lead_AK15Jet_Eta",JetLooseTagged_outside_lead_AK15Jet_Eta)
chain.SetBranchAddress("JetLooseTagged_outside_lead_AK15Jet_Flav",JetLooseTagged_outside_lead_AK15Jet_Flav)

# ... for all loose untagged jets outside of the leading ak15 jet
chain.SetBranchStatus("JetLooseUntagged_outside_lead_AK15Jet_Pt",1)
chain.SetBranchStatus("JetLooseUntagged_outside_lead_AK15Jet_Eta",1)
chain.SetBranchStatus("JetLooseUntagged_outside_lead_AK15Jet_Flav",1)
JetLooseUntagged_outside_lead_AK15Jet_Pt = array('f',30*[-1])
JetLooseUntagged_outside_lead_AK15Jet_Eta = array('f',30*[-1])
JetLooseUntagged_outside_lead_AK15Jet_Flav = array('f',30*[-1])
chain.SetBranchAddress("JetLooseUntagged_outside_lead_AK15Jet_Pt",JetLooseUntagged_outside_lead_AK15Jet_Pt)
chain.SetBranchAddress("JetLooseUntagged_outside_lead_AK15Jet_Eta",JetLooseUntagged_outside_lead_AK15Jet_Eta)
chain.SetBranchAddress("JetLooseUntagged_outside_lead_AK15Jet_Flav",JetLooseUntagged_outside_lead_AK15Jet_Flav)

# ... for all medium tagged jets outside of the leading ak15 jet
chain.SetBranchStatus("JetMediumTagged_outside_lead_AK15Jet_Pt",1)
chain.SetBranchStatus("JetMediumTagged_outside_lead_AK15Jet_Eta",1)
chain.SetBranchStatus("JetMediumTagged_outside_lead_AK15Jet_Flav",1)
JetMediumTagged_outside_lead_AK15Jet_Pt = array('f',30*[-1])
JetMediumTagged_outside_lead_AK15Jet_Eta = array('f',30*[-1])
JetMediumTagged_outside_lead_AK15Jet_Flav = array('f',30*[-1])
chain.SetBranchAddress("JetMediumTagged_outside_lead_AK15Jet_Pt",JetMediumTagged_outside_lead_AK15Jet_Pt)
chain.SetBranchAddress("JetMediumTagged_outside_lead_AK15Jet_Eta",JetMediumTagged_outside_lead_AK15Jet_Eta)
chain.SetBranchAddress("JetMediumTagged_outside_lead_AK15Jet_Flav",JetMediumTagged_outside_lead_AK15Jet_Flav)

# variables to define analysis-level phase space for btagging efficiencies
chain.SetBranchStatus("DeltaPhi_AK4Jet_Hadr_Recoil",1)
chain.SetBranchStatus("DeltaPhi_AK4Jet_MET",1)
chain.SetBranchStatus("Hadr_Recoil_Pt",1)
chain.SetBranchStatus("M_W_transverse",1)
chain.SetBranchStatus("Evt_Pt_MET",1)
DeltaPhi_AK4Jet_Hadr_Recoil = array('f',30*[-1])
DeltaPhi_AK4Jet_MET = array('f',30*[-1])
Hadr_Recoil_Pt = array('f',[-1])
M_W_transverse = array('f',[-1])
Evt_Pt_MET = array('f',[-1])
chain.SetBranchAddress("DeltaPhi_AK4Jet_Hadr_Recoil",DeltaPhi_AK4Jet_Hadr_Recoil)
chain.SetBranchAddress("DeltaPhi_AK4Jet_MET",DeltaPhi_AK4Jet_MET)
chain.SetBranchAddress("Hadr_Recoil_Pt",Hadr_Recoil_Pt)
chain.SetBranchAddress("M_W_transverse",M_W_transverse)
chain.SetBranchAddress("Evt_Pt_MET",Evt_Pt_MET)


# Jet_Pt_outside = array('f',30*[-1])
# Jet_Eta_outside = array('f',30*[-1])
# Jet_Flav_outside = array('f',30*[-1])
# chain.SetBranchAddress("Jet_Pt",Jet_Pt_outside)
# chain.SetBranchAddress("Jet_Eta",Jet_Eta_outside)
# chain.SetBranchAddress("Jet_Flav",Jet_Flav_outside)

# binning for btagging scale factors from BTV group
binning_pt = [20.,30.,50.,70.,100.,140.,200.,300.,600.,1000.]
# binning_eta = [0.,1.4,2.0,2.5]
binning_eta = [0.,2.5]
binning_flavor = [-0.5,3.5,4.5,5.5]

# hadronic analysis channel
all_jets_hadronic = ROOT.TH3D("all_jets_hadronic","all_jets_hadronic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
loose_btagged_jets_hadronic = ROOT.TH3D("loose_btagged_jets_hadronic","loose_btagged_jets_hadronic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
medium_btagged_jets_hadronic = ROOT.TH3D("medium_btagged_jets_hadronic","medium_btagged_jets_hadronic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))

all_jets_outside_hadronic = ROOT.TH3D("all_jets_outside_hadronic","all_jets_outside_hadronic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
loose_btagged_jets_outside_hadronic = ROOT.TH3D("loose_btagged_jets_outside_hadronic","loose_btagged_jets_outside_hadronic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
medium_btagged_jets_outside_hadronic = ROOT.TH3D("medium_btagged_jets_outside_hadronic","medium_btagged_jets_outside_hadronic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))

# leptonic analysis channel
all_jets_leptonic = ROOT.TH3D("all_jets_leptonic","all_jets_leptonic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
loose_btagged_jets_leptonic = ROOT.TH3D("loose_btagged_jets_leptonic","loose_btagged_jets_leptonic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))
medium_btagged_jets_leptonic = ROOT.TH3D("medium_btagged_jets_leptonic","medium_btagged_jets_leptonic",len(binning_pt)-1,array('f',binning_pt),len(binning_eta)-1,array('f',binning_eta),len(binning_flavor)-1,array('f',binning_flavor))


print "looping over",chain.GetEntries(),"events"
n_all = chain.GetEntries()
for i in range(n_all):
    if i % 100000 == 0:
        print("{n}/{all} = {frac:.2f} % done".format(n=i, all=n_all, frac=float(i)/float(n_all)*100 ))
    chain.GetEntry(i)
    HEMcut = N_HEM_Jets[0] == 0
    isHadronic = HEMcut and N_Jets_AK15[0]>0 and Hadr_Recoil_Pt[0]>250. and N_Taus[0]==0 and N_Jets[0]>0\
                        and min(DeltaPhi_AK4Jet_Hadr_Recoil[0:N_Jets[0]])>0.8
    isLeptonic = HEMcut and Evt_Pt_MET[0]>100. and N_Jets[0]>0 and N_LoosePhotons[0]==0 and (N_LooseElectrons[0]+N_LooseMuons[0])==1\
                        and (N_TightElectrons[0]+N_TightMuons[0])==1 and Jet_Pt[0]>50. and M_W_transverse[0]>=40. and DeltaPhi_AK4Jet_MET[0]>1.5
    if (not isHadronic) and (not isLeptonic):
        continue

    for k in range(N_Jets[0]):
        if isHadronic:
            all_jets_hadronic.Fill(Jet_Pt[k],abs(Jet_Eta[k]),Jet_Flav[k])
        if isLeptonic:
            all_jets_leptonic.Fill(Jet_Pt[k],abs(Jet_Eta[k]),Jet_Flav[k])
    for l in range(N_BTagsL[0]):
        if isHadronic:
            loose_btagged_jets_hadronic.Fill(LooseTaggedJet_Pt[l],abs(LooseTaggedJet_Eta[l]),LooseTaggedJet_Flav[l])
        if isLeptonic:
            loose_btagged_jets_leptonic.Fill(LooseTaggedJet_Pt[l],abs(LooseTaggedJet_Eta[l]),LooseTaggedJet_Flav[l])
    for m in range(N_BTagsM[0]):
        if isHadronic:
            medium_btagged_jets_hadronic.Fill(MediumTaggedJet_Pt[m],abs(MediumTaggedJet_Eta[m]),MediumTaggedJet_Flav[m])
        if isLeptonic:
            medium_btagged_jets_leptonic.Fill(LooseTaggedJet_Pt[l],abs(LooseTaggedJet_Eta[l]),LooseTaggedJet_Flav[l])
   # jets outside of AK15 -> only for hadronic
    if isHadronic:
        for m in range(N_BTagsM_outside[0]):
            medium_btagged_jets_outside_hadronic.Fill(JetMediumTagged_outside_lead_AK15Jet_Pt[m],abs(JetMediumTagged_outside_lead_AK15Jet_Eta[m]),JetMediumTagged_outside_lead_AK15Jet_Flav[m])
        for m in range(N_BTagsL_outside[0]):
            loose_btagged_jets_outside_hadronic.Fill(JetLooseTagged_outside_lead_AK15Jet_Pt[m],abs(JetLooseTagged_outside_lead_AK15Jet_Eta[m]),JetLooseTagged_outside_lead_AK15Jet_Flav[m])
            all_jets_outside_hadronic.Fill(JetLooseTagged_outside_lead_AK15Jet_Pt[m],abs(JetLooseTagged_outside_lead_AK15Jet_Eta[m]),JetLooseTagged_outside_lead_AK15Jet_Flav[m])
        for k in range(N_untagged_loose_outside[0]):
            all_jets_outside_hadronic.Fill(JetLooseUntagged_outside_lead_AK15Jet_Pt[k],abs(JetLooseUntagged_outside_lead_AK15Jet_Eta[k]),JetLooseUntagged_outside_lead_AK15Jet_Flav[k])

#  hadronic efficiencies
loose_btagging_efficiency_hadronic = loose_btagged_jets_hadronic.Clone()
loose_btagging_efficiency_hadronic.SetName("loose_btagging_efficiency_hadronic")
loose_btagging_efficiency_hadronic.SetTitle("loose_btagging_efficiency_hadronic")
loose_btagging_efficiency_hadronic.Divide(all_jets_hadronic)

medium_btagging_efficiency_hadronic = medium_btagged_jets_hadronic.Clone()
medium_btagging_efficiency_hadronic.SetName("medium_btagging_efficiency_hadronic")
medium_btagging_efficiency_hadronic.SetTitle("medium_btagging_efficiency_hadronic")
medium_btagging_efficiency_hadronic.Divide(all_jets_hadronic)

loose_btagging_efficiency_outside_hadronic = loose_btagged_jets_outside_hadronic.Clone()
loose_btagging_efficiency_outside_hadronic.SetName("loose_btagging_efficiency_outside_hadronic")
loose_btagging_efficiency_outside_hadronic.SetTitle("loose_btagging_efficiency_outside_hadronic")
loose_btagging_efficiency_outside_hadronic.Divide(all_jets_outside_hadronic)

medium_btagging_efficiency_outside_hadronic = medium_btagged_jets_outside_hadronic.Clone()
medium_btagging_efficiency_outside_hadronic.SetName("medium_btagging_efficiency_outside_hadronic")
medium_btagging_efficiency_outside_hadronic.SetTitle("medium_btagging_efficiency_outside_hadronic")
medium_btagging_efficiency_outside_hadronic.Divide(all_jets_outside_hadronic)

# leptonic efficiencies
loose_btagging_efficiency_leptonic = loose_btagged_jets_leptonic.Clone()
loose_btagging_efficiency_leptonic.SetName("loose_btagging_efficiency_leptonic")
loose_btagging_efficiency_leptonic.SetTitle("loose_btagging_efficiency_leptonic")
loose_btagging_efficiency_leptonic.Divide(all_jets_leptonic)

medium_btagging_efficiency_leptonic = medium_btagged_jets_leptonic.Clone()
medium_btagging_efficiency_leptonic.SetName("medium_btagging_efficiency_leptonic")
medium_btagging_efficiency_leptonic.SetTitle("medium_btagging_efficiency_leptonic")
medium_btagging_efficiency_leptonic.Divide(all_jets_leptonic)

output_file = ROOT.TFile.Open("btag_efficiencies_"+label+".root","RECREATE")

for hist3D in [
        all_jets_hadronic,
        loose_btagged_jets_hadronic,
        medium_btagged_jets_hadronic,
        loose_btagging_efficiency_hadronic,
        medium_btagging_efficiency_hadronic,

        all_jets_outside_hadronic,
        loose_btagged_jets_outside_hadronic,
        medium_btagged_jets_outside_hadronic,
        loose_btagging_efficiency_outside_hadronic,
        medium_btagging_efficiency_outside_hadronic,

        all_jets_leptonic,
        loose_btagged_jets_leptonic,
        medium_btagged_jets_leptonic,
        loose_btagging_efficiency_leptonic,
        medium_btagging_efficiency_leptonic
    ]:
    hist3D.GetXaxis().SetTitle("p_{T}")
    hist3D.GetYaxis().SetTitle("|#eta|")
    hist3D.GetZaxis().SetTitle("hadron flavor")
    output_file.WriteTObject(hist3D)

output_file.Close()
