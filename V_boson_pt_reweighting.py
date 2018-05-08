import ROOT
import sys
from array import array
from DataFormats.FWLite import Events, Handle
from math import *

boson=str(sys.argv[1])
postfix=str(sys.argv[2])
filename = sys.argv[3]

events = Events (filename)

handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
eventinfo = Handle('GenEventInfoProduct')
labelPruned = "prunedGenParticles"
labelPacked = "packedGenParticles"
labelWeight = "generator"

binning = [30,40,50,60,70,80,90,100,110,120,130,140,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1600,1800,2000,2200,2400,2600,2800,3000,6500]
v_boson_pt_hist = ROOT.TH1D(boson+"_boson_pt",boson+"_boson_pt",len(binning)-1,array('d',binning))
file_ = ROOT.TFile(boson+"_boson_pt_"+postfix+".root","RECREATE")

weight_xs = 1.
if boson=="Z":
    if "50To100" in filename:
        weight_xs = 3*0.971*0.0000173748656012
    elif "100To250" in filename:
        weight_xs = 3*0.971*0.00000638503945658
    elif "250To400" in filename:
        weight_xs = 3*0.971*0.0000184890023189
    elif "400To650" in filename:
        weight_xs = 3*0.971*0.000203629482553
    elif "650ToInf" in filename:
        weight_xs = 3*0.971*0.000208821846317
    else:
        print "problem with xs weight"
        exit()
elif boson=="W":
    if "100To250" in filename:
        weight_xs = 0.00000385148734634
    elif "250To400" in filename:
        weight_xs = 0.0000396029149925
    elif "400To600" in filename:
        weight_xs = 0.000265993494557
    elif "600ToInf" in filename:
        weight_xs = 0.000255801929068
    else:
        print "problem with xs weight"
        exit()
else:
    print "only W or Z boson allowed"
    exit()
    
print "weight_xs = ",weight_xs

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
        if boson=="Z":
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
        elif boson=="W":
            print "not yet implemented"
            exit()
        else:
            print "only W or Z boson allowed"
            exit()
    if len(decay_prods)!=2:
        print "v boson could not be determined"
        continue
    v_boson = decay_prods[0]+decay_prods[1]
    v_boson_pt = v_boson.pt()
    #print z_boson_pt,weight
    v_boson_pt_hist.Fill(v_boson_pt,weight*weight_xs/1000.)
    count+=1
    
file_.WriteTObject(v_boson_pt_hist)
file_.Close()
    
                
