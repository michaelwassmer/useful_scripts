# this script print the trigger paths / filters of a MINIAOD file you give as an argument
# trigger paths if you use TriggerResults::HLT
# filters if you use TriggerResults::RECO for data or TriggerResults::PAT for mc
import ROOT
import sys
from DataFormats import FWLite
ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.FWLiteEnabler.enable()
ROOT.gSystem.Load('libDataFormatsFWLite.so')
events = FWLite.Events(sys.argv[1:])
geninfo = FWLite.Handle('GenEventInfoProduct')
lheinfo = FWLite.Handle('LHEEventProduct')
#label = 'TriggerResults::HLT'
#label = 'TriggerResults::RECO'
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
    print event_sum
    
print "GEN: ",weight_sum_gen/event_sum
print "LHE: ",weight_sum_lhe/event_sum
print "#neg./#all. ",neg_sum*1.0/event_sum
print "#pos-#neg/#pos+#neg ",(event_sum-2*neg_sum)*1.0/(event_sum)
print "sum of all weighted events: ",weight_sum_gen
