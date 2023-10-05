"""
This script calculates the data/mc scale factors of the top-jet tagging efficiency for the mono-top analysis.
The top tag efficiency is calculated based on the two ttbar control regions, which are quite pure in events containing genuine top jets.
The input is a ROOT file containing all the necessary templates from the monotop analysis and an optional comma-separated list of systematic uncertainties.

1. ROOT file needs to be read. Histograms need to read and converted to numpy.
2. Summarize necessary MC backgrounds in one total background template including systematics
3. Top tag efficiencies are calculated for MC and data in the ttbar control regions as well as corresponding data/mc scale factors.
4. Save the top tag efficiencies and scale factors in a json.
"""

# imports
import sys
from Helper import *
import numpy as np
import json
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
if ".root" not in infile:
    raise Exception(
        "Given input file does not seem to be a ROOT file, which typically ends with '.root'",
        f"Given input file was >>> {infile} <<<",
    )

# list of systematic uncertainties to consider
# systematics are given as a comma-separated list
systs = []
if len(sys.argv) == 3:
    systs = sys.argv[2]
    systs = systs.split(",")


# processes to consider as relevant backgrounds
procs = ["ttbar", "SingleTop", "WJetsToLNu_stitched", "diboson", "qcd", "DYJetsToLL"]

"""
read the necessary histograms, i.e. in gamma+jets CR, and put them into a dictionary
dictionary structure:
    key=name of histogram
    value=Hist object i.e. (edges, values, errors)
"""
hists = ReadTemplates(
    infile,
    ["CR_TT_electron", "CR_TT_muon"],
    procs + ["data_obs"],
    systs,
)

# add together electron and muon channels
hists_combined = {}
for label in hists.keys():
    if "CR_TT_muon" in label:
        continue
    new_label = label.replace("CR_TT_electron", "CR_TT_lepton")
    hists_combined[new_label] = hists[label].copy()
    hists_combined[new_label].add(
        hists[label.replace("CR_TT_electron", "CR_TT_muon")], True
    )

hists.update(hists_combined)

# electron or muon or lepton (combination of ele and mu) channel
lep = "lepton"

# edges of the histograms should be similar in all histograms otherwise this method does not work
# therefore just use one histogram to set this variable
edges = np.array(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__nom"].edges)

# qcd mistag scale factors from correctionlib
qcd_mistag_correction = correctionlib.CorrectionSet.from_file("qcd_mistag.json.gz")

# get representative AK15 jet pts to retrieve qcd mistag sfs from correctionlib object
# therefore, just increase the edges of the jet pt histograms by 1 and remove the last entry
rep_jet_pts = (edges + 1.0)[:-1]
# then evalute the correctionlib object to get the qcdmistag sfs
qcd_mistag_sfs = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "nom")
qcd_mistag_sfs_up = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Up")
qcd_mistag_sfs_down = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Down")

#########
### 2 ###
#########

# calculate summed background processes in tag regions as well as independent of tag or not
# start with the nominal MC backgrounds

# create histograms to hold summed background processes
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"] = Hist(
    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom",
    edges,
)
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"] = Hist(
    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom",
    edges,
)

# loop over processes and add them to the summed background histograms
for proc in procs:
    # copies of the nominal histograms for QCDMistag systematics
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__QCDMistagUp"] = hists[
        f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__nom"
    ].copy()
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__QCDMistagDown"] = hists[
        f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__nom"
    ].copy()
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__{proc}__QCDMistagUp"] = hists[
        f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__{proc}__nom"
    ].copy()
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__{proc}__QCDMistagDown"] = hists[
        f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__{proc}__nom"
    ].copy()
    # apply qcd mistag scale factor for qcd jet events in the tag region
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__nom"].apply_sfs(qcd_mistag_sfs)
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"].add(
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__nom"], True
    )
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"].add(
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__{proc}__nom"], True
    )

# do the same but for systematic variations of the MC processes
for syst in systs + ["QCDMistag"]:
    for var in ["Up", "Down"]:
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"] = Hist(
            f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}",
            edges,
        )
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"] = Hist(
            f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}",
            edges,
        )
        for proc in procs:
            if syst + var == "QCDMistagUp":
                hists[
                    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__{syst+var}"
                ].apply_sfs(qcd_mistag_sfs_up)
            elif syst + var == "QCDMistagDown":
                hists[
                    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__{syst+var}"
                ].apply_sfs(qcd_mistag_sfs_down)
            else:
                hists[
                    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__{syst+var}"
                ].apply_sfs(qcd_mistag_sfs)
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"].add(
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__{syst+var}"], False
            )
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"].add(
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__{proc}__{syst+var}"], False
            )
# print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"])
# print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"])

#########
### 3 ###
#########

# dictionary to contain all the tag efficiencies as Hist objects
tes = {}

# start with mc efficiencies

# mc template in ttbar CR with a tag
mc_top_cr_tag_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__nom"
# mc template in ttbar CR irrespective of tag or not
mc_top_cr_all_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top__ttbar__nom"

# ttbar MC template in ttbar CR with a tag
mc_top_cr_tag_hist = hists[mc_top_cr_tag_name]
# ttbar MC template in ttbar CR irrespective of tag or not
mc_top_cr_all_hist = hists[mc_top_cr_all_name]

# top tag efficiency in mc
tes["mc"] = {}
# top tag efficiency in data
tes["data"] = {}

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

# now do the data efficiencies
# this is done by estimating the top jet processes in data by
# subtracting the MC qcd jet processes (summarized in the Bkg templates) from data

# first get copies of data templates
data_top_cr_tag_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"
data_top_cr_all_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"

data_top_cr_tag_hist = hists[data_top_cr_tag_name].copy()
data_top_cr_tag_hist.name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__data_obs__nom"

data_top_cr_all_hist = hists[data_top_cr_all_name].copy()
data_top_cr_all_hist.name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top__data_obs__nom"

# print(data_top_cr_tag_hist)
# print(data_top_cr_all_hist)

# now subtract the summed background templates
data_top_cr_tag_hist.add(
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"], True, -1.0
)
data_top_cr_all_hist.add(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"], True, -1.0)

# print(data_top_cr_tag_hist)
# print(data_top_cr_all_hist)

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

# loop over systematics
for syst in systs + ["QCDMistag"]:
    # loop over the two variations
    for var in ["Up", "Down"]:
        if syst != "QCDMistag":
            mc_top_cr_tag_syst_name = mc_top_cr_tag_name.replace("nom", syst + var)
            mc_top_cr_all_syst_name = mc_top_cr_all_name.replace("nom", syst + var)
            mc_top_cr_tag_syst_hist = hists[mc_top_cr_tag_syst_name]
            mc_top_cr_all_syst_hist = hists[mc_top_cr_all_syst_name]
            # calculate the top tag efficiency for systematically variated mc
            tes["mc"][syst + var] = Hist(
                f"tes_mc_{syst}{var}",
                edges,
                mc_top_cr_tag_syst_hist.values / mc_top_cr_all_syst_hist.values,
                np.zeros_like(mc_top_cr_tag_syst_hist.values),
            )

        # data effiencies analogously to the nominal case but now for systematically variated MC
        data_top_cr_tag_syst_name = data_top_cr_tag_name
        data_top_cr_all_syst_name = data_top_cr_all_name

        data_top_cr_tag_syst_hist = hists[data_top_cr_tag_syst_name].copy()
        data_top_cr_tag_syst_hist.name = (
            f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__data_obs__{syst+var}"
        )
        # print("bla",data_top_cr_tag_syst_hist)
        data_top_cr_all_syst_hist = hists[data_top_cr_all_syst_name].copy()
        data_top_cr_all_syst_hist.name = (
            f"CR_TT_{lep}_AK15Jet_Pt_0_Top__data_obs__{syst+var}"
        )

        data_top_cr_tag_syst_hist.add(
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"], False, -1.0
        )
        data_top_cr_all_syst_hist.add(
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"], False, -1.0
        )

        tes["data"][syst + var] = Hist(
            f"tes_data_{syst+var}",
            edges,
            data_top_cr_tag_syst_hist.values / data_top_cr_all_syst_hist.values,
            np.zeros_like(data_top_cr_tag_syst_hist.values),
        )
        print(tes["data"][syst + var])
        # calculate mistag scale factors for systematically variated mc
        if syst == "QCDMistag":
            sfs[syst + var] = Hist(
                f"sfs_{syst}{var}",
                edges,
                tes["data"][syst + var].values / tes["mc"]["nom"].values,
                np.zeros_like(tes["data"][syst + var].values),
            )
        else:
            sfs[syst + var] = Hist(
                f"sfs_{syst}{var}",
                edges,
                tes["data"][syst + var].values / tes["mc"][syst + var].values,
                np.zeros_like(tes["data"][syst + var].values),
            )
    # calculate the total error of the nominal mistag fraction by adding the single uncertainties in quadrature
    if syst != "QCDMistag":
        tes["mc"]["nom"].errors = np.sqrt(
            np.square(
                GetSymmUncFromUpDown(
                    tes["mc"][syst + "Up"].values, tes["mc"][syst + "Down"].values
                )
            )
            + np.square(tes["mc"]["nom"].errors)
        )
    tes["data"]["nom"].errors = np.sqrt(
        np.square(
            GetSymmUncFromUpDown(
                tes["data"][syst + "Up"].values, tes["data"][syst + "Down"].values
            )
        )
        + np.square(tes["data"]["nom"].errors)
    )
    # calculate the total error of the nominal mistag scale factor by adding the single uncertainties in quadrature
    sfs["nom"].errors = np.sqrt(
        np.square(
            GetSymmUncFromUpDown(sfs[syst + "Up"].values, sfs[syst + "Down"].values)
        )
        + np.square(sfs["nom"].errors)
    )

print(tes["mc"]["nom"])
print(tes["data"]["nom"])
print(sfs["nom"])

#########
### 4 ###
#########

# dump information into json
json_dict = {}

# top tag efficiency in mc
json_dict["eff_mc"] = {
    "edges": list(edges),
    "values": list(tes["mc"]["nom"].values),
    "uncertainties": list(tes["mc"]["nom"].errors),
}

# top tag efficiency in data
json_dict["eff_data"] = {
    "edges": list(edges),
    "values": list(tes["data"]["nom"].values),
    "uncertainties": list(tes["data"]["nom"].errors),
}

# data/mc top tag scale factor
json_dict["sf_data_mc"] = {
    "edges": list(edges),
    "values": list(sfs["nom"].values),
    "uncertainties": list(sfs["nom"].errors),
}

cset = cs.CorrectionSet(
    schema_version=2,
    description="Top tag efficiencies and data/mc scale factors",
    corrections=[
        CreateCorrection(
            "eff_mc",
            list(edges),
            list(tes["mc"]["nom"].values),
            list(tes["mc"]["nom"].values_up()),
            list(tes["mc"]["nom"].values_down()),
        ),
        CreateCorrection(
            "eff_data",
            list(edges),
            list(tes["data"]["nom"].values),
            list(tes["data"]["nom"].values_up()),
            list(tes["data"]["nom"].values_down()),
        ),
        CreateCorrection(
            "sf_data_mc",
            list(edges),
            list(sfs["nom"].values),
            list(sfs["nom"].values_up()),
            list(sfs["nom"].values_down()),
        ),
    ],
)

with gzip.open("top_tag.json.gz", "wt") as fout:
    fout.write(cset.json(exclude_unset=True, indent=4))

# save information in json file
# with open("top_tag.json", "w") as outfile:
#     json.dump(json_dict, outfile, indent=4)
