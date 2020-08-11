processes = {
    "znunujets" : "ZJetsToNuNu*/*nominal*.root",
    "wlnujets"  : "WJetsToLNu*/*nominal*.root",
    "zlljets"   : "DYJetsToLL*/*nominal*.root",
    "gammajets" : "GJets*/*nominal*.root",
    "ttbar"     : "TTTo*/*nominal*.root",
    "singlet"   : "ST_*/*nominal*.root",
    "diboson"   : "{WW*,WZ*,ZZ*}/*nominal*.root",
    "qcd"       : "QCD*/*nominal*.root"
    }
    
general_had_selection = "((Hadr_Recoil_Pt>250.) && (N_AK15Jets>=1) && (Min$(AK15Jet_Pt)>160.) && (Min$(DeltaPhi_AK4Jet_Recoil)>0.8) && (N_Taus==0))"

met_trigger_selection = "((Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_vX == 1) || (Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_vX == 1))"

electron_trigger_selection = "((Triggered_HLT_Ele32_WPTight_Gsf_vX==1) || (Triggered_HLT_Photon200_vX==1) || (Triggered_HLT_Ele115_CaloIdVT_GsfTrkIdT_vX==1))"

no_lepton_photon_selection = "((N_LooseMuons==0) && (N_LooseElectrons==0) && (N_LoosePhotons==0))"

dielectron_selection = "((N_LooseElectrons==2) && (LooseElectron_Pt[0]>40.) && (N_LooseMuons==0) && (N_LoosePhotons==0) && (DiElectron_Mass>60.) && (DiElectron_Mass<120.) && (Evt_Pt_MET<80.))"

dimuon_selection = "((N_LooseMuons==2) && (N_LooseElectrons==0) && (N_LoosePhotons==0) && (DiMuon_Mass>60.) && (DiMuon_Mass<120.) && (Evt_Pt_MET<80.))"

single_electron_selection = "((N_LooseElectrons==1) && (N_TightElectrons==1) && (N_LooseMuons==0) && (N_LoosePhotons==0))"

single_muon_selection = "((N_LooseMuons==1) && (N_TightMuons==1) && (N_LooseElectrons==0) && (N_LoosePhotons==0))"

single_photon_selection = "((N_TightPhotons==1) && (N_LoosePhotons==1) && (N_LooseMuons==0) && (N_LooseElectrons==0))"

regions = {
    "had_SR"         : no_lepton_photon_selection + " && " + met_trigger_selection,
    "had_CR_ZElEl"   : dielectron_selection + " && " + electron_trigger_selection,
    "had_CR_ZMuMu"   : dimuon_selection + " && " + met_trigger_selection,
    "had_CR_WEl"     : single_electron_selection,
    "had_CR_WMu"     : single_muon_selection,
    "had_CR_ttbarEl" : single_electron_selection,
    "had_CR_ttbarMu" : single_muon_selection,
    "had_CR_Gamma"   : single_photon_selection
    }

for region in regions:
    if "had" in region:
        regions[region] = general_had_selection + " && " + regions[region]
    elif "lep" in region:
        regions[region] = general_lep_selection + " && " + regions[region]
    else:
        print("this should not happen")
        exit()

for region in regions:
    print(region,regions[region])
