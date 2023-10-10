#!/bin/bash

INFILE=$1
YEAR=$2

# QCD mistag effs and sfs
python3 CalcQCDMisTagSFs.py $INFILE \
                            unclustEn_$YEAR,pileup_$YEAR,prefire_$YEAR,btagL_$YEAR,mistagL_$YEAR,btag_correlated,mistag_correlated,jesAbsolute,jesAbsolute_$YEAR,jesBBEC1,jesBBEC1_$YEAR,jesEC2,jesEC2_$YEAR,jesFlavorQCD,jesHF,jesHF_$YEAR,jesRelativeBal,jesRelativeSample_$YEAR,jer_0_$YEAR,jer_1_$YEAR,jer_2_$YEAR,jer_3_$YEAR,jer_4_$YEAR,jer_5_$YEAR,photonID_$YEAR,factScale_gammajets,renScale_gammajets,isr,fsr,TH_vjets_EW1,TH_vjets_EW2_aj,TH_vjets_EW3_aj

# Top tag effs and sfs
python3 CalcTopTagSFs.py $INFILE \
                         unclustEn_$YEAR,pileup_$YEAR,prefire_$YEAR,btagL_$YEAR,mistagL_$YEAR,btag_correlated,mistag_correlated,jesAbsolute,jesAbsolute_$YEAR,jesBBEC1,jesBBEC1_$YEAR,jesEC2,jesEC2_$YEAR,jesFlavorQCD,jesHF,jesHF_$YEAR,jesRelativeBal,jesRelativeSample_$YEAR,jer_0_$YEAR,jer_1_$YEAR,jer_2_$YEAR,jer_3_$YEAR,jer_4_$YEAR,jer_5_$YEAR,muonIso_$YEAR,muonID_$YEAR,metTrigger_$YEAR,electronReco_$YEAR,electronID_$YEAR,electronTrigger_$YEAR,TopPt_reweighting,renScale_tt,factScale_tt,renScale_wjets,factScale_wjets,renScale_ST,factScale_ST,isr,fsr,TH_vjets_EW1,TH_vjets_EW2_evj,TH_vjets_EW3_evj
