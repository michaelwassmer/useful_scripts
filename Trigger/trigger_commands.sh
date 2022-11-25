#!/bin/bash

# input arguments
YEAR=$1

if [[ ${YEAR} =~ "2018" ]]
then
    REF_TRIG_ELE=(HLT_Ele32_WPTight_Gsf==1)
    REF_TRIG_MU=(HLT_IsoMu24==1)
    REF_TRIG_HAD=(HLT_PFHT180==1)
    PROBE_TRIG="(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1)"
    ELE_DATASET_LABEL=EGamma
elif [[ ${YEAR} =~ "2017" ]]
then
    REF_TRIG_ELE=(HLT_Ele35_WPTight_Gsf==1)
    REF_TRIG_MU=(HLT_IsoMu27==1)
    REF_TRIG_HAD=(HLT_PFHT180==1)
    PROBE_TRIG="(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1)"
    ELE_DATASET_LABEL=SingleElectron
    #if [ ${YEAR} = "2017B" ]
    #then
    #    PROBE_TRIG="(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1)"
    #fi
elif [[ ${YEAR} =~ "2016postVFP" ]]
then
    REF_TRIG_ELE=(HLT_Ele27_WPTight_Gsf==1)
    REF_TRIG_MU="(HLT_IsoMu24==1 || HLT_IsoTkMu24==1)"
    REF_TRIG_HAD=(HLT_PFHT125==1)
    PROBE_TRIG="(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1)"
    ELE_DATASET_LABEL=SingleElectron
    #if [ ${YEAR} = "2016postVFPH" ]
    #then
    #    PROBE_TRIG="(HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1)"
    #fi
elif [[ ${YEAR} =~ "2016preVFP" ]]
then
    REF_TRIG_ELE=(HLT_Ele27_WPTight_Gsf==1)
    REF_TRIG_MU="(HLT_IsoMu24==1 || HLT_IsoTkMu24==1)"
    REF_TRIG_HAD=(HLT_PFHT125==1)
    PROBE_TRIG="(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1)"
    ELE_DATASET_LABEL=SingleElectron
else
    echo "Given era ${YEAR} not recognized!"
    echo "Exiting ..."
    exit -1
fi

### MC ###

# pfmetnomu triggers in single ele regions

# reference
python3 ../CreateTemplates.py -n templates_mc_wjets_${YEAR}_singleele_ref_isoele -t METAnalyzer/MET_tree -j 4 -S "(n_loose_electrons==1 && n_tight_electrons==1 && n_loose_muons==0) && ${REF_TRIG_ELE}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
# reference+probe
python3 ../CreateTemplates.py -n templates_mc_wjets_${YEAR}_singleele_ref_isoele_probe_pfmetnomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_electrons==1 && n_tight_electrons==1 && n_loose_muons==0) && ${REF_TRIG_ELE} && ${PROBE_TRIG}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root

# pfmetnomu triggers in single mu regions

# reference
python3 ../CreateTemplates.py -n templates_mc_wjets_${YEAR}_singlemu_ref_isomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_muons==1 && n_tight_muons==1 && n_loose_electrons==0) && ${REF_TRIG_MU}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
# reference+probe
python3 ../CreateTemplates.py -n templates_mc_wjets_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_muons==1 && n_tight_muons==1 && n_loose_electrons==0) && ${REF_TRIG_MU} && ${PROBE_TRIG}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root

# pfmetnomu triggers in di mu regions

# reference
python3 ../CreateTemplates.py -n templates_mc_dyjets_${YEAR}_dimu_ref_isomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_muons==2 && n_tight_muons==2 && n_loose_electrons==0) && ${REF_TRIG_MU}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
# reference+probe
python3 ../CreateTemplates.py -n templates_mc_dyjets_${YEAR}_dimu_ref_isomu_probe_pfmetnomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_muons==2 && n_tight_muons==2 && n_loose_electrons==0) && ${REF_TRIG_MU} && ${PROBE_TRIG}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root

# pfmetnomu triggers in all hadronic regions

# reference
#python3 ../CreateTemplates.py -n templates_mc_zjets_${YEAR}_hadr_ref_jetht -t METAnalyzer/MET_tree -j 4 -c "dphis:=return ROOT::VecOps::Map(p4_jets,[phi_pfmetnomu_t1](ROOT::Math::XYZTVector vec){return abs(TVector2::Phi_mpi_pi(vec.phi()-phi_pfmetnomu_t1));})" -S "(n_loose_muons==0 && n_tight_muons==0 && n_loose_electrons==0) && (Min(dphis)>0.5) && ${REF_TRIG_HAD}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}/ZJetsToNuNu_HT-*To*_TuneCP5_13TeV-madgraphMLM-pythia8/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
#&& Min(dphis)>0.5 && abs(TVector2::Phi_mpi_pi(p4_jets[0].phi()-phi_pfmetnomu_t1))>1.5
# reference+probe
#python3 ../CreateTemplates.py -n templates_mc_zjets_${YEAR}_hadr_ref_jetht_probe_pfmetnomu -t METAnalyzer/MET_tree -j 4 -c "dphis:=return ROOT::VecOps::Map(p4_jets,[phi_pfmetnomu_t1](ROOT::Math::XYZTVector vec){return abs(TVector2::Phi_mpi_pi(vec.phi()-phi_pfmetnomu_t1));})" -S "(n_loose_muons==0 && n_tight_muons==0 && n_loose_electrons==0) && (Min(dphis)>0.5) && ${REF_TRIG_HAD} && ${PROBE_TRIG}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}/ZJetsToNuNu_HT-*To*_TuneCP5_13TeV-madgraphMLM-pythia8/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
#&& Min(dphis)>0.5 && abs(TVector2::Phi_mpi_pi(p4_jets[0].phi()-phi_pfmetnomu_t1))>1.5

### DATA ###

# pfmetnomu triggers in single ele regions

# reference
python3 ../CreateTemplates.py -n templates_data_${YEAR}_singleele_ref_isoele -t METAnalyzer/MET_tree -j 4 -S "(n_loose_electrons==1 && n_tight_electrons==1 && n_loose_muons==0) && ${REF_TRIG_ELE}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}*/${ELE_DATASET_LABEL}/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
# reference+probe
python3 ../CreateTemplates.py -n templates_data_${YEAR}_singleele_ref_isoele_probe_pfmetnomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_electrons==1 && n_tight_electrons==1 && n_loose_muons==0) && ${REF_TRIG_ELE} && ${PROBE_TRIG}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}*/${ELE_DATASET_LABEL}/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root

# pfmetnomu triggers in single mu regions

# reference
python3 ../CreateTemplates.py -n templates_data_${YEAR}_singlemu_ref_isomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_muons==1 && n_tight_muons==1 && n_loose_electrons==0) && ${REF_TRIG_MU}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}*/SingleMuon/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
# reference+probe
python3 ../CreateTemplates.py -n templates_data_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_muons==1 && n_tight_muons==1 && n_loose_electrons==0) && ${REF_TRIG_MU} && ${PROBE_TRIG}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}*/SingleMuon/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root

# pfmetnomu triggers in di mu regions

# reference
python3 ../CreateTemplates.py -n templates_data_${YEAR}_dimu_ref_isomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_muons==2 && n_tight_muons==2 && n_loose_electrons==0) && ${REF_TRIG_MU}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}*/SingleMuon/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root 
# reference+probe
python3 ../CreateTemplates.py -n templates_data_${YEAR}_dimu_ref_isomu_probe_pfmetnomu -t METAnalyzer/MET_tree -j 4 -S "(n_loose_muons==2 && n_tight_muons==2 && n_loose_electrons==0) && ${REF_TRIG_MU} && ${PROBE_TRIG}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}*/SingleMuon/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root 

# pfmetnomu triggers in all hadronic regions

# reference
#python3 ../CreateTemplates.py -n templates_data_${YEAR}_hadr_ref_jetht -t METAnalyzer/MET_tree -j 4 -c "dphis:=return ROOT::VecOps::Map(p4_jets,[phi_pfmetnomu_t1](ROOT::Math::XYZTVector vec){return abs(TVector2::Phi_mpi_pi(vec.phi()-phi_pfmetnomu_t1));})" -S "(n_loose_muons==0 && n_tight_muons==0 && n_loose_electrons==0) && (Min(dphis)>0.5) && ${REF_TRIG_HAD}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}*/JetHT/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
#&& Min(dphis)>0.5 && abs(TVector2::Phi_mpi_pi(p4_jets[0].phi()-phi_pfmetnomu_t1))>1.5
# reference+probe
#python3 ../CreateTemplates.py -n templates_data_${YEAR}_hadr_ref_jetht_probe_pfmetnomu -t METAnalyzer/MET_tree -j 4 -c "dphis:=return ROOT::VecOps::Map(p4_jets,[phi_pfmetnomu_t1](ROOT::Math::XYZTVector vec){return abs(TVector2::Phi_mpi_pi(vec.phi()-phi_pfmetnomu_t1));})" -S "(n_loose_muons==0 && n_tight_muons==0 && n_loose_electrons==0) && (Min(dphis)>0.5) && ${REF_TRIG_HAD} && ${PROBE_TRIG}" -1 "pt_pfmetnomu_raw;25;0;500,pt_pfmetnomu_t1;25;0;500,pt_pfmetnomu_t1xy;25;0;500,pt_puppimetnomu_raw;25;0;500,pt_puppimetnomu_t1;25;0;500,pt_puppimetnomu_t1xy;25;0;500,pt_pfmet_raw;25;0;500,pt_pfmet_t1;25;0;500,pt_pfmet_t1xy;25;0;500,pt_puppimet_raw;25;0;500,pt_puppimet_t1;25;0;500,pt_puppimet_t1xy;25;0;500" /pnfs/desy.de/cms/tier2/store/user/mwassmer/RecoMET/MET_Trigger_Studies/${YEAR}*/JetHT/MET_Trigger_Studies_211122/*/000*/MET_ntuples_*.root
#&& Min(dphis)>0.5 && abs(TVector2::Phi_mpi_pi(p4_jets[0].phi()-phi_pfmetnomu_t1))>1.5


#python3 PlotEffs.py --mc_files eff_mc_wjets_${YEAR}_singleele_ref_isoele_probe_pfmetnomu.root,eff_mc_wjets_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu.root,eff_mc_dyjets_${YEAR}_dimu_ref_isomu_probe_pfmetnomu.root,eff_mc_zjets_${YEAR}_hadr_ref_jetht_probe_pfmetnomu.root --mc_labels="MC SingleEl,MC SingleMu,MC DiMu, MC Had" --data_files=eff_data_${YEAR}_singleele_ref_isoele_probe_pfmetnomu.root,eff_data_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu.root,eff_data_${YEAR}_dimu_ref_isomu_probe_pfmetnomu.root,eff_data_${YEAR}_hadr_ref_jetht_probe_pfmetnomu.root --data_labels="Data SingleEl,Data SingleMu,Data DiMu,Data Had" --variables=trig_eff_pt_pfmetnomu_t1,trig_eff_pt_puppimetnomu_t1 --variables_labels="PFMETNoMu (GeV),PuppiMETNoMu (GeV)" --probe_triggers="HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 or HLT_PFMETNoMu120_PFMHTNoMu120_IDTight"
