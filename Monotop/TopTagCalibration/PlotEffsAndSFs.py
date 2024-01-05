# imports
import sys
import gzip
import json
import matplotlib.pyplot as plt
import numpy as np

# three input arguments need to be provided
if len(sys.argv) != 4:
    raise RuntimeError("Number of input arguments is not correct! Exiting ... ")

# input file: correctionlib json
input_file = sys.argv[1]
# jet type to put on the plot
jet_type = sys.argv[2]
# era to put on the plot
era = sys.argv[3]

# catch some errors
if not input_file.endswith(".json.gz"):
    raise RuntimeError(
        "Input file has the wrong file extension, please check! Exiting ... "
    )
if not (jet_type in ["Top-jet", "QCD-jet"]):
    raise RuntimeError("Unknown jet type, please check! Exiting ... ")
if not (era in ["2018", "2017", "2016postVFP", "2016preVFP"]):
    raise RuntimeError("Unknown era, please check! Exiting ... ")


# desired corrections from correction json
necessary_corrections = ["eff_mc", "eff_data", "sf_data_mc"]
# corresponding labels
correction_labels = ["MC Efficiency", "Data Efficiency", "Data/MC scale factor"]
label_dict = dict(zip(necessary_corrections, correction_labels))
print(label_dict)

# open correction json file and read interesting stuff from it
with gzip.open(input_file, "r") as json_file:
    json_content = json_file.read()
    json_dict = json.loads(json_content)
    corrections = json_dict["corrections"]
    # three corrections are expected in the json (mc efficiency, data efficiency, data/mc scale factor)
    if len(corrections) != 3:
        raise RuntimeError(
            "Number of corrections in json file is not equal to 3! Exiting ..."
        )
    # create separate dictionary to store only the interesting stuff from the json
    correction_dict = {}
    # loop over all included corrections
    for correction in corrections:
        # print(correction)
        # search for the desired corrections
        for necessary_correction in necessary_corrections:
            if correction["name"] == necessary_correction:
                correction_dict[necessary_correction] = {}
                correction_variations = correction["data"]["content"]
                # nominal values and edges
                correction_dict[necessary_correction]["Nom"] = {}
                correction_dict[necessary_correction]["Nom"]["Edges"] = np.array(
                    correction["data"]["default"]["edges"]
                )
                correction_dict[necessary_correction]["Nom"]["Values"] = np.array(
                    correction["data"]["default"]["content"]
                )
                # systematic variation values and edges
                for correction_variation in correction_variations:
                    correction_dict[necessary_correction][
                        correction_variation["key"]
                    ] = {}
                    correction_dict[necessary_correction][correction_variation["key"]][
                        "Edges"
                    ] = np.array(correction_variation["value"]["edges"])
                    correction_dict[necessary_correction][correction_variation["key"]][
                        "Values"
                    ] = np.array(correction_variation["value"]["content"])

print(correction_dict)

# plotting
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle(f"{jet_type}, {era}")

x_edges = correction_dict["eff_mc"]["Nom"]["Edges"]
# calculate x values of points from edges -> centers between edges (same in all corrections)
x_values = (
    correction_dict["eff_mc"]["Nom"]["Edges"][1:]
    + correction_dict["eff_mc"]["Nom"]["Edges"][:-1]
) / 2.0
# calculate x errors of points
x_error = (
    correction_dict["eff_mc"]["Nom"]["Edges"][1:]
    - correction_dict["eff_mc"]["Nom"]["Edges"][:-1]
) / 2.0
# mc efficiency
y_values_eff_mc = correction_dict["eff_mc"]["Nom"]["Values"]
y_error_eff_mc = (
    correction_dict["eff_mc"]["Up"]["Values"]
    - correction_dict["eff_mc"]["Down"]["Values"]
) / 2.0
ax1.errorbar(
    x_values,
    y_values_eff_mc,
    xerr=x_error,
    yerr=y_error_eff_mc,
    marker="o",
    fmt="o",
    label="MC",
)
# data efficiency
y_values_eff_data = correction_dict["eff_data"]["Nom"]["Values"]
y_error_eff_data = (
    correction_dict["eff_data"]["Up"]["Values"]
    - correction_dict["eff_data"]["Down"]["Values"]
) / 2.0
ax1.errorbar(
    x_values,
    y_values_eff_data,
    xerr=x_error,
    yerr=y_error_eff_data,
    marker="o",
    fmt="o",
    label="Data",
)
# ax1.set_xlabel("AK15 jet pt")
if jet_type == "Top-jet":
    min = 0.0
    max = 1.0
elif jet_type == "QCD-jet":
    min = 0.0
    max = 0.06
ax1.set_ylim(
    top=max,
    bottom=min,
)
ax1.set_ylabel("Efficiency")
ax1.set_xticks(x_edges)
ax1.grid(axis="y")
ax1.legend()

# scale factors
y_values_sf = correction_dict["sf_data_mc"]["Nom"]["Values"]
y_error_sf = (
    correction_dict["sf_data_mc"]["Up"]["Values"]
    - correction_dict["sf_data_mc"]["Down"]["Values"]
) / 2.0
ax2.errorbar(
    x_values,
    y_values_sf,
    xerr=x_error,
    yerr=y_error_sf,
    marker="o",
    fmt="o",
    color="black",
)
ax2.set_xlabel("AK15 jet pt (GeV)")
ax2.set_xticks(x_edges)
if jet_type == "Top-jet":
    min = 0.5
    max = 1.5
elif jet_type == "QCD-jet":
    min = 1.0
    max = 3.0
ax2.set_ylim(
    top=max,
    bottom=min,
)
ax2.set_ylabel("Data/MC SF")
ax2.grid(axis="y")

# save plot as pdf
plt.savefig(f"{jet_type}_{era}.pdf")
