"""
This script calculates the data/mc scale factors of the top-jet tagging efficiency for the mono-top analysis.
The top tag efficiency is calculated based on the two ttbar control regions (ele and muon channel), which are enriched in events containing genuine top jets.
The input is a ROOT file containing all the necessary templates from the monotop analysis and an optional comma-separated list of systematic uncertainties.

Workflow of the script:
1. ROOT file needs to be read. Histograms need to read and converted to numpy.
2. Summarize necessary MC top backgrounds in one total top background template including systematics.
3. Top tag efficiencies are calculated for MC and data in the ttbar control regions as well as corresponding data/mc scale factors.
4. Save the top tag efficiencies and scale factors in a correctionlib json format.
"""

# imports
import sys
from Helper import *
import numpy as np
import correctionlib
import correctionlib.schemav2 as cs
import gzip

#########
### 1 ###
#########

# some basic input checks
if len(sys.argv) < 2:
    raise Exception(
        "Not enough input arguments.",
        "You need at least the input ROOT file containing the histograms.",
    )
elif len(sys.argv) > 3:
    raise Exception(
        "Too many input arguments.",
        "You need either only one input argument, a ROOT file, or optionally a comma-separated list of systematics as second argument.",
    )

# input ROOT file
infile = sys.argv[1]
if not ".root" in infile:
    raise Exception(
        "Given input file does not seem to be a ROOT file, which typically ends with '.root'",
        f"Given input file was >>> {infile} <<<",
    )

# list of systematic uncertainties to consider
# systematics are given as a comma-separated list and are split using the comma
systs = []
if len(sys.argv) == 3:
    systs = sys.argv[2]
    systs = systs.split(",")

# processes to consider as relevant backgrounds
top_procs = ["ttbar", "SingleTop"]

"""
read the necessary histograms, i.e. in ttbar CRs, and put them into a dictionary
dictionary structure:
    key=name of histogram
    value=Hist object i.e. (edges, values, errors)
"""
hists = ReadTemplates(
    infile,
    ["CR_TT_electron", "CR_TT_muon"],
    top_procs + ["data_obs"],
    systs,
)

# add together electron and muon channels for more statistics
hists_combined = {}
for label in hists.keys():
    if "CR_TT_muon" in label:
        continue
    new_label = label.replace("CR_TT_electron", "CR_TT_lepton")
    hists_combined[new_label] = hists[label].copy(new_label)
    hists_combined[new_label].add(
        hists[label.replace("CR_TT_electron", "CR_TT_muon")], True
    )
hists.update(hists_combined)

# electron or muon or lepton (combination of ele and mu) channel
lep = "lepton"

# edges of the histograms are assumed to be similar in all histograms, otherwise this method does not work
# therefore just use one histogram to set the edges
edges = np.array(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__nom"].edges)

# load qcd mistag scale factors from correctionlib
qcd_mistag_correction = correctionlib.CorrectionSet.from_file("qcd_mistag.json.gz")

# get representative AK15 jet pts to retrieve qcd mistag sfs from correctionlib object
# therefore, just increase the edges of the jet pt histograms by 1 and remove the last entry
rep_jet_pts = (edges + 1.0)[:-1]
# then evalute the correctionlib object to get the qcdmistag sfs
qcd_mistag_sfs = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Nom")
qcd_mistag_sfs_up = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Up")
qcd_mistag_sfs_down = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Down")
# also need qcd mistag fractions in data
qcd_mistag_effs = qcd_mistag_correction["eff_data"].evaluate(rep_jet_pts, "Nom")
qcd_mistag_effs_up = qcd_mistag_correction["eff_data"].evaluate(rep_jet_pts, "Up")
qcd_mistag_effs_down = qcd_mistag_correction["eff_data"].evaluate(rep_jet_pts, "Down")

#########
### 2 ###
#########

# calculate summed top processes in tag regions as well as independent of tag or not
# start with the nominal MC backgrounds

# create histogram to hold summed top background processes in (tagged or not tagged) region
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"] = Hist(
    f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom",
    edges,
)
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"] = Hist(
    f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom",
    edges,
)
# add top processes together
for proc in top_procs:
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"].add(
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__{proc}__nom"], True
    )
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"].add(
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__nom"], True
    )

# print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"])

# repeat for systematics
for syst in systs + ["QCDMistag"]:
    for var in ["Up", "Down"]:
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"] = Hist(
            f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}",
            edges,
        )
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"] = Hist(
            f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}",
            edges,
        )
        for proc in top_procs:
            if syst == "QCDMistag":
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].add(
                    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__{proc}__nom"], False
                )
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"].add(
                    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__nom"], False
                )
            else:
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].add(
                    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__{proc}__{syst+var}"], False
                )
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"].add(
                    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__{syst+var}"],
                    False,
                )

# calculate non-top-jet backgrounds in all region by subtracting the top-jet backgrounds from the data in the all region
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"] = hists[
    f"CR_TT_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"
].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom")
# print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"])
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"].add(
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"], True, -1.0
)
# print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__NoTopBkg__nom"])

# repeat for systematics
for syst in systs + ["QCDMistag"]:
    for var in ["Up", "Down"]:
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"] = hists[
            f"CR_TT_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"
        ].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}")
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"].add(
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"], False, -1.0
        )

# calculate top jet background in tag region by extrapolating non-top backgrounds into tag region via qcd mistag fractions in data
# and then subtracting this extrapolation from data in the tag region
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data"] = hists[
    f"CR_TT_{lep}_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"
].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data")
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"] = hists[
    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"
].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom")
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"].apply_sfs(qcd_mistag_effs)
# print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"])
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data"].add(
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"], True, -1.0
)
print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"])
print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data"])

# repeat for systematics
for syst in systs + ["QCDMistag"]:
    for var in ["Up", "Down"]:
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}_Data"] = hists[
            f"CR_TT_{lep}_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"
        ].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}_Data")
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"] = hists[
            f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"
        ].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}")
        if syst + var == "QCDMistagUp":
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"].apply_sfs(
                qcd_mistag_effs_up
            )
        elif syst + var == "QCDMistagDown":
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"].apply_sfs(
                qcd_mistag_effs_down
            )
        else:
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"].apply_sfs(
                qcd_mistag_effs
            )
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}_Data"].add(
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"],
            False,
            -1.0,
        )
        print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"])
        print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}_Data"])

#########
### 3 ###
#########

# dictionary to contain all the tag efficiencies as Hist objects
tes = {}

# start with mc efficiencies

# mc template in ttbar CR with a tag
mc_top_cr_tag_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"
# mc template in ttbar CR irrespective of tag or not
mc_top_cr_all_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"

# ttbar MC template in ttbar CR with a tag
mc_top_cr_tag_hist = hists[mc_top_cr_tag_name]
# ttbar MC template in ttbar CR irrespective of tag or not
mc_top_cr_all_hist = hists[mc_top_cr_all_name]

# top tag efficiency in mc
tes["mc"] = {}

# calculate top tag efficiency in nominal (nom, i.e. no systematic variations) MC by just dividing tag/all
# statistical uncertainties are calculated as crude max uncertainty estimation from template errors
tes["mc"]["nom"] = Hist(
    "tes_mc_nom",
    edges,
    mc_top_cr_tag_hist.values / mc_top_cr_all_hist.values,
    GetSymmUncFromUpDown(
        mc_top_cr_tag_hist.values_up() / mc_top_cr_all_hist.values_down(),
        mc_top_cr_tag_hist.values_down() / mc_top_cr_all_hist.values_up(),
    ),
)

print(tes["mc"]["nom"])

# now do the data efficiencies
# this is done by estimating the top jet processes in data by
# subtracting the MC qcd jet processes (summarized in the Bkg templates) from data

# first get copies of data templates
data_top_cr_tag_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data"
data_top_cr_all_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"

data_top_cr_tag_hist = hists[data_top_cr_tag_name]

data_top_cr_all_hist = hists[data_top_cr_all_name]

# print(data_top_cr_tag_hist)
# print(data_top_cr_all_hist)

# print(data_top_cr_tag_hist)
# print(data_top_cr_all_hist)

# top tag efficiency in data
tes["data"] = {}

# nominal data efficiency
tes["data"]["nom"] = Hist(
    "tes_data_nom",
    edges,
    data_top_cr_tag_hist.values / data_top_cr_all_hist.values,
    GetSymmUncFromUpDown(
        data_top_cr_tag_hist.values_up() / data_top_cr_all_hist.values_down(),
        data_top_cr_tag_hist.values_down() / data_top_cr_all_hist.values_up(),
    ),
)

print(tes["data"]["nom"])

# nominal scale factor
sfs = {}
sfs["nom"] = Hist(
    "sfs_nom",
    edges,
    tes["data"]["nom"].values / tes["mc"]["nom"].values,
    np.sqrt(
        np.square(tes["data"]["nom"].errors / tes["mc"]["nom"].values)
        + np.square(
            GetSymmUncFromUpDown(
                tes["data"]["nom"].values / tes["mc"]["nom"].values_up(),
                tes["data"]["nom"].values / tes["mc"]["nom"].values_down(),
            )
        )
    ),
)

print(sfs["nom"])
