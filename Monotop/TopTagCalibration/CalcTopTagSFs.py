"""
This script calculates the data/mc scale factors of the top-jet tagging efficiency for the mono-top analysis.
The top tag efficiency is calculated based on the two ttbar control regions, which are quite pure in events containing genuine top jets.
The input is a ROOT file containing all the necessary templates from the monotop analysis and an optional comma-separated list of systematic uncertainties.

1. ROOT file needs to be read. Histograms need to read and converted to numpy.
2. Top tag efficiencies are calculated for MC and data in the ttbar control regions as well as corresponding data/mc scale factors.
3. Save the top tag efficiencies and scale factors in a json.
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

lep = "electron"

qcd_mistag_sfs = [2.40, 1.97, 2.16, 2.05]

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

# dictionary to contain all the tag efficiencies as Hist objects
tes = {}

# start with mc

# mc template in ttbar CR with a tag
mc_top_cr_tag_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__nom"
# mc template in ttbar CR irrespective of tag or not
mc_top_cr_all_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top__ttbar__nom"

# ttbar MC template in ttbar CR with a tag
mc_top_cr_tag_hist = hists[mc_top_cr_tag_name]
# ttbar MC template in ttbar CR irrespective of tag or not
mc_top_cr_all_hist = hists[mc_top_cr_all_name]
# mc_top_cr_tag_hist.add(
#     hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__SingleTop__nom"], 1, True
# )
# mc_top_cr_all_hist.add(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__SingleTop__nom"], 1, True)

# top tag efficiency in mc
tes["mc"] = {}
tes["data"] = {}

# calculate top tag efficiency in nominal (nom, i.e. no systematic variations) MC by just dividing tag/all
# statistical uncertainties are calculated from binomial confidence interval and then symmetrized
tes["mc"]["nom"] = Hist(
    "tes_mc_nom",
    mc_top_cr_tag_hist.edges,
    mc_top_cr_tag_hist.values / mc_top_cr_all_hist.values,
    GetSymmUncFromUpDown(
        mc_top_cr_tag_hist.values_up() / mc_top_cr_all_hist.values_down(),
        mc_top_cr_tag_hist.values_down() / mc_top_cr_all_hist.values_up(),
    ),
)

data_top_cr_tag_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"
data_top_cr_all_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"

data_top_cr_tag_hist = hists[data_top_cr_tag_name].copy()
data_top_cr_tag_hist.name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__data_obs__nom"
# print("bla1",data_top_cr_tag_hist)
data_top_cr_all_hist = hists[data_top_cr_all_name].copy()
data_top_cr_all_hist.name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top__data_obs__nom"

for proc in procs:
    proc_sub_tag_name = data_top_cr_tag_name.replace("Any", "QCD").replace(
        "data_obs", proc
    )
    proc_sub_all_name = data_top_cr_all_name.replace("Any", "QCD").replace(
        "data_obs", proc
    )
    proc_sub_tag_hist = hists[proc_sub_tag_name].copy()
    proc_sub_all_hist = hists[proc_sub_all_name].copy()
    proc_sub_tag_hist.apply_sfs(qcd_mistag_sfs)
    data_top_cr_tag_hist.add(proc_sub_tag_hist, -1.0, True)
    data_top_cr_all_hist.add(proc_sub_all_hist, -1.0, True)

tes["data"]["nom"] = Hist(
    "tes_data_nom",
    data_top_cr_tag_hist.edges,
    data_top_cr_tag_hist.values / data_top_cr_all_hist.values,
    GetSymmUncFromUpDown(
        data_top_cr_tag_hist.values_up() / data_top_cr_all_hist.values_down(),
        data_top_cr_tag_hist.values_down() / data_top_cr_all_hist.values_up(),
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
        for proc in procs:
            # print(data_top_cr_tag_syst_hist)
            proc_sub_tag_name = (
                data_top_cr_tag_syst_name.replace("Any", "QCD")
                .replace("data_obs", proc)
                .replace("nom", syst + var)
            )
            proc_sub_all_name = (
                data_top_cr_all_syst_name.replace("Any", "QCD")
                .replace("data_obs", proc)
                .replace("nom", syst + var)
            )
            proc_sub_tag_hist = hists[proc_sub_tag_name].copy()
            proc_sub_all_hist = hists[proc_sub_all_name].copy()
            proc_sub_tag_hist.apply_sfs(qcd_mistag_sfs)
            data_top_cr_tag_syst_hist.add(proc_sub_tag_hist, -1.0, False)
            data_top_cr_all_syst_hist.add(proc_sub_all_hist, -1.0, False)

        tes["data"][syst + var] = Hist(
            f"tes_data_{syst+var}",
            data_top_cr_tag_syst_hist.edges,
            data_top_cr_tag_syst_hist.values / data_top_cr_all_syst_hist.values,
            np.zeros_like(data_top_cr_tag_syst_hist.values),
        )
        print(tes["data"][syst + var])
        # # calculate mistag scale factor for systematically variated mc
        # sfs[syst + var] = Hist(
        #     f"sfs_{syst}{var}",
        #     mfs["data"].edges,
        #     mfs["data"].values / mfs["mc"][syst + var].values,
        #     np.zeros_like(mfs["data"].values),
        # )
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
    # sfs["nom"].errors = np.sqrt(
    #     np.square(
    #         GetSymmUncFromUpDown(sfs[syst + "Up"].values, sfs[syst + "Down"].values)
    #     )
    #     + np.square(sfs["nom"].errors)
    # )

print(tes["mc"]["nom"])
print(tes["data"]["nom"])
