"""
This script calculates the data/mc scale factors of the QCD-jet (no b-flavor) mistag fraction for the mono-top analysis.
The qcd mistag fraction is calculated based on the gamma+jets control region, which is very pure in events containing genuine QCD jets.
A small contamination of b-flavor jet events is considered by subtracting those events based on their MC prediction combined with a very conservative uncertainty on those events.
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


"""
read the necessary histograms, i.e. in gamma+jets CR, and put them into a dictionary
dictionary structure:
    key=name of histogram
    value=Hist object i.e. (edges, values, errors)
"""
hists = ReadTemplates(
    infile, ["AK15Jet_Pt_0"], ["CR_Gamma"], ["G1Jet", "data_obs"], systs
)

#########
### 2 ###
#########

# dictionary to contain all the mistag fractions as Hist objects
mfs = {}

# start with data

# data template in gamma+jets CR with a tag
data_gjets_qcd_cr_tag = hists["CR_Gamma_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"].copy(
    "CR_Gamma_AK15Jet_Pt_0_QCD_Tagged__data_obs__nom"
)
# data template in gamma+jets CR irrespective of tag or not
data_gjets_qcd_cr_all = hists["CR_Gamma_AK15Jet_Pt_0_Any__data_obs__nom"].copy(
    "CR_Gamma_AK15Jet_Pt_0_QCD__data_obs__nom"
)

# names of necessary nominal MC templates for QCD mistag fraction
# qcd-jet events
mc_gjets_qcd_cr_tag_name = "CR_Gamma_AK15Jet_Pt_0_QCD_Tagged__G1Jet_Ptbinned__nom"
mc_gjets_qcd_cr_all_name = "CR_Gamma_AK15Jet_Pt_0_QCD__G1Jet_Ptbinned__nom"
# b-jet events (contamination)
mc_gjets_b_cr_tag_name = "CR_Gamma_AK15Jet_Pt_0_B_Tagged__G1Jet_Ptbinned__nom"
mc_gjets_b_cr_all_name = "CR_Gamma_AK15Jet_Pt_0_B__G1Jet_Ptbinned__nom"

# gamma+jets qcd-jet MC template in gamma+jets CR with a tag
mc_gjets_qcd_cr_tag_hist = hists[mc_gjets_qcd_cr_tag_name]
# gamma+jets qcd-jet MC template in gamma+jets CR irrespective of tag or not
mc_gjets_qcd_cr_all_hist = hists[mc_gjets_qcd_cr_all_name]
# gamma+jets b-jet MC template in gamma+jets CR with a tag
mc_gjets_b_cr_tag_hist = hists[mc_gjets_b_cr_tag_name]
# gamma+jets b-jet MC template in gamma+jets CR irrespective of tag or not
mc_gjets_b_cr_all_hist = hists[mc_gjets_b_cr_all_name]

# subtract b-jet contaminations from data in both regions
data_gjets_qcd_cr_tag.add(mc_gjets_b_cr_tag_hist, True, -1)
data_gjets_qcd_cr_all.add(mc_gjets_b_cr_all_hist, True, -1)

# calculate qcd mistag fraction in data by just dividing tag/all
# statistical uncertainties are calculated from binomial confidence interval and then symmetrized
mfs["data"] = {}
mfs["data"]["nom"] = Hist(
    "mfs_data_nom",
    data_gjets_qcd_cr_tag.edges,
    data_gjets_qcd_cr_tag.values / data_gjets_qcd_cr_all.values,
    GetSymmUncFromUpDown(
        *GetEffStatErrors(data_gjets_qcd_cr_tag.values, data_gjets_qcd_cr_all.values)
    ),
)

# qcd mistag fractions in mc
mfs["mc"] = {}

# calculate qcd mistag fraction in nominal (nom, i.e. no systematic variations) MC by just dividing tag/all
# statistical uncertainties are calculated as crude max uncertainty estimation from template errors
mfs["mc"]["nom"] = Hist(
    "mfs_mc_nom",
    mc_gjets_qcd_cr_tag_hist.edges,
    mc_gjets_qcd_cr_tag_hist.values / mc_gjets_qcd_cr_all_hist.values,
    GetSymmUncFromUpDown(
        mc_gjets_qcd_cr_tag_hist.values_up() / mc_gjets_qcd_cr_all_hist.values_down(),
        mc_gjets_qcd_cr_tag_hist.values_down() / mc_gjets_qcd_cr_all_hist.values_up(),
    ),
)

# dictionary to contain all the data/mc scale factors as Hist objects
sfs = {}

# nominal data/mc scale factor
# statistical data uncertainty and statistical mc uncertainty are added in quadrature to obtain overall uncertainty
sfs["nom"] = Hist(
    "sfs_nom",
    mfs["data"]["nom"].edges,
    mfs["data"]["nom"].values / mfs["mc"]["nom"].values,
    np.sqrt(
        np.square(mfs["data"]["nom"].errors / mfs["mc"]["nom"].values)
        + np.square(
            GetSymmUncFromUpDown(
                mfs["data"]["nom"].values / mfs["mc"]["nom"].values_up(),
                mfs["data"]["nom"].values / mfs["mc"]["nom"].values_down(),
            )
        )
    ),
)

# repeat the calculations from above for systematic variations of mc
# don't consider stat uncertainties of the systematic variations

# loop over systematics
for syst in systs + ["BJetMistag", "BJetNorm"]:
    # loop over the two variations
    for var in ["Up", "Down"]:
        if syst == "BJetMistag" or syst == "BJetNorm":
            mc_gjets_qcd_cr_tag_syst_name = mc_gjets_qcd_cr_tag_name
            mc_gjets_qcd_cr_all_syst_name = mc_gjets_qcd_cr_all_name
            mc_gjets_b_cr_tag_syst_name = mc_gjets_b_cr_tag_name
            mc_gjets_b_cr_all_syst_name = mc_gjets_b_cr_all_name
        else:
            mc_gjets_qcd_cr_tag_syst_name = mc_gjets_qcd_cr_tag_name.replace(
                "nom", syst + var
            )
            mc_gjets_qcd_cr_all_syst_name = mc_gjets_qcd_cr_all_name.replace(
                "nom", syst + var
            )
            mc_gjets_b_cr_tag_syst_name = mc_gjets_b_cr_tag_name.replace(
                "nom", syst + var
            )
            mc_gjets_b_cr_all_syst_name = mc_gjets_b_cr_all_name.replace(
                "nom", syst + var
            )
        # qcd jets
        mc_gjets_qcd_cr_tag_syst_hist = hists[mc_gjets_qcd_cr_tag_syst_name]
        mc_gjets_qcd_cr_all_syst_hist = hists[mc_gjets_qcd_cr_all_syst_name]
        # b jets
        mc_gjets_b_cr_tag_syst_hist = hists[mc_gjets_b_cr_tag_syst_name]
        mc_gjets_b_cr_all_syst_hist = hists[mc_gjets_b_cr_all_syst_name]
        if syst == "BJetMistag":
            bjet_sfs = None
            if var == "Up":
                bjet_sfs = np.full_like(mc_gjets_b_cr_tag_syst_hist.values, 1.5)
            elif var == "Down":
                bjet_sfs = np.full_like(mc_gjets_b_cr_tag_syst_hist.values, 0.5)
            mc_gjets_b_cr_tag_syst_hist.apply_sfs(bjet_sfs)
        elif syst == "BJetNorm":
            bjet_norm = None
            if var == "Up":
                bjet_norm = np.full_like(mc_gjets_b_cr_tag_syst_hist.values, 1.5)
            elif var == "Down":
                bjet_norm = np.full_like(mc_gjets_b_cr_tag_syst_hist.values, 0.5)
            mc_gjets_b_cr_tag_syst_hist.apply_sfs(bjet_norm)
            mc_gjets_b_cr_all_syst_hist.apply_sfs(bjet_norm)
        data_gjets_qcd_cr_tag_syst = hists[
            "CR_Gamma_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"
        ].copy("CR_Gamma_AK15Jet_Pt_0_QCD_Tagged__data_obs__nom")
        data_gjets_qcd_cr_all_syst = hists[
            "CR_Gamma_AK15Jet_Pt_0_Any__data_obs__nom"
        ].copy("CR_Gamma_AK15Jet_Pt_0_QCD__data_obs__nom")
        data_gjets_qcd_cr_tag_syst.add(mc_gjets_b_cr_tag_syst_hist, False, -1)
        data_gjets_qcd_cr_all_syst.add(mc_gjets_b_cr_all_syst_hist, False, -1)
        # calculate the mistag fraction for systematically varied data
        mfs["data"][syst + var] = Hist(
            f"mfs_data_{syst}{var}",
            data_gjets_qcd_cr_tag_syst.edges,
            data_gjets_qcd_cr_tag_syst.values / data_gjets_qcd_cr_all_syst.values,
            np.zeros_like(data_gjets_qcd_cr_tag_syst.values),
        )
        # calculate the mistag fraction for systematically varied mc
        mfs["mc"][syst + var] = Hist(
            f"mfs_mc_{syst}{var}",
            mc_gjets_qcd_cr_tag_syst_hist.edges,
            mc_gjets_qcd_cr_tag_syst_hist.values / mc_gjets_qcd_cr_all_syst_hist.values,
            np.zeros_like(mc_gjets_qcd_cr_tag_syst_hist.values),
        )
        # calculate mistag scale factor for systematically varied mc
        sfs[syst + var] = Hist(
            f"sfs_{syst}{var}",
            mfs["data"][syst + var].edges,
            mfs["data"][syst + var].values / mfs["mc"][syst + var].values,
            np.zeros_like(mfs["data"][syst + var].values),
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
    mfs["data"]["nom"].errors = np.sqrt(
        np.square(
            GetSymmUncFromUpDown(
                mfs["data"][syst + "Up"].values, mfs["data"][syst + "Down"].values
            )
        )
        + np.square(mfs["data"]["nom"].errors)
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
print(mfs["data"]["nom"])
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
    "edges": list(mfs["data"]["nom"].edges),
    "values": list(mfs["data"]["nom"].values),
    "uncertainties": list(mfs["data"]["nom"].errors),
}

# data/mc mistag scale factor
json_dict["sf_data_mc"] = {
    "edges": list(sfs["nom"].edges),
    "values": list(sfs["nom"].values),
    "uncertainties": list(sfs["nom"].errors),
}

cset = cs.CorrectionSet(
    schema_version=2,
    description="QCD mistag fractions and data/mc scale factors",
    corrections=[
        CreateCorrection(
            "eff_mc",
            list(mfs["mc"]["nom"].edges),
            list(mfs["mc"]["nom"].values),
            list(mfs["mc"]["nom"].values_up()),
            list(mfs["mc"]["nom"].values_down()),
        ),
        CreateCorrection(
            "eff_data",
            list(mfs["data"]["nom"].edges),
            list(mfs["data"]["nom"].values),
            list(mfs["data"]["nom"].values_up()),
            list(mfs["data"]["nom"].values_down()),
        ),
        CreateCorrection(
            "sf_data_mc",
            list(sfs["nom"].edges),
            list(sfs["nom"].values),
            list(sfs["nom"].values_up()),
            list(sfs["nom"].values_down()),
        ),
    ],
)

with gzip.open("qcd_mistag.json.gz", "wt") as fout:
    fout.write(cset.json(exclude_unset=True, indent=4))
