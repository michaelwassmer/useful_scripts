"""
This script calculates the data/mc scale factors of the top-jet tagging efficiency for the mono-top analysis.
The top-jet tag efficiency is calculated based on the two ttbar control regions (ele and muon channel), which are enriched in events containing genuine top jets.
The input is a ROOT file containing all the necessary templates from the monotop analysis and an optional comma-separated list of systematic uncertainties.

Workflow of the script:
1. ROOT file needs to be read. Histograms need to read and converted to numpy.
2. Summarize necessary QCD-jet and B-jet MC backgrounds in one total NoTop-jet background template including systematics. Do the same for Top-jet MC backgrounds.
3. Expected entries before top-tagging need to be scaled to match the ones in data to be agnostic against unrelated data/mc disagreements.
4. Top tag efficiencies are calculated for MC and data in the ttbar control regions as well as corresponding data/mc scale factors.
5. Save the top tag efficiencies and scale factors in a correctionlib json format.
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

# processes to consider as relevant QCD-jet and B-jet backgrounds
procs = ["ttbar", "SingleTop", "WJetsToLNu_stitched", "diboson", "qcd", "DYJetsToLL"]
# processes that can result in Top-jets
top_procs = ["ttbar", "SingleTop"]
# jet types besides Top-jet
jet_types = ["QCD", "B"]
# all jet types
jet_types_all = ["QCD", "B", "Top"]
# artifical systematics, which need to be created manually are are not available as templates in the ROOT file
systs_calib = ["QCDMistag", "BJetMistag", "BJetNorm"]

# control region where the efficiencies and scale factors are calculated
cr = "CR_TT"

"""
read the necessary histograms, i.e. in ttbar CRs, and put them into a dictionary
dictionary structure:
    key=name of histogram
    value=Hist object i.e. (edges, values, errors)
"""
hists = ReadTemplates(
    infile,
    ["AK15Jet_Pt_0"],
    [f"{cr}_electron", f"{cr}_muon"],
    procs + ["data_obs"],
    systs,
)

# add together electron and muon channels for more statistics
hists_combined = {}
for label in hists.keys():
    if f"{cr}_muon" in label:
        continue
    new_label = label.replace(f"{cr}_electron", f"{cr}_lepton")
    hists_combined[new_label] = hists[label].copy()
    hists_combined[new_label].add(
        hists[label.replace(f"{cr}_electron", f"{cr}_muon")], True
    )
hists.update(hists_combined)

# electron or muon or lepton (combination of ele and mu) channel
lep = "lepton"

# edges of the histograms are assumed to be similar in all histograms, otherwise this method does not work
# therefore just use one histogram to set the edges
edges = np.array(hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__ttbar__nom"].edges)

# load QCD-jet mistag scale factors from correctionlib (those are calculated with CalcQCDMisTagSFs script)
qcd_mistag_correction = correctionlib.CorrectionSet.from_file("qcd_mistag.json.gz")

# get representative AK15 jet pts to retrieve QCD-jet mistag sfs from correctionlib object
# therefore, just increase the edges of the jet pt histograms by 1 and remove the last entry
rep_jet_pts = (edges + 1.0)[:-1]

# then evalute the correctionlib object to get the QCD-jet mistag sfs
qcd_mistag_sfs = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Nom")
qcd_mistag_sfs_up = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Up")
qcd_mistag_sfs_down = qcd_mistag_correction["sf_data_mc"].evaluate(rep_jet_pts, "Down")

# B-Jet mistag scale factors (assume scale factor of 1+-0.5)
bjet_sfs_up = np.full_like(rep_jet_pts, 1.5)
bjet_sfs_down = np.full_like(rep_jet_pts, 0.5)

# B-Jet normalization variations (assume no relevant B-jet norm uncerainty for now)
bjet_norm_up = np.full_like(rep_jet_pts, 1.0)
bjet_norm_down = np.full_like(rep_jet_pts, 1.0)

#########
### 2 ###
#########

### QCD-jet and B-jet processes ###

# calculate summed QCD-jet and B-jet background processes (labeled as NoTop and Bkg) in tag region as well as independent of tag or not (inclusive region)
# start with the nominal MC backgrounds

# create histograms to hold summed QCD-jet and B-jet background processes
# tag region
hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__nom"] = Hist(
    f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__nom",
    edges,
)
# inclusive region
hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__nom"] = Hist(
    f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__nom",
    edges,
)

# loop over processes and add them to the summed background (Bkg) histograms
for proc in procs:
    for jet_type in jet_types:
        # calib/artificial systematics need special treatment since they are not in the ROOT file, therefore create them here as copies of the nominal
        for syst_calib in systs_calib:
            for var in ["Up", "Down"]:
                # copies of the nominal histograms for calib systematics
                hists[
                    f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst_calib}{var}"
                ] = hists[
                    f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__nom"
                ].copy(
                    f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst_calib}{var}"
                )
                hists[
                    f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__{syst_calib}{var}"
                ] = hists[f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__nom"].copy(
                    f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__{syst_calib}{var}"
                )
        # apply QCD-jet mistag scale factor for QCD-jet events in the tag region
        if jet_type == "QCD":
            hists[f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__nom"].apply_sfs(
                qcd_mistag_sfs
            )
        # add single backgrounds to the summed background
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__nom"].add(
            hists[f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__nom"], True
        )
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__nom"].add(
            hists[f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__nom"], True
        )

# print("QCD jets in tag or no tag")
# print(hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__nom"])
# print("QCD jets in tag")
# print(hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__nom"])

# do the same as before but now for systematic variations of the MC processes
for syst in systs + systs_calib:
    for var in ["Up", "Down"]:
        # create the summed histograms
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__{syst+var}"] = Hist(
            f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__{syst+var}",
            edges,
        )
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__{syst+var}"] = Hist(
            f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__{syst+var}",
            edges,
        )
        # now add the processes to them
        for proc in procs:
            for jet_type in jet_types:
                # artifical/calib systematics need special treatment
                # QCD-jet mistag scale factor variations
                if syst + var == "QCDMistagUp" and jet_type == "QCD":
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                    ].apply_sfs(qcd_mistag_sfs_up)
                elif syst + var == "QCDMistagDown" and jet_type == "QCD":
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                    ].apply_sfs(qcd_mistag_sfs_down)
                # B-jet normalization variations (currently not relevant -> 1)
                elif syst + var == "BJetNormUp" and jet_type == "B":
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                    ].apply_sfs(bjet_norm_up)
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__{syst+var}"
                    ].apply_sfs(bjet_norm_up)
                elif syst + var == "BJetNormDown" and jet_type == "B":
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                    ].apply_sfs(bjet_norm_down)
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__{syst+var}"
                    ].apply_sfs(bjet_norm_down)
                # B-jet mistag scale factor variations
                elif syst + var == "BJetMistagUp" and jet_type == "B":
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                    ].apply_sfs(bjet_sfs_up)
                elif syst + var == "BJetMistagDown" and jet_type == "B":
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                    ].apply_sfs(bjet_sfs_down)
                # regular systematic variations from ROOT file
                else:
                    if (
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                        in hists
                    ):
                        # apply nominal QCD-jet mistag scale factors for systematics
                        if jet_type == "QCD":
                            hists[
                                f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                            ].apply_sfs(qcd_mistag_sfs)
                    # replace missing systematics by nominal templates
                    else:
                        hists[
                            f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                        ] = hists[
                            f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__nom"
                        ].copy(
                            f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                        )
                    if (
                        not f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__{syst+var}"
                        in hists
                    ):
                        hists[
                            f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__{syst+var}"
                        ] = hists[
                            f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__nom"
                        ].copy(
                            f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__{syst+var}"
                        )
                # add to summed background (don't propagate stat errors because we deal with systematics here)
                hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__{syst+var}"].add(
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}_Tagged__{proc}__{syst+var}"
                    ],
                    False,
                )
                hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__{syst+var}"].add(
                    hists[f"{cr}_{lep}_AK15Jet_Pt_0_{jet_type}__{proc}__{syst+var}"],
                    False,
                )
# print(hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__nom"])
# print(hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__nom"])

### Top-jet processes ###

# calculate summed Top-jet processes in tag region as well as independent of tag or not (inclusive region)
# start with the nominal MC backgrounds

# create histograms to hold summed Top-jet processes
# tag region
hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"] = Hist(
    f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom",
    edges,
)
# inclusive region
hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"] = Hist(
    f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom",
    edges,
)

# add Top-jet processes together
for proc in top_procs:
    hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"].add(
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__nom"], True
    )
    hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"].add(
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__{proc}__nom"], True
    )

# repeat the same for systematics
for syst in systs + systs_calib:
    for var in ["Up", "Down"]:
        # create the summed histograms
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"] = Hist(
            f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}",
            edges,
        )
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"] = Hist(
            f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}",
            edges,
        )
        # now add the processes to them
        for proc in top_procs:
            # for QCD-jet and B-jet mistag systematics use the nominal Top-jet templates
            if syst in systs_calib:
                hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].add(
                    hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__{proc}__nom"], False
                )
                hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"].add(
                    hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__nom"], False
                )
            # for all other systematics use the variations if available, otherwise use nominal
            else:
                if f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__{syst+var}" in hists:
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"
                    ].add(
                        hists[
                            f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__{syst+var}"
                        ],
                        False,
                    )
                else:
                    hists[
                        f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"
                    ].add(
                        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__{proc}__nom"],
                        False,
                    )
                if f"{cr}_{lep}_AK15Jet_Pt_0_Top__{proc}__{syst+var}" in hists:
                    hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].add(
                        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__{proc}__{syst+var}"],
                        False,
                    )
                else:
                    hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].add(
                        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__{proc}__nom"], False
                    )

#########
### 3 ###
#########

# now create total MC templates in order to be able to calculate data/mc scale factors
hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__nom"] = Hist(
    f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__nom", edges
)
# therefore add the NoTop Bkg and the Top TopBkg templates that were created in the previous step
hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__nom"].add(
    hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"], True
)
hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__nom"].add(
    hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__nom"], True
)
# entries in each bin of the MC templates in the inclusive region are scaled such that ...
# ... the entries match the corresponding entries in data in the inclusive region ...
# ... in order to be agnostic against data/mc differences that are unrelated to the tagger
data_mc_scalefactor_nom = (
    hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"].values
    / hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__nom"].values
)
print("Nominal data/mc scale factors:", data_mc_scalefactor_nom)
# apply data/mc scale factor back to the separated templates
hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"].apply_sfs(
    data_mc_scalefactor_nom
)
hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"].apply_sfs(data_mc_scalefactor_nom)
hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__nom"].apply_sfs(
    data_mc_scalefactor_nom
)
hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__nom"].apply_sfs(data_mc_scalefactor_nom)

# the same is repeated for the systematic variations
for syst in systs + systs_calib:
    for var in ["Up", "Down"]:
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__{syst+var}"] = Hist(
            f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__{syst+var}", edges
        )
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__{syst+var}"].add(
            hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"], False
        )
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__{syst+var}"].add(
            hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__{syst+var}"], False
        )
        data_mc_scalefactor_syst = (
            hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__data_obs__nom"].values
            / hists[f"{cr}_{lep}_AK15Jet_Pt_0_Any__MC__{syst+var}"].values
        )
        # debug
        # print(f"{syst}{var} data/mc scale factors:", data_mc_scalefactor_syst)
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__{syst+var}"].apply_sfs(
            data_mc_scalefactor_syst
        )
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__{syst+var}"].apply_sfs(
            data_mc_scalefactor_syst
        )
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__{syst+var}"].apply_sfs(
            data_mc_scalefactor_syst
        )
        hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__{syst+var}"].apply_sfs(
            data_mc_scalefactor_syst
        )

#########
### 4 ###
#########

# dictionary to contain all the tag efficiencies as Hist objects
tes = {}

# start with mc efficiencies

# mc template in ttbar CR with a tag
mc_top_cr_tag_name = f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__TopBkg__nom"
# mc template in ttbar CR irrespective of tag or not
mc_top_cr_all_name = f"{cr}_{lep}_AK15Jet_Pt_0_Top__TopBkg__nom"

# Top-jet MC template in ttbar CR with a tag
mc_top_cr_tag_hist = hists[mc_top_cr_tag_name]
print(mc_top_cr_tag_hist)
# Top-jet MC template in ttbar CR irrespective of tag or not
mc_top_cr_all_hist = hists[mc_top_cr_all_name]
print(mc_top_cr_all_hist)

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
# in the tag region this is done by estimating the Top-jet processes in data by
# subtracting the MC NoTop-jet processes (summarized in the Bkg templates) from data
# in the inclusive region, the MC prediction for the Top-jet processes is used by definition due to the data/mc scaling

# first get copies of data templates in tag region
data_top_cr_tag_name = f"{cr}_{lep}_AK15Jet_Pt_0_Any_Tagged__data_obs__nom"
# in region independent of tag or not, use MC prediction
data_top_cr_all_name = mc_top_cr_all_name

data_top_cr_tag_hist = hists[data_top_cr_tag_name].copy(
    f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__data_obs__nom"
)

data_top_cr_all_hist = hists[data_top_cr_all_name].copy(
    f"{cr}_{lep}_AK15Jet_Pt_0_Top__data_obs__nom"
)

# now subtract the summed NoTop-jet background templates in the tag region
data_top_cr_tag_hist.add(
    hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__nom"], True, -1.0
)

# data_top_cr_all_hist.add(hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__nom"], True, -1.0)

print(data_top_cr_tag_hist)
print(data_top_cr_all_hist)

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

# nominal scale factor
sfs = {}
sfs_unc_sources = {}
sfs["nom"] = Hist(
    "sfs_nom",
    edges,
    data_top_cr_tag_hist.values / mc_top_cr_tag_hist.values,
    GetSymmUncFromUpDown(
        data_top_cr_tag_hist.values_up() / mc_top_cr_tag_hist.values_down(),
        data_top_cr_tag_hist.values_down() / mc_top_cr_tag_hist.values_up(),
    ),
)
sfs_unc_sources["stat"] = Hist(f"sfs_stat_rel", sfs["nom"].edges, sfs["nom"].errors / sfs["nom"].values, np.zeros_like(sfs["nom"].errors))

print(tes["mc"]["nom"])
print(tes["data"]["nom"])
print(sfs["nom"])

# loop over systematics
for syst in systs + systs_calib:
    # loop over the two variations
    for var in ["Up", "Down"]:
        if not (syst in systs_calib):
            mc_top_cr_tag_syst_name = mc_top_cr_tag_name.replace("nom", syst + var)
            if not mc_top_cr_tag_syst_name in hists:
                mc_top_cr_tag_syst_name = mc_top_cr_tag_name
            mc_top_cr_all_syst_name = mc_top_cr_all_name.replace("nom", syst + var)
            if not mc_top_cr_all_syst_name in hists:
                mc_top_cr_all_syst_name = mc_top_cr_all_name
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
        data_top_cr_all_syst_name = (
            mc_top_cr_all_syst_name  # .replace("nom", syst + var)
        )

        data_top_cr_tag_syst_hist = hists[data_top_cr_tag_syst_name].copy(
            f"{cr}_{lep}_AK15Jet_Pt_0_Top_Tagged__data_obs__{syst+var}"
        )

        data_top_cr_all_syst_hist = hists[data_top_cr_all_syst_name].copy(
            f"{cr}_{lep}_AK15Jet_Pt_0_Top__data_obs__{syst+var}"
        )

        data_top_cr_tag_syst_hist.add(
            hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop_Tagged__Bkg__{syst+var}"], False, -1.0
        )

        # data_top_cr_all_syst_hist.add(
        #     hists[f"{cr}_{lep}_AK15Jet_Pt_0_NoTop__Bkg__{syst+var}"], False, -1.0
        # )

        tes["data"][syst + var] = Hist(
            f"tes_data_{syst+var}",
            edges,
            data_top_cr_tag_syst_hist.values / data_top_cr_all_syst_hist.values,
            np.zeros_like(data_top_cr_tag_syst_hist.values),
        )
        print(tes["data"][syst + var])

        # calculate mistag scale factors for systematically variated mc
        if syst in systs_calib:
            sfs[syst + var] = Hist(
                f"sfs_{syst}{var}",
                edges,
                data_top_cr_tag_syst_hist.values / mc_top_cr_tag_hist.values,
                np.zeros_like(tes["data"][syst + var].values),
            )
        else:
            sfs[syst + var] = Hist(
                f"sfs_{syst}{var}",
                edges,
                data_top_cr_tag_syst_hist.values / mc_top_cr_tag_syst_hist.values,
                np.zeros_like(tes["data"][syst + var].values),
            )
    # calculate the total error of the nominal mistag fraction by adding the single uncertainties in quadrature
    if not (syst in systs_calib):
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
    sfs_unc_sources[syst] = Hist(f"sfs_{syst}_rel", sfs["nom"].edges, GetSymmUncFromUpDown(sfs[syst + "Up"].values, sfs[syst + "Down"].values) / sfs["nom"].values, np.zeros_like(sfs["nom"].errors))
    sfs_unc_sources["total"] = Hist(f"sfs_total_rel", sfs["nom"].edges, sfs["nom"].errors / sfs["nom"].values, np.zeros_like(sfs["nom"].errors))

print(tes["mc"]["nom"])
print(tes["data"]["nom"])
print(sfs["nom"])
for syst, hist in sfs_unc_sources.items():
    print(f"| {syst} | " + " | ".join(f"{value} %" for value in list(np.round(100.*hist.values,1))) + "|")

#########
### 5 ###
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
