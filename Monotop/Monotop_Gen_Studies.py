from __future__ import print_function
import ROOT
import sys
from array import array
from DataFormats.FWLite import Events, Handle
from math import *
import Utilities.General.cmssw_das_client as das_client

ROOT.gStyle.SetOptStat(0)
# ROOT.gSystem.Load('libGenVector')

file_prefix = "root://xrootd-cms.infn.it//"

# not needed at the moment
def FindAllMothers(particle):
    mother_ids = []
    print ("particle id ", particle.pdgId())
    print ("# mothers ", particle.numberOfMothers())
    for i in range(particle.numberOfMothers()):
        print ("mother id ", particle.mother(i).pdgId())
        mother_ids.append(particle.mother(i).pdgId())
        next_mothers_ids = FindAllMothers(particle.mother(i))
        for next_mother_id in next_mothers_ids:
            mother_ids.append(next_mother_id)
    return mother_ids

def get_files(dataset_name):
    print (dataset_name)
    files = []
    data = das_client.get_data("file dataset=" + dataset_name + " instance=prod/global")
    for d in data.get("data", None):
        # print(d)
        for f in d.get("file", None):
            # print(f)
            # if not 'nevents' in f:
            # continue
            files.append(
                [file_prefix + f.get("name", None), f.get("nevents", None)]
            )
    return files
    
def find_masses(dataset_name):
    index_1 = dataset_name.find("Mphi")
    index_2 = dataset_name.find("_13TeV")
    substring = dataset_name[index_1:index_2]
    substring = substring.replace("-","_")
    string_array = substring.split("_")
    print(string_array)
    return string_array[1],string_array[3]

# inputs
#postfix = str(sys.argv[3])

sample_das_string = str(sys.argv[1])

max_events = int(sys.argv[2])

mphi,mchi = find_masses(sample_das_string)

file_info = get_files(sample_das_string)

files = []
n_events = 0
for i in range(len(file_info)):
    if n_events < max_events:
        files.append(str(file_info[i][0]))
        n_events+=file_info[i][1]

print(files)
print(n_events)

# product labels and handles
handlePruned = Handle("std::vector<reco::GenParticle>")
handlePacked = Handle("std::vector<pat::PackedGenParticle>")
eventinfo = Handle("GenEventInfoProduct")
lheinfo = Handle("LHEEventProduct")
labelPruned = "prunedGenParticles"
labelPacked = "packedGenParticles"
labelWeight = "generator"
labelLHE = "externalLHEProducer"

top_pt = ROOT.TH1F("Top_Pt","Vector Monotop M_{#phi}="+mphi+" M_{#chi}="+mchi,20,0,1000)
top_pt.GetXaxis().SetTitle("Top Quark/Antiquark p_{T}")

dm_pt = ROOT.TH1F("DM_Pt","Vector Monotop M_{#phi}="+mphi+" M_{#chi}="+mchi,20,0,1000)
dm_pt.GetXaxis().SetTitle("Dark Matter p_{T}")

count = 0
# loop over files
for filename in files:
    # loop over events in file
    events = Events(filename)
    for event in events:
        count += 1
        if count % 1000 == 0:
            print (count)
        event.getByLabel(labelPruned, handlePruned)
        event.getByLabel(labelWeight, eventinfo)
        event.getByLabel(labelLHE, lheinfo)
        # get the products (prunedGenParticles collection, GenEventInfoProduct and LHEEventProduct)
        pruned = handlePruned.product()
        weight = eventinfo.product().weight()
        lhe_weight = lheinfo.product().originalXWGTUP()
        
        everything_found = False
        top_p4 = None
        top_found = False
        dm_1_p4 = None
        dm_2_p4 = None
        dm_1_found = False
        dm_2_found = False
        
        for p in pruned:
            #print (p.pdgId())
            if everything_found: break
            if abs(p.pdgId())==6 and p.isHardProcess():
                top_found = True
                top_p4 = p.p4()
            if p.pdgId()==18 and p.isPromptFinalState():
                dm_1_found = True
                dm_1_p4 = p.p4()
            if p.pdgId()==-18 and p.isPromptFinalState():
                dm_2_found = True
                dm_2_p4 = p.p4()
            
            everything_found = top_found and dm_1_found and dm_2_found
        
        
        top_pt.Fill(top_p4.pt(),weight)
        dm_pt.Fill(dm_1_p4.pt(),weight)
        dm_pt.Fill(dm_2_p4.pt(),weight)

top_pt.Scale(1./top_pt.Integral())
#top_pt.Draw("hist")
#raw_input("bla")
dm_pt.Scale(1./dm_pt.Integral())
#dm_pt.Draw("hist")
#raw_input("bla")

output_file = ROOT.TFile.Open("GenStudies_"+"Mphi_"+mphi+"_Mchi_"+mchi+".root","RECREATE")
output_file.WriteTObject(top_pt)
output_file.WriteTObject(dm_pt)
output_file.Close()
