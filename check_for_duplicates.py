import sys
import ROOT

treename="MVATree"

sample_directories=sys.argv[1:]
#print sample_directories

chain = ROOT.TChain(treename)
for i in range(len(sample_directories)):
    chain.Add(sample_directories[i])

event_id = []
run_id = []
lumi_id = []
#lep_pt = []

for evt in chain:
    event_id.append(evt.Evt_ID)
    run_id.append(evt.Evt_Run)
    lumi_id.append(evt.Evt_Lumi)
    #lep_pt.append(evt.lep_pt)
#print event_id
seen = set()
duplicates = []

for id_evt,id_run,id_lumi in zip(event_id,run_id,lumi_id):
    if (id_evt,id_run,id_lumi) in seen:
        duplicates.append([id_evt,id_run,id_lumi])
    seen.add((id_evt,id_run,id_lumi))    
        
if len(duplicates)>0:
    print "sample: ",[sample for sample in sample_directories], " has duplicates"        
    #print "# unique ids: ",len(uniq)
    #print "# all ids: ",len(event_id)
    print "duplicates: ",duplicates[:10]
else:
    print "no duplicates"
