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

# electron or muon channel to use
lep = "electron"

# qcd mistag scale factors for now
# still needs to be exchanged to actually read from json file
qcd_mistag_sfs = [2.40, 1.97, 2.16, 2.05]

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
    [f"CR_TT_{lep}"],
    procs + ["data_obs"],
    systs,
)

#########
### 2 ###
#########

# calculate summed background processes in tag regions as well as independent of tag or not
# start with the nominal MC backgrounds

# create histograms to hold summed background processes
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"] = Hist(
    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom",
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__nom"].edges,
)
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"] = Hist(
    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom",
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__nom"].edges,
)

# loop over processes and add them to the summed background histograms
for proc in procs:
    # apply qcd mistag scale factor for qcd jet events in the tag region
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__nom"].apply_sfs(qcd_mistag_sfs)
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"].add(
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__nom"], True
    )
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"].add(
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__{proc}__nom"], True
    )

# do the same but for systematic variations of the MC processes
for syst in systs:
    for var in ["Up", "Down"]:
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"] = Hist(
            f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}",
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__{syst+var}"].edges,
        )
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"] = Hist(
            f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}",
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__{syst+var}"].edges,
        )
        for proc in procs:
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__{syst+var}"].apply_sfs(
                qcd_mistag_sfs
            )
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"].add(
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__{proc}__{syst+var}"], False
            )
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"].add(
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__{proc}__{syst+var}"], False
            )
        # print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"])
        # print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"])

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
    mc_top_cr_tag_hist.edges,
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

# now subtract the summed background templates
data_top_cr_tag_hist.add(
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"], True, -1.0
)
data_top_cr_all_hist.add(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"], True, -1.0)

# nominal data efficiency
tes["data"]["nom"] = Hist(
    "tes_data_nom",
    data_top_cr_tag_hist.edges,
    data_top_cr_tag_hist.values / data_top_cr_all_hist.values,
    GetSymmUncFromUpDown(
        data_top_cr_tag_hist.values_up() / data_top_cr_all_hist.values_down(),
        data_top_cr_tag_hist.values_down() / data_top_cr_all_hist.values_up(),
    ),
)

sfs = {}
sfs["nom"] = Hist(
    "sfs_nom",
    tes["data"]["nom"].edges,
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
for syst in systs:
    # loop over the two variations
    for var in ["Up", "Down"]:
        mc_top_cr_tag_syst_name = mc_top_cr_tag_name.replace("nom", syst + var)
        mc_top_cr_all_syst_name = mc_top_cr_all_name.replace("nom", syst + var)
        mc_top_cr_tag_syst_hist = hists[mc_top_cr_tag_syst_name]
        mc_top_cr_all_syst_hist = hists[mc_top_cr_all_syst_name]
        # calculate the top tag efficiency for systematically variated mc
        tes["mc"][syst + var] = Hist(
            f"tes_mc_{syst}{var}",
            mc_top_cr_tag_syst_hist.edges,
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
            data_top_cr_tag_syst_hist.edges,
            data_top_cr_tag_syst_hist.values / data_top_cr_all_syst_hist.values,
            np.zeros_like(data_top_cr_tag_syst_hist.values),
        )
        print(tes["data"][syst + var])
        # calculate mistag scale factors for systematically variated mc
        sfs[syst + var] = Hist(
            f"sfs_{syst}{var}",
            tes["data"][syst + var].edges,
            tes["data"][syst + var].values / tes["mc"][syst + var].values,
            np.zeros_like(tes["data"][syst + var].values),
        )
    # calculate the total error of the nominal mistag fraction by adding the single uncertainties in quadrature
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
    "edges": list(tes["mc"]["nom"].edges),
    "values": list(tes["mc"]["nom"].values),
    "uncertainties": list(tes["mc"]["nom"].errors),
}

# top tag efficiency in data
json_dict["eff_data"] = {
    "edges": list(tes["data"]["nom"].edges),
    "values": list(tes["data"]["nom"].values),
    "uncertainties": list(tes["data"]["nom"].errors),
}

# data/mc top tag scale factor
json_dict["sf_data_mc"] = {
    "edges": list(sfs["nom"].edges),
    "values": list(sfs["nom"].values),
    "uncertainties": list(sfs["nom"].errors),
}

# save information in json file
with open("top_tag.json", "w") as outfile:
    json.dump(json_dict, outfile, indent=4)
