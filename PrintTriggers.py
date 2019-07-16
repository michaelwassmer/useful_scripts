# this script print the trigger paths / filters of a MINIAOD file you give as an argument
# trigger paths if you use TriggerResults::HLT
# filters if you use TriggerResults::RECO for data or TriggerResults::PAT for mc
import ROOT
import sys
from DataFormats import FWLite
ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.FWLiteEnabler.enable()
ROOT.gSystem.Load('libDataFormatsFWLite.so')
events = FWLite.Events(sys.argv[1])
triggerResultsHandle = FWLite.Handle('edm::TriggerResults')
label = 'TriggerResults::HLT'
#label = 'TriggerResults::RECO'
#label =	'TriggerResults::PAT'
triggerObjects, triggerObjectLabel  = FWLite.Handle("std::vector<pat::TriggerObjectStandAlone>"), "selectedPatTrigger"
k=0
for event in events:
    if k>0:
        break
    event.getByLabel(label, triggerResultsHandle)
    event.getByLabel(triggerObjectLabel, triggerObjects)
    triggerResults = triggerResultsHandle.product()
    triggerNames = event.object().triggerNames(triggerResults)
    for i in range(triggerResults.size()):
        #if not "MET" in triggerNames.triggerName(i):
            #continue
        print '#{0:03}   {2:5}   {1}'.format(
            i, triggerNames.triggerName(i), str(triggerResults.accept(i))
            )
    #for j,to in enumerate(triggerObjects.product()):
        #print j
        #print to
        #to.unpackPathNames(triggerNames)
        #print "Trigger object pt %6.2f eta %+5.3f phi %+5.3f  " % (to.pt(),to.eta(),to.phi())
        #print "         collection: ", to.collection()
        #print "         type ids: ", ", ".join([str(f) for f in to.filterIds()])
        #print "         filters: ", ", ".join([str(f) for f in to.filterLabels()])
        #pathslast = set(to.pathNames(True))
        #print "         paths:   ", ", ".join([("%s*" if f in pathslast else "%s")%f for f in to.pathNames()])
        #print to.triggerObject().pdgId()
    k+=1
