# this script counts the weighted sum of all events in the files given as a argument to the script
import ROOT
import sys
from DataFormats import FWLite
ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.FWLiteEnabler.enable()
ROOT.gSystem.Load('libDataFormatsFWLite.so')
events = FWLite.Events(sys.argv[1:])
geninfo = FWLite.Handle('GenEventInfoProduct')
lheinfo = FWLite.Handle('LHEEventProduct')
label_gen =	'generator'
label_lhe = 'externalLHEProducer'
weight_sum_gen = 0
weight_sum_lhe = 0
event_sum = 0
neg_sum = 0
for event in events:
    event.getByLabel(label_gen, geninfo)
    event.getByLabel(label_lhe, lheinfo)
    weight_gen = geninfo.product().weight()
    weight_lhe = lheinfo.product().originalXWGTUP()
    weight_sum_gen+=weight_gen
    weight_sum_lhe+=weight_lhe
    #print lheinfo.product().weights().at(0)
    event_sum+=1
    if weight_gen<0.:
        neg_sum+=1
    if event_sum % 10000 == 0:
        print event_sum
    
print "GEN: ",weight_sum_gen/event_sum
print "LHE: ",weight_sum_lhe/event_sum
print "#neg./#all. ",neg_sum*1.0/event_sum
print "#pos-#neg/#pos+#neg ",(event_sum-2*neg_sum)*1.0/(event_sum)
print "sum of all weighted events: ",weight_sum_gen
print "sum weighted events divided by sum unweighted events: ",weight_sum_gen*1.0/event_sum
