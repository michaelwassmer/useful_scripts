"""
This script calculates the data/mc scale factors of the top-jet tagging efficiency for the mono-top analysis.
The top tag efficiency is calculated based on the two ttbar control regions (ele and muon channel), which are enriched in events containing genuine top jets.
The input is a ROOT file containing all the necessary templates from the monotop analysis and an optional comma-separated list of systematic uncertainties.

Workflow of the script:
1. ROOT file needs to be read. Histograms/Templates need to read and converted to numpy arrays.
2. Summarize necessary MC top-jet backgrounds in one total top-jet background template including systematics.
3. Top-jet tag efficiencies are calculated for MC and data in the ttbar control regions as well as corresponding data/mc scale factors.
4. Save the top-jet tag efficiencies and scale factors in a correctionlib json format.
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

# processes that can result in top jets
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
# therefore just use one histogram which needs to be there to set the edges
edges = np.array(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__nom"].edges)

# load qcd-jet mistag scale factors from correctionlib
qcd_mistag_correction = correctionlib.CorrectionSet.from_file("qcd_mistag.json.gz")

# get representative AK15 jet pts to retrieve qcd-jet mistag sfs and data efficiencies from correctionlib object
# therefore just increase the edges of the jet pt histograms by 1 and remove the last entry
rep_jet_pts = (edges + 1.0)[:-1]
# then evalute the correctionlib object to get the qcd-jet mistag sfs
qcd_mistag_sfs = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Nom")
qcd_mistag_sfs_up = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Up")
qcd_mistag_sfs_down = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Down")
# also need qcd-jet mistag fractions in data
qcd_mistag_effs = qcd_mistag_correction["eff_data"].evaluate(rep_jet_pts, "Nom")
qcd_mistag_effs_up = qcd_mistag_correction["eff_data"].evaluate(rep_jet_pts, "Up")
qcd_mistag_effs_down = qcd_mistag_correction["eff_data"].evaluate(rep_jet_pts, "Down")

#########
### 2 ###
#########

# calculate summed top-jet processes in tag region as well as independent of tag or not
# start with the nominal MC backgrounds

# create histograms to hold summed top-jet processes
# region independent of tag
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"] = Hist(
    f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom",
    edges,
)
# region with tag
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

# repeat the same for systematics
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
            # for QCD-jet mistag systematics use the nominal top-jet templates
            if syst == "QCDMistag":
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].add(
                    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__{proc}__nom"], False
                )
                hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"].add(
                    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__nom"], False
                )
            # for all other systematics use the variations if available otherwise nominal
            else:
                if f"CR_TT_{lep}_AK15Jet_Pt_0_Top__{proc}__{syst+var}" in hists:
                    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].add(
                        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__{proc}__{syst+var}"],
                        False,
                    )
                else:
                    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].add(
                        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__{proc}__nom"], False
                    )
                if f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__{syst+var}" in hists:
                    hists[
                        f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"
                    ].add(
                        hists[
                            f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__{syst+var}"
                        ],
                        False,
                    )
                else:
                    hists[
                        f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"
                    ].add(
                        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__nom"],
                        False,
                    )

# calculate qcd-jet processes/contributions in region independent of tag by subtracting the top-jet processes/contributions from the data in this region
# clone data
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"] = hists[
    f"CR_TT_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"
].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom")
# subtract top-jet processes/contributions from data
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"].add(
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"], True, -1.0
)

# repeat for systematics
for syst in systs + ["QCDMistag"]:
    for var in ["Up", "Down"]:
        # clone data
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"] = hists[
            f"CR_TT_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"
        ].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}")
        # subtract top-jet processes from data
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"].add(
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"], False, -1.0
        )

# calculate top-jet processes in tag region by extrapolating the qcd-jet backgrounds into the tag region via the qcd-jet mistag fractions in data
# then subtract this extrapolation from data in the tag region to obtain the top-jet contributions in this region
# clone data
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data"] = hists[
    f"CR_TT_{lep}_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"
].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data")
# clone qcd-jet backgrounds from the region independent of tag
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"] = hists[
    f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__nom"
].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom")
# extrapolate it to the tag region via the qcd-jet mistag fractions in data
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"].apply_sfs(qcd_mistag_effs)
# subtract the extrapolation from the data
hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data"].add(
    hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__nom"], True, -1.0
)
# compare top-jet processes obtained from data via extrapolation with the same only using MC truth
print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data"])
print(hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"])

# repeat same procedure for systematics
for syst in systs + ["QCDMistag"]:
    for var in ["Up", "Down"]:
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}_Data"] = hists[
            f"CR_TT_{lep}_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"
        ].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}_Data")
        hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"] = hists[
            f"CR_TT_{lep}_AK15Jet_Pt_0_QCD__Bkg__{syst+var}"
        ].copy(f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}")
        # qcd-jet mistag efficiency up
        if syst + var == "QCDMistagUp":
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"].apply_sfs(
                qcd_mistag_effs_up
            )
        # qcd-jet mistag efficiency down
        elif syst + var == "QCDMistagDown":
            hists[f"CR_TT_{lep}_AK15Jet_Pt_0_QCD_Tagged__Bkg__{syst+var}"].apply_sfs(
                qcd_mistag_effs_down
            )
        # all other systematics
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

# dictionary to contain all the top-jet tag efficiencies as Hist objects
tes = {}

# start with mc efficiencies

# top-jet template in ttbar CR with a tag
mc_top_cr_tag_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"
# top-jet template in ttbar CR irrespective of tag or not
mc_top_cr_all_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"

# top-jet MC template in ttbar CR with a tag
mc_top_cr_tag_hist = hists[mc_top_cr_tag_name]
# top-jet MC template in ttbar CR irrespective of tag or not
mc_top_cr_all_hist = hists[mc_top_cr_all_name]

# top-jet tag efficiency in mc
tes["mc"] = {}

# calculate top-jet tag efficiency in nominal (nom, i.e. no systematic variations) MC by just dividing tag/all
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

# for top-jet contributions in tag region use what has been determined above with the extrapolation method
data_top_cr_tag_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom_Data"
# for top-jet contributions in region independent of tag use the MC estimation since its usually very good for top processes
data_top_cr_all_name = f"CR_TT_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"

# corresponding histograms/templates
data_top_cr_tag_hist = hists[data_top_cr_tag_name]
data_top_cr_all_hist = hists[data_top_cr_all_name]

# print(data_top_cr_tag_hist)
# print(data_top_cr_all_hist)

# print(data_top_cr_tag_hist)
# print(data_top_cr_all_hist)

# top-jet tag efficiency in data
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
    # np.sqrt(
    #     np.square(tes["data"]["nom"].errors / tes["mc"]["nom"].values)
    #     + np.square(
    #         GetSymmUncFromUpDown(
    #             tes["data"]["nom"].values / tes["mc"]["nom"].values_up(),
    #             tes["data"]["nom"].values / tes["mc"]["nom"].values_down(),
    #         )
    #     )
    # ),
    GetSymmUncFromUpDown(
        tes["data"]["nom"].values_up() / tes["mc"]["nom"].values_down(),
        tes["data"]["nom"].values_down() / tes["mc"]["nom"].values_up(),
    ),
)

print(sfs["nom"])

# loop over systematics
for syst in systs + ["QCDMistag"]:
    # loop over the two variations
    for var in ["Up", "Down"]:
        if syst != "QCDMistag":
            mc_top_cr_tag_syst_name = mc_top_cr_tag_name.replace("nom", syst + var)
            if not mc_top_cr_tag_syst_name in hists:
                mc_top_cr_tag_syst_name = mc_top_cr_tag_name
            mc_top_cr_all_syst_name = mc_top_cr_all_name.replace("nom", syst + var)
            if not mc_top_cr_all_syst_name in hists:
                mc_top_cr_all_syst_name = mc_top_cr_all_name
            mc_top_cr_tag_syst_hist = hists[mc_top_cr_tag_syst_name]
            mc_top_cr_all_syst_hist = hists[mc_top_cr_all_syst_name]
            # calculate the top-jet tag efficiency for systematically variated mc
            tes["mc"][syst + var] = Hist(
                f"tes_mc_{syst}{var}",
                edges,
                mc_top_cr_tag_syst_hist.values / mc_top_cr_all_syst_hist.values,
                np.zeros_like(mc_top_cr_tag_syst_hist.values),
            )
            print(tes["mc"][syst + var])

        # data effiencies analogously to the nominal case but now for systematically variated MC
        data_top_cr_tag_syst_name = data_top_cr_tag_name.replace("nom", syst + var)
        if not data_top_cr_tag_syst_name in hists:
            data_top_cr_tag_syst_name = data_top_cr_tag_name
        data_top_cr_all_syst_name = data_top_cr_all_name.replace("nom", syst + var)
        if not data_top_cr_all_syst_name in hists:
            data_top_cr_all_syst_name = data_top_cr_all_name
        data_top_cr_tag_syst_hist = hists[data_top_cr_tag_syst_name]
        data_top_cr_all_syst_hist = hists[data_top_cr_all_syst_name]

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
        print(sfs[syst + var])

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

# create correctionlib object
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

# save top tag efficiencies and scale factors
with gzip.open("top_tag.json.gz", "wt") as fout:
    fout.write(cset.json(exclude_unset=True, indent=4))
