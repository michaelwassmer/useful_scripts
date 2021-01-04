import sys
import ROOT
import math

input_file = sys.argv[1]
input_template = sys.argv[2]
acceptable_uncertainty = float(sys.argv[3])

root_file = ROOT.TFile.Open(input_file,"READ")

histogram = root_file.Get(input_template).Clone()

print "Historam has ",histogram.GetEntries()," entries"

relative_uncertainty = 100000.0
content = 0.0
error_squared = 0.0
lower_bin_edges = []
content_before = histogram.GetBinContent(histogram.GetNbinsX()+1)
relative_uncertainty_before = 100000.0

for i in range(histogram.GetNbinsX(),0,-1):
    if relative_uncertainty > acceptable_uncertainty or \
       content < content_before or \
       relative_uncertainty > relative_uncertainty_before:
        content += histogram.GetBinContent(i)
        error_squared += math.pow(histogram.GetBinError(i),2)
        try:
            relative_uncertainty = math.sqrt(error_squared)*1.0/content
        except ZeroDivisionError:
            relative_uncertainty = 100000.
        print "--------------------------------------------------------------"
        print "currently at bin ",i
        print "content: ",content
        print "error squared: ",error_squared
        print "relative uncertainty: ",relative_uncertainty
        print "content before: ",content_before
        print "relative uncertainty before: ",relative_uncertainty_before
    else:
        lower_bin_edges.append(histogram.GetBinLowEdge(i))
        content_before = content
        relative_uncertainty_before = relative_uncertainty
        content = 0.0
        error_squared = 0.0
        relative_uncertainty = 100000.

new_binning = list(reversed(lower_bin_edges))

print "new binning"
print new_binning
print "number of bins ",len(new_binning)-1

lowest_bin_edge = histogram.GetBinLowEdge(1)
adapted_binning = []

if lowest_bin_edge < new_binning[0]:
    difference = new_binning[0]-lowest_bin_edge
    adapted_binning = [x-difference for x in new_binning]


print "adapted binning"
print adapted_binning
print "number of bins ",len(adapted_binning)-1

edge_before = lowest_bin_edge
edge_difference_before = 0.0
final_binning = []

for i in range(len(adapted_binning)):
    edge_difference = adapted_binning[i] - edge_before
    if edge_difference < edge_difference_before:
        shift = edge_difference_before - edge_difference
        adapted_binning[i]=adapted_binning[i]+shift
    edge_difference_before = adapted_binning[i]-edge_before
    edge_before = adapted_binning[i]

print "final binning"
print adapted_binning
print "number of bins ",len(adapted_binning)-1

root_file.Close()


    
