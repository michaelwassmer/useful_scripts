#!/bin/bash

# input arguments
YEAR=$1

python3 CalcEffs.py eff_data_${YEAR}_dimu_ref_isomu_probe_pfmetnomu templates_data_${YEAR}_dimu_ref_isomu.root templates_data_${YEAR}_dimu_ref_isomu_probe_pfmetnomu.root
python3 CalcEffs.py eff_data_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu templates_data_${YEAR}_singlemu_ref_isomu.root templates_data_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu.root
python3 CalcEffs.py eff_data_${YEAR}_singleele_ref_isoele_probe_pfmetnomu templates_data_${YEAR}_singleele_ref_isoele.root templates_data_${YEAR}_singleele_ref_isoele_probe_pfmetnomu.root

python3 CalcEffs.py eff_mc_dyjets_${YEAR}_dimu_ref_isomu_probe_pfmetnomu templates_mc_dyjets_${YEAR}_dimu_ref_isomu.root templates_mc_dyjets_${YEAR}_dimu_ref_isomu_probe_pfmetnomu.root
python3 CalcEffs.py eff_mc_wjets_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu templates_mc_wjets_${YEAR}_singlemu_ref_isomu.root templates_mc_wjets_${YEAR}_singlemu_ref_isomu_probe_pfmetnomu.root
python3 CalcEffs.py eff_mc_wjets_${YEAR}_singleele_ref_isoele_probe_pfmetnomu templates_mc_wjets_${YEAR}_singleele_ref_isoele.root templates_mc_wjets_${YEAR}_singleele_ref_isoele_probe_pfmetnomu.root
