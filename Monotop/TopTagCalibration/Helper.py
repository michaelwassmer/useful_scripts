# uproot to read ROOT files
import uproot as up

# statsmodels to calculate binomial confidence intervals
import statsmodels.api as sm

# numpy calculations with arrays
import numpy as np


# container for histogram information
class Hist:
    def __init__(
        self, name: str, edges: list[float], values: list[float], errors: list[float]
    ) -> None:
        self.name = name
        self.edges = edges
        self.values = values
        self.errors = errors

    def __str__(self):
        str = f"""
        name: {self.name}
        edges: {self.edges}
        values: {self.values}
        errors: {self.errors}
        """
        return str


# function to read templates/histograms from a ROOT file via uproot based on a few search
# keys that need to be present in the name of the histogram
def ReadTemplates(
    infile: str,
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
