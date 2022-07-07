from __future__ import print_function
from optparse import OptionParser
from array import array
import collections

# function to check whether a variable is a typical ROOT-style array variable with a requested index, e.g. jet_pt[5]
def IsArrVar(arr_var):
    if "[" in arr_var and "]" in arr_var:
        index_1 = arr_var.find("[")
        index_2 = arr_var.find("]")
        index = arr_var[1+int(index_1):int(index_2)]
        if index.isdigit():
            return True
        else:
            return False
    else:
        return False

# function to find the requested index of an array variable, e.g. 5 in jet_pt[5]
def FindArrVarIndex(arr_var):
    if not IsArrVar(arr_var):
        raise ValueError("The given array variable >>>{}<<< doesn't have the expected structure of an array variable var[number]".format(arr_var),"Exiting ...")
    index_1 = arr_var.find("[")
    index_2 = arr_var.find("]")
    index = arr_var[1+int(index_1):int(index_2)]
    return index

# function to transform an array variable with a requested index in a variable without the [] construction, e.g. jet_pt[5]->jet_pt_5
def TransformArrVar(arr_var):
    index = FindArrVarIndex(arr_var)
    transformed_arr_var = arr_var.replace("["+str(index)+"]","_"+str(index))
    return transformed_arr_var

# function to remove the requested index from an array variable, e.g. jet_pt[5]->jet_pt
def RemoveArrVarIndex(arr_var):
    index = FindArrVarIndex(arr_var)
    arr_var_without_index = arr_var.replace("["+str(index)+"]","")
    return arr_var_without_index

usage = "usage: %prog [options] file1.root file2.root"
parser = OptionParser()
parser.add_option(
    "-n", "--name", dest="name", type="string", default="unnamed", help="name to recognize output"
)
parser.add_option(
    "-t",
    "--treename",
    dest="treename",
    type="string",
    default="",
    help="name of the ROOT tree in the ROOT files you want to process"
)
parser.add_option(
    "-f",
    "--dataframe",
    dest="is_dataframe",
    action="store_true",
    default=False,
    help="set this flag if you want to pass a dataframe directly as an argument",
)
parser.add_option(
    "-s",
    "--save",
    dest="save",
    action="store_true",
    default=False,
    help="set this flag if you want to save the generated dataframe to disk",
)
parser.add_option(
    "-j", "--nthreads", dest="nthreads", type="int", default=4, help="number of threads to use, default is 4"
)
parser.add_option(
     "-S",
     "--selection",
     dest="selection",
     type="string",
     default="(true)",
     help="ROOT selection string using branches in the used ROOT tree",
)
parser.add_option(
    "-1",
    "--variables_1D",
    dest="variables_1D",
    type="string",
    default="",
    help="string containing the variables you want to create 1D templates of as comma separated list, e.g. var1,var2,var3,..."
)
parser.add_option(
    "-2",
    "--variables_2D",
    dest="variables_2D",
    type="string",
    default="",
    help="string containing the variables you want to create 2D templates of as comma separated list, e.g. varx1:vary1,varx2:vary2,..."
)
parser.add_option(
    "-a",
    "--add_variables",
    dest="add_variables",
    type="string",
    default="",
    help="string for needed additional variables (e.g. weights or variables to construct other variables from) as comma separated list, e.g. vara,varb,varc,..."
)
parser.add_option(
    "-c",
    "--constr_variables",
    dest="constr_variables",
    type="string",
    default="",
    help="ROOT string for needed constructed variables as comma separated list, e.g. varxy=varx+vary,varuvw=varu-varx-varw,..."
)
parser.add_option(
    "-w",
    "--weight",
    dest="weight",
    type="string",
    default="1",
    help="ROOT string of the weight which should be applied to all events, e.g. generator_weight*sample_weight. The single weights making up the total weight need to be given in the add_variables option for them to be available."
)

(options, args) = parser.parse_args()

# create a list of desired template variables from input arguments
vars_1D = options.variables_1D.split(",")
vars_2D = options.variables_2D.split(",")
add_vars = options.add_variables.split(",")
constr_vars = options.constr_variables.split("#")
print("1D variables: ",vars_1D)
print("2D variables: ",vars_2D)
print("additional variables: ",add_vars)
print("constructed variables: ",constr_vars)

# account for the case that nothing is given as input arguments
if vars_1D == [""]:
    vars_1D = []
if vars_2D == [""]:
    vars_2D = []
if add_vars == [""]:
    add_vars = []
if constr_vars == [""]:
    constr_vars = []

# determine the needed branches from the desired template variables and the additional variables
branches = []
constructed_vars = collections.OrderedDict()
for var_1D in vars_1D:
    var = None
    var_weight = None
    if ";" in var_1D:
        var_1D_list = var_1D.split(";")
        var = var_1D_list[0]
        if len(var_1D_list) == 5: var_weight = var_1D_list[4]
    else:
        var = var_1D
    if var and IsArrVar(var):
        constructed_vars[TransformArrVar(var)]=var
        var = RemoveArrVarIndex(var)
    if var_weight and IsArrVar(var_weight):
        constructed_vars[TransformArrVar(var_weight)]=var_weight
        var_weight = RemoveArrVarIndex(var_weight)
    if var and (not var in branches):
        branches.append(var)
    if var_weight and (not var_weight in branches):
        branches.append(var_weight)
for var_2D in vars_2D:
    vars = var_2D.split(":")
    var_1D_x = vars[0]
    var_1D_y = vars[1]
    varx = None
    vary = None
    if ";" in var_1D_x:
        varx = var_1D_x.split(";")[0]
    else:
        varx = var_1D_x
    if ";" in var_1D_y:
        vary = var_1D_y.split(";")[0]
    else:
        vary = var_1D_y
    if not varx in branches:
        branches.append(varx)
    if not vary in branches:
        branches.append(vary)
for add_var in add_vars:
    if not add_var in branches:
        branches.append(add_var)

print("needed branches: ",branches)

# import needed ROOT stuff and set some options
import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)
from ROOT import RDataFrame as RDF

# ROOT.PyConfig.IgnoreCommandLineOptions = True
# set the number of threads the RDataFrame is supposed to use
ROOT.ROOT.EnableImplicitMT(options.nthreads)

# dictionary of variables you explicitly construct from the branches above
for constr_var in constr_vars:
    var = None
    formula = None
    var,formula = constr_var.split(":=")
    constructed_vars[var] = formula
print(constructed_vars)

# add branches to a corresponding ROOT vector to later pass to initialization of RDataFrame
branch_vec = ROOT.vector("string")()
for branch in branches:
    branch_vec.push_back(branch)

# initialize RDataFrame
data_frame = None

# either create the RDataFrame from a ROOT tree in a file or from a ROOT chain made up of several files
# or create it directly from an existing RDataFrame including a ROOT tree
if not options.is_dataframe:
    print ("No dataframe was given. Handling the arguments as trees and adding them to chain.")
    input_files = args
    input_chain = ROOT.TChain(options.treename)
    for input_file in input_files:
        input_chain.Add(input_file)
    print ("Finished loading chain with ", input_chain.GetEntries(), " entries")
    data_frame = RDF(input_chain, branch_vec)
else:
    print ("Dataframe flag was set. Handling argument as dataframe.")
    input_file = args[0]
    data_frame = RDF(options.treename, input_file)

print ("Finished creating the RDataFrame")

# possibly save the created RDataFrame to disk
if not options.is_dataframe and options.save:
    print ("saving dataframe to disk as ", data_mc_string + "_" + names + "_dataframe.root")
    data_frame.Snapshot("tree", data_mc_string + "_" + names + "_dataframe.root", branch_vec)
    print ("saved dataframe to disk ...")

# a label for the ouput files
name = options.name

# a ROOT style selection string
selection = options.selection

# dictionaries to contain the requested 1D and 2D templates
histos_1D={}
histos_2D={}

# define a weight on the events
# the weight can also be a branch or constructed from several branches, e.g. generator_weight*sample_weight
reference_events = data_frame.Define("weight",options.weight)
# define constructed variables on RDataFrame
for constructed_var in constructed_vars:
    reference_events=reference_events.Define(constructed_var,constructed_vars[constructed_var])

# apply the selection from above to the RDataFrame
reference_events = reference_events.Filter(selection)

# loop over 1D variables given as input arguments
for i, var_1D in enumerate(vars_1D):
    var,nbinsx,x_low,x_high,var_weight = None,30,1,1,None
    Histo1D_argument = None
    weight = "weight"
    # if a binning and range is given use that binning and range, if not use 50 bins and let ROOT decide the range
    if ";" in var_1D:
        var_1D_list = var_1D.split(";")
        var,nbinsx,x_low,x_high = str(var_1D_list[0]), int(var_1D_list[1]), float(var_1D_list[2]), float(var_1D_list[3])
        if len(var_1D_list) == 5: var_weight = str(var_1D_list[4])
    else:
        var = var_1D
    if var and IsArrVar(var):
        var = TransformArrVar(var)
    histo_key = "{}".format(var)
    if var_weight:
        if IsArrVar(var_weight):
            var_weight = TransformArrVar(var_weight)
        if "var_weight_{}".format(var_weight) not in reference_events.GetDefinedColumnNames():
            reference_events = reference_events.Define("var_weight_{}".format(var_weight),"weight*{}".format(var_weight))
        histo_key += "_{}".format(var_weight)
        weight = "var_weight_{}".format(var_weight)
    Histo1D_argument = (histo_key, "title;{};arbitrary units".format(var), nbinsx, x_low, x_high)
    #print(var_1D)
    #print(Histo1D_argument)
    # define the desired histograms on the RDataFrame after selection and assign the previously defined weight to the events
    histos_1D[histo_key]=reference_events.Histo1D(
                                          Histo1D_argument,
                                          var,weight
                                          )

#print(histos_1D)

# loop over 2D variables given as input arguments
for var_2D in vars_2D:
    vars = var_2D.split(":")
    var_1D_x = vars[0]
    var_1D_y = vars[1]
    varx = None
    vary = None
    Histo2D_argument_x = None
    Histo2D_argument_y = None
    if ";" in var_1D_x:
        varx,nbinsx,x_low,x_high = var_1D_x.split(";")
        Histo2D_argument_x = (int(nbinsx), float(x_low), float(x_high))
    else:
        varx = var_1D_x
        Histo2D_argument_x = (50, 1, 1)
    if ";" in var_1D_y:
        vary,nbinsy,y_low,y_high = var_1D_y.split(";")
        Histo2D_argument_y = (int(nbinsy), float(y_low), float(y_high))
    else:
        vary = var_1D_y
        Histo2D_argument_y = (50, 1, 1)
    Histo2D_argument = ("{}_{}".format(varx,vary), "title;{};{};arbitrary units".format(varx,vary)) + Histo2D_argument_x + Histo2D_argument_y
    histos_2D["{}_{}".format(varx,vary)]=reference_events.Histo2D(
                                          Histo2D_argument,
                                          varx,vary,"weight"
                                          )

#print(histos_2D)

# create a ROOT file and write all the created histograms into the file
output_file = ROOT.TFile(name + ".root", "RECREATE")
for histo_1D in histos_1D:
    output_file.WriteTObject(histos_1D[histo_1D].GetPtr())
for histo_2D in histos_2D:
    output_file.WriteTObject(histos_2D[histo_2D].GetPtr())
output_file.Close()

print("Finished writing templates")
