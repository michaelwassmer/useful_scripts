#!/bin/bash

# input arguments
YEAR=$1

python3 PlotEffs.py --label ${YEAR} --era ${YEAR} --mc_files eff_mc_wjets_${YEAR}_singleele_ref_isoele_probe_pfmetnomu.root,eff_mc_wjets_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu.root,eff_mc_dyjets_${YEAR}_dimu_ref_isomu_probe_pfmetnomu.root --mc_labels="MC SingleEl,MC SingleMu,MC DiMu" --data_files=eff_data_${YEAR}_singleele_ref_isoele_probe_pfmetnomu.root,eff_data_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu.root,eff_data_${YEAR}_dimu_ref_isomu_probe_pfmetnomu.root --data_labels="Data SingleEl,Data SingleMu,Data DiMu" --variables=trig_eff_pt_pfmetnomu_t1,trig_eff_pt_puppimetnomu_t1 --variables_labels="PFMETNoMu (GeV),PuppiMETNoMu (GeV)" --probe_triggers="HLT_PFMETNoMu120_PFMHTNoMu120_IDTight"
