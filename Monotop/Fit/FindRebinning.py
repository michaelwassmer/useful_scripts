import sys
import ROOT
import math

input_file = sys.argv[1]
input_template = sys.argv[2]
acceptable_uncertainty = float(sys.argv[3])

root_file = ROOT.TFile.Open(input_file,"READ")

histogram = root_file.Get(input_template).Clone()

print histogram.GetEntries()

relative_uncertainty = 100000.
content = 0.
error_squared = 0.
lower_bin_edges = []

for i in range(histogram.GetNbinsX(),0,-1):
    if relative_uncertainty > acceptable_uncertainty:
        content += histogram.GetBinContent(i)
        error_squared += math.pow(histogram.GetBinError(i),2)
        try:
            relative_uncertainty = math.sqrt(error_squared)*1.0/content
        except ZeroDivisionError:
            relative_uncertainty = 100000.
        #print content
        #print error_squared
        #print relative_uncertainty
    else:
        lower_bin_edges.append(histogram.GetBinLowEdge(i))
        content = 0.
        error_squared = 0.
        relative_uncertainty = 100000.

new_binning = list(reversed(lower_bin_edges))

print "new binning"
print new_binning


root_file.Close()


    
