# necessary for type annotations with forward references
from __future__ import annotations

# uproot to read ROOT files
import uproot as up

# statsmodels to calculate binomial confidence intervals
import statsmodels.api as sm

# numpy calculations with arrays
import numpy as np

# to make copies of Hist class
import copy

# correctionlib
import correctionlib.schemav2 as cs


# container for histogram information
class Hist:
    def __init__(
        self,
        name: str,
        edges: list[float],
        values: list[float] = [],
        errors: list[float] = [],
    ) -> None:
        self.name = name
        assert len(edges) > 1
        self.edges = np.array(edges)
        if len(values) > 0:
            assert len(values) == len(edges) - 1
            self.values = np.array(values)
        else:
            self.values = np.zeros(len(self.edges) - 1)
        if len(errors) > 0:
            assert len(errors) == len(edges) - 1
            self.errors = np.array(errors)
        else:
            self.errors = np.zeros(len(self.edges) - 1)

    def __str__(self) -> str:
        str = f"""
        name: {self.name}
        edges: {self.edges}
        values: {self.values}
        errors: {self.errors}
        """
        return str

    def add(
        self, hist_to_add: Hist, add_uncs_quad: bool = False, factor: float = 1.0
    ) -> None:
        assert np.array_equal(self.edges, hist_to_add.edges)
        # assert len(self.values) == len(hist_to_add.values)
        # assert len(self.errors) == len(hist_to_add.errors)
        if add_uncs_quad:
            # add uncertainties in quadrature if desired
            self.errors = np.sqrt(
                np.square(self.errors) + np.square(abs(factor) * hist_to_add.errors)
            )
        else:
            # reset errors
            self.errors = np.zeros_like(self.values)
        # add bin contents
        self.values = self.values + (factor * hist_to_add.values)

    def apply_sfs(self, sfs: list[float]) -> None:
        assert len(self.values) == len(sfs)
        # assert len(self.errors) == len(sfs)
        # calculate new bin contents
        self.values = self.values * np.array(sfs)
        # calculate new uncertainties
        self.errors = self.errors * np.array(sfs)

    def values_up(self) -> np.ndarray:
        return self.values + self.errors

    def values_down(self) -> np.ndarray:
        return self.values - self.errors

    def copy(self, new_name: str = "") -> Hist:
        clone = copy.deepcopy(self)
        if new_name != "":
            clone.name = new_name
        return clone


# function to read templates/histograms from a ROOT file via uproot based on a few search
# keys that need to be present in the name of the histogram
def ReadTemplates(
    infile: str,
    var_search_keys: list[str],
    cat_search_keys: list[str],
    proc_search_keys: list[str],
    syst_search_keys: list[str],
) -> dict[str, Hist]:
    templates = {}
    # open ROOT file
    with up.open(infile) as rfile:
        # loop over contents
        for name, type in rfile.classnames().items():
            # only consider histograms i.e. TH1D
            if type != "TH1D":
                continue
            # only consider templates showing a specific variable
            if not KeepHist(name, var_search_keys):
                continue
            # only consider templates in specific categories
            if not KeepHist(name, cat_search_keys):
                continue
            # only consider templates from specific processes
            if not KeepHist(name, proc_search_keys):
                continue
            # only consider templates for the following systematics
            if not KeepHist(name, ["nom"] + syst_search_keys):
                continue
            name = name.replace(";1", "")
            print(name, type)
            # read information and store it in dict
            templates[name] = ReadHist(rfile, name)
    return templates


# read specific histogram from file and return it as a Hist instance
def ReadHist(file, hist_name: str) -> Hist:
    values = file[hist_name].values()
    errors = file[hist_name].errors()
    edges = file[hist_name].axis().edges()
    return Hist(hist_name, edges, values, errors)


# decide whether to keep a histogram depending on its name and some search keys
def KeepHist(hist_name: str, search_keys: list[str]) -> bool:
    keep_hist = False
    for search_key in search_keys:
        if search_key in hist_name:
            keep_hist = True
            break
    return keep_hist


# calculate a symmetrized uncertainty from an up- and down-variation of a histogram
def GetSymmUncFromUpDown(hist_up: np.ndarray, hist_down: np.ndarray) -> np.ndarray:
    hist_diff = np.absolute(hist_up - hist_down)
    hist_diff = hist_diff / 2
    return hist_diff


# calculate binomial error of a proportion based on the number of selected events and the total events
def GetEffStatErrors(
    hist_selected: np.ndarray, hist_all: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    down, up = sm.stats.proportion_confint(
        hist_selected, hist_all, alpha=0.32, method="beta"
    )
    return up, down


def CreateCorrection(
    label: str,
    edges: list[float],
    nom_values: list[float],
    up_values: list[float],
    down_values: list[float],
):
    correction = cs.Correction(
        name=label,
        version=1,
        inputs=[
            cs.Variable(
                name="pt",
                type="real",
                description="Transverse momentum (pt) of the AK15 jet",
            ),
            cs.Variable(name="syst", type="string", description="Systematic"),
        ],
        output=cs.Variable(
            name="value",
            type="real",
            description="value",
        ),
        data=cs.Category(
            nodetype="category",
            input="syst",
            content=[
                cs.CategoryItem(
                    key="Up",
                    value=cs.Binning(
                        nodetype="binning",
                        input="pt",
                        edges=edges,
                        content=up_values,
                        flow="clamp",
                    ),
                ),
                cs.CategoryItem(
                    key="Down",
                    value=cs.Binning(
                        nodetype="binning",
                        input="pt",
                        edges=edges,
                        content=down_values,
                        flow="clamp",
                    ),
                ),
            ],
            default=cs.Binning(
                nodetype="binning",
                input="pt",
                edges=edges,
                content=nom_values,
                flow="clamp",
            ),
        ),
    )
    return correction
