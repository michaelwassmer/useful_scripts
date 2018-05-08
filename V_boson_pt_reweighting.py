import ROOT
import sys
from array import array
from DataFormats.FWLite import Events, Handle
from math import *

events = Events (sys.argv[2:])

handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
eventinfo = Handle('GenEventInfoProduct')
labelPruned = "prunedGenParticles"
labelPacked = "packedGenParticles"
labelWeight = "generator"

binning = [30,40,50,60,70,80,90,100,110,120,130,140,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1600,1800,2000,2200,2400,2600,2800,3000,6500]
v_boson_pt = ROOT.TH1D("z_boson_pt","z_boson_pt",len(binning)-1,array('d',binning))
file_ = ROOT.TFile("z_boson_pt_"+str(sys.argv[1])+".root","RECREATE")
# loop over events
count= 0
for event in events:
    if count % 10000 == 0:
        print count
    #if count>10000:
        #break
    #print "----------------------------------------------------------------"
    event.getByLabel (labelPacked, handlePacked)
    event.getByLabel (labelPruned, handlePruned)
    event.getByLabel (labelWeight, eventinfo)
    # get the product
    packed = handlePacked.product()
    pruned = handlePruned.product()
    weight = eventinfo.product().weight()
    decay_prods = []
    for p in pruned:
        if p.pdgId()!=23:
            continue
        #print "found Z boson"
        for i in range(p.numberOfDaughters()):
            daughter = p.daughter(i)
            if daughter.status()!=1:
                #print "not stable"
                continue
            if not (abs(daughter.pdgId())==12 or abs(daughter.pdgId())==14 or abs(daughter.pdgId())==16):
                #print "no neutrino"
                continue
            #print "found neutrino"
            decay_prods.append(daughter.p4())
    if len(decay_prods)!=2:
        continue
    z_boson = decay_prods[0]+decay_prods[1]
    z_boson_pt = z_boson.pt()
    #print z_boson_pt,weight
    v_boson_pt.Fill(z_boson_pt,weight)
    count+=1
    
file_.WriteTObject(v_boson_pt)
file_.Close()
    
                
