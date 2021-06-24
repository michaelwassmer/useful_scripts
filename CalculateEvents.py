# this script counts the weighted sum of all events in the files given as a argument to the script
import ROOT
import sys
from DataFormats import FWLite
ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.FWLiteEnabler.enable()
ROOT.gSystem.Load('libDataFormatsFWLite.so')

file_names = open(sys.argv[1]).readlines()
file_names_ = []
for file_name in file_names:
    #file_names_.append(file_name.rstrip('\n'))
    file_names_.append("root://cmsxrootd.fnal.gov//"+file_name.rstrip('\n'))
#print file_names_[1:10]

def Count():
    #events = FWLite.Events(sys.argv[1:])
    #events = FWLite.Events(file_names_[1:100])
    geninfo = FWLite.Handle('GenEventInfoProduct')
    lheinfo = FWLite.Handle('LHEEventProduct')
    label_gen =	'generator'
    #label_lhe = 'externalLHEProducer'
    label_lhe = 'externalLHEProducer'
    weight_sum_gen = 0
    weight_sum_lhe = 0
    event_sum = 0
    neg_sum = 0
    for file_name in file_names_:
        if event_sum > 1000000:
            break
        events = None
        try:
            events = FWLite.Events(file_name)
            for event in events:
                if event_sum % 1000 == 0:
                    print event_sum
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
                #if event_sum % 10000 == 0:
                    #print event_sum
        except TypeError:
            continue
        
    print "GEN: sum of event weights / number of events ",weight_sum_gen*1.0/event_sum
    print "LHE: sum of event weights / number of events ",weight_sum_lhe*1.0/event_sum
    print "#neg./#all. ",neg_sum*1.0/event_sum
    print "#pos-#neg/#pos+#neg ",(event_sum-2*neg_sum)*1.0/(event_sum)
    print "sum of all weighted events: ",weight_sum_gen

def main():
    Count()
    
if __name__== "__main__":
    main()
