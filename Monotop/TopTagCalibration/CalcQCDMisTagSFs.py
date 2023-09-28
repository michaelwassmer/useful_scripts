"""
This script calculates the data/mc scale factors of the QCD-jet mistag fraction for the mono-top analysis.
The qcd mistag fraction is calculated based on the gamma+jets control region, which is very pure in events containing genuine QCD jets.
The input is a ROOT file containing all the necessary templates from the monotop analysis and an optional comma-separated list of systematic uncertainties.

1. ROOT file needs to be read. Histograms need to read and converted to numpy.
2. QCD mistag fractions are calculated for MC and data in the gamma+jets control region as well as corresponding data/mc scale factors.
3. Save the mistag fractions and scale factors in a json.
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


"""
read the necessary histograms, i.e. in gamma+jets CR, and put them into a dictionary
dictionary structure:
    key=name of histogram
    value=Hist object i.e. (edges, values, errors)
"""
hists = ReadTemplates(infile, ["CR_Gamma"], ["G1Jet", "data_obs"], systs)

#########
### 2 ###
#########

# dictionary to contain all the mistag fractions as Hist objects
mfs = {}

# start with data cause it's easy (no systematics)

# data template in gamma+jets CR with a tag
data_gjets_cr_tag = hists["CR_Gamma_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"]
# data template in gamma+jets CR irrespective of tag or not
data_gjets_cr_all = hists["CR_Gamma_AK15Jet_Pt_0_Any__data_obs__nom"]

# calculate qcd mistag fraction in data by just dividing tag/all
# statistical uncertainties are calculated from binomial confidence interval and then symmetrized
mfs["data"] = Hist(
    "mfs_data",
    data_gjets_cr_tag.edges,
    data_gjets_cr_tag.values / data_gjets_cr_all.values,
    GetSymmUncFromUpDown(
        *GetEffStatErrors(data_gjets_cr_tag.values, data_gjets_cr_all.values)
    ),
)

# names of necessary nominal MC templates for QCD mistag fraction
mc_gjets_cr_tag_name = "CR_Gamma_AK15Jet_Pt_0_QCD_Tagged__G1Jet_Ptbinned__nom"
mc_gjets_cr_all_name = "CR_Gamma_AK15Jet_Pt_0_QCD__G1Jet_Ptbinned__nom"

# gamma+jets MC template in gamma+jets CR with a tag
mc_gjets_cr_tag_hist = hists[mc_gjets_cr_tag_name]
# gamma+jets MC template in gamma+jets CR irrespective of tag or not
mc_gjets_cr_all_hist = hists[mc_gjets_cr_all_name]

# qcd mistag fractions in mc
mfs["mc"] = {}

# calculate qcd mistag fraction in nominal (nom, i.e. no systematic variations) MC by just dividing tag/all
# statistical uncertainties are calculated from binomial confidence interval and then symmetrized
mfs["mc"]["nom"] = Hist(
    "mfs_mc_nom",
    mc_gjets_cr_tag_hist.edges,
    mc_gjets_cr_tag_hist.values / mc_gjets_cr_all_hist.values,
    GetSymmUncFromUpDown(
        *GetEffStatErrors(mc_gjets_cr_tag_hist.values, mc_gjets_cr_all_hist.values)
    ),
)

# dictionary to contain all the data/mc scale factors as Hist objects
sfs = {}

# nominal data/mc scale factor
# statistical data uncertainty and statisticam mc uncertainty are added in quadrature to obtain overall uncertainty
sfs["nom"] = Hist(
    "sfs_nom",
    mfs["data"].edges,
    mfs["data"].values / mfs["mc"]["nom"].values,
    np.sqrt(
        np.square(mfs["data"].errors / mfs["mc"]["nom"].values)
        + np.square(
            GetSymmUncFromUpDown(
                mfs["data"].values
                / (mfs["mc"]["nom"].values + mfs["mc"]["nom"].errors),
                mfs["data"].values
                / (mfs["mc"]["nom"].values - mfs["mc"]["nom"].errors),
            )
        )
    ),
)

# repeat the calculations from above for systematic variations of mc
# don't consider stat uncertainties of the systematic variations

# loop over systematics
for syst in systs:
    # loop over the two variations
    for var in ["Up", "Down"]:
        mc_gjets_cr_tag_syst_name = mc_gjets_cr_tag_name.replace("nom", syst + var)
        mc_gjets_cr_all_syst_name = mc_gjets_cr_all_name.replace("nom", syst + var)
        mc_gjets_cr_tag_syst_hist = hists[mc_gjets_cr_tag_syst_name]
        mc_gjets_cr_all_syst_hist = hists[mc_gjets_cr_all_syst_name]
        # calculate the mistag fraction for systematically variated mc
        mfs["mc"][syst + var] = Hist(
            f"mfs_mc_{syst}{var}",
            mc_gjets_cr_tag_syst_hist.edges,
            mc_gjets_cr_tag_syst_hist.values / mc_gjets_cr_all_syst_hist.values,
            np.zeros_like(mc_gjets_cr_tag_syst_hist.values),
        )
        # calculate mistag scale factor for systematically variated mc
        sfs[syst + var] = Hist(
            f"sfs_{syst}{var}",
            mfs["data"].edges,
            mfs["data"].values / mfs["mc"][syst + var].values,
            np.zeros_like(mfs["data"].values),
        )
    # calculate the total error of the nominal mistag fraction by adding the single uncertainties in quadrature
    mfs["mc"]["nom"].errors = np.sqrt(
        np.square(
            GetSymmUncFromUpDown(
                mfs["mc"][syst + "Up"].values, mfs["mc"][syst + "Down"].values
            )
        )
        + np.square(mfs["mc"]["nom"].errors)
    )
    # calculate the total error of the nominal mistag scale factor by adding the single uncertainties in quadrature
    sfs["nom"].errors = np.sqrt(
        np.square(
            GetSymmUncFromUpDown(sfs[syst + "Up"].values, sfs[syst + "Down"].values)
        )
        + np.square(sfs["nom"].errors)
    )

# printout
print(mfs["mc"]["nom"])
print(mfs["data"])
print(sfs["nom"])

#########
### 3 ###
#########

# dump information into json
json_dict = {}

# mistag fraction in mc
json_dict["eff_mc"] = {
    "edges": list(mfs["mc"]["nom"].edges),
    "values": list(mfs["mc"]["nom"].values),
    "uncertainties": list(mfs["mc"]["nom"].errors),
}

# mistag fraction in data
json_dict["eff_data"] = {
    "edges": list(mfs["data"].edges),
    "values": list(mfs["data"].values),
    "uncertainties": list(mfs["data"].errors),
}

# data/mc mistag scale factor
json_dict["sf_data_mc"] = {
    "edges": list(sfs["nom"].edges),
    "values": list(sfs["nom"].values),
    "uncertainties": list(sfs["nom"].errors),
}

# save information in json file
with open("qcd_mistag.json", "w") as outfile:
    json.dump(json_dict, outfile, indent=4)
