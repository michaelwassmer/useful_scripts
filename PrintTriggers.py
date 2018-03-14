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
#label = 'TriggerResults::HLT'
#label = 'TriggerResults::RECO'
label =	'TriggerResults::PAT'
k=0
for event in events:
    if k>0:
        break
    event.getByLabel(label, triggerResultsHandle)
    triggerResults = triggerResultsHandle.product()
    triggerNames = event.object().triggerNames(triggerResults)
    for i in range(triggerResults.size()):
        #if not "MET" in triggerNames.triggerName(i):
            #continue
        print '#{0:03}   {2:5}   {1}'.format(
            i, triggerNames.triggerName(i), str(triggerResults.accept(i))
            )
    k+=1
