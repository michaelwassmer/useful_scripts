import ROOT
import sys
from array import array
from DataFormats.FWLite import Events, Handle
from math import *
#ROOT.gSystem.Load('libGenVector')

#not needed at the moment
def FindAllMothers(particle):
    mother_ids = []
    print "particle id ",particle.pdgId()
    print "# mothers ",particle.numberOfMothers()
    for i in range(particle.numberOfMothers()):
        print "mother id ",particle.mother(i).pdgId()
        mother_ids.append(particle.mother(i).pdgId())
        next_mothers_ids = FindAllMothers(particle.mother(i))
        for next_mother_id in next_mothers_ids:
            mother_ids.append(next_mother_id)
    return mother_ids

# also use muR and muF variations
scales = {  #"nominal" : 1000,
            "Weight_scale_variation_muR_1p0_muF_1p0" : 1001,
            "Weight_scale_variation_muR_1p0_muF_2p0" : 1002,
            "Weight_scale_variation_muR_1p0_muF_0p5" : 1003,
            "Weight_scale_variation_muR_2p0_muF_1p0" : 1004,
            "Weight_scale_variation_muR_2p0_muF_2p0" : 1005,
            "Weight_scale_variation_muR_2p0_muF_0p5" : 1006,
            "Weight_scale_variation_muR_0p5_muF_1p0" : 1007,
            "Weight_scale_variation_muR_0p5_muF_2p0" : 1008,
            "Weight_scale_variation_muR_0p5_muF_0p5" : 1009
        }

# inputs
boson=str(sys.argv[1])
postfix=str(sys.argv[2])
filenames = sys.argv[3:]

# product labels and handles
handlePruned  = Handle ("std::vector<reco::GenParticle>")
#handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
eventinfo = Handle('GenEventInfoProduct')
lheinfo = Handle('LHEEventProduct')
labelPruned = "prunedGenParticles"
labelPacked = "packedGenParticles"
labelWeight = "generator"
labelLHE = "externalLHEProducer"

# binning according to https://arxiv.org/pdf/1705.04664.pdf
binning = [30,40,50,60,70,80,90,100,110,120,130,140,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1600,1800,2000,2200,2400,2600,2800,3000,6500]
v_boson_pt_hist = ROOT.TH1D(boson+"_boson_pt",boson+"_boson_pt",len(binning)-1,array('d',binning))
v_boson_pt_hist.Sumw2()
file_ = ROOT.TFile(boson+"_boson_pt_"+postfix+".root","RECREATE")

# list of histograms for scale variations
v_boson_pt_hists = {}
for scale in scales:
    v_boson_pt_hists[scale]=ROOT.TH1D(boson+"_boson_pt_"+scale,boson+"_boson_pt_"+scale,len(binning)-1,array('d',binning))
    v_boson_pt_hists[scale].Sumw2()

count= 0

# loop over files
for filename in filenames:
    # cross section weights
    weight_xs = 1.
    if boson=="Zvv":
        if "70to100" in filename.lower():
            weight_xs = 1.
        elif "100to200" in filename.lower():
            weight_xs = 3.034e+02
        elif "200to400" in filename.lower():
            weight_xs = 9.171e+01
        elif "400to600" in filename.lower():
            weight_xs = 1.310e+01
        elif "600to800" in filename.lower():
            weight_xs = 3.248e+00
        elif "800to1200" in filename.lower():
            weight_xs = 1.496e+00
        elif "1200to2500" in filename.lower():
            weight_xs = 3.425e-01
        elif "2500toInf" in filename.lower():
            weight_xs = 5.268e-03
        else:
            print "problem with xs weight"
            exit()
    elif boson=="Zll":
        if "70to100" in filename.lower():
            weight_xs = 1.467e+02
        elif "100to200" in filename.lower():
            weight_xs = 1.608e+02
        elif "200to400" in filename.lower():
            weight_xs = 4.863e+01
        elif "400to600" in filename.lower():
            weight_xs = 6.975e+00
        elif "600to800" in filename.lower():
            weight_xs = 1.756e+00
        elif "800to1200" in filename.lower():
            weight_xs = 8.099e-01
        elif "1200to2500" in filename.lower():
            weight_xs = 1.931e-01
        elif "2500toInf" in filename.lower():
            weight_xs = 3.513e-03
        else:
            print "problem with xs weight"
            exit()
    elif boson=="W":
        if "70to100" in filename.lower():
            weight_xs = 1.289e+03
        elif "100to200" in filename.lower():
            weight_xs = 1.392e+03
        elif "200to400" in filename.lower():
            weight_xs = 4.103e+02
        elif "400to600" in filename.lower():
            weight_xs = 5.785e+01
        elif "600to800" in filename.lower():
            weight_xs = 1.295e+01
        elif "800to1200" in filename.lower():
            weight_xs = 5.451e+00
        elif "1200to2500" in filename.lower():
            weight_xs = 1.084e+00
        elif "2500toInf" in filename.lower():
            weight_xs = 8.061e-03
        else:
            print "problem with xs weight"
            exit()
    else:
        print "only W or Z boson allowed"
        exit()
        
    print "weight_xs = ",weight_xs

    # loop over events
    events = Events (filename)
    for event in events:
        count+=1
        if count % 100 == 0:
            print count
        if count>1000:
            break
        #event.getByLabel (labelPacked, handlePacked)
        event.getByLabel (labelPruned, handlePruned)
        event.getByLabel (labelWeight, eventinfo)
        event.getByLabel (labelLHE , lheinfo)
        # get the product
        #packed = handlePacked.product()
        pruned = handlePruned.product()
        weight = eventinfo.product().weight()
        lhe_weight = lheinfo.product().originalXWGTUP()
        decay_prods = []
        radiated_photons = []
        for p in pruned:
            if boson=="Zvv":
                if not ((abs(p.pdgId())==12 or abs(p.pdgId())==14 or abs(p.pdgId())==16) and p.isPromptFinalState()):
                    #print "no neutrino"
                    continue
                #print "found neutrino"
                decay_prods.append(p)
            elif boson=="Zll":
                # need to save stable photons to calculate dressed leptons later
                if abs(p.pdgId())==22 and p.status()==1 and (not p.statusFlags().isPrompt()):
                    radiated_photons.append(p)
                    continue
                # check for prompt final state charged leptons
                if not ((abs(p.pdgId())==11 or abs(p.pdgId())==13) and p.isPromptFinalState()):# or abs(daughter.pdgId())==15 or abs(daughter.pdgId())==16 with taus
                    #print "no charged lepton"
                    continue
                #print "found charged lepton"
                decay_prods.append(p)
            elif boson=="W":
                # need to save stable photons to calculate dressed leptons later
                if abs(p.pdgId())==22 and p.status()==1 and (not p.statusFlags().isPrompt()):
                    radiated_photons.append(p)
                    continue
                # check for prompt final state charged leptons and neutrinos
                if not ((abs(p.pdgId())==11 or abs(p.pdgId())==12 or abs(p.pdgId())==13 or abs(p.pdgId())==14) and p.isPromptFinalState()):# or abs(daughter.pdgId())==15 or abs(daughter.pdgId())==16 with taus
                    #print "no neutrino/charged lepton"
                    continue
                #print "found neutrino/charged lepton"
                decay_prods.append(p)
            else:
                print "only W or Z boson allowed"
                exit()
        
        # fail-safe: check if the number of found daughters is exactly 2 as one would expect
        if len(decay_prods)!=2:
            #print "more than two decay prods ",len(decay_prods)
            continue
        
        if boson=="Zvv":
            # fail-safe: check if the daughters of the Z boson are particle and anti-particle as well as same lepton flavor
            if decay_prods[0].pdgId()+decay_prods[1].pdgId()!=0:
                continue
        
        elif boson=="Zll":
            # fail-safe: check if the daughters of the Z boson are particle and anti-particle as well as same lepton flavor
            if decay_prods[0].pdgId()+decay_prods[1].pdgId()!=0:
                continue
            # add radiated photons back to leptons
            for decay_prod in decay_prods:
                if abs(decay_prod.pdgId())==11 or abs(decay_prod.pdgId())==13:
                    for photon in radiated_photons:
                        if sqrt(ROOT.Math.VectorUtil.DeltaR2(decay_prod.p4(),photon.p4()))<0.1:
                            decay_prod.setP4(decay_prod.p4()+photon.p4())
        
        elif boson=="W":
            # fail-safe: check if the daughters of the W boson are particle and anti-particle as well as same lepton flavor
            if decay_prods[0].pdgId()*decay_prods[1].pdgId()>=0 or abs(abs(decay_prods[0].pdgId())-abs(decay_prods[1].pdgId()))!=1:
                #print "W conditions not satisfied "
                continue
            # add radiated photons back to lepton
            for decay_prod in decay_prods:
                if abs(decay_prod.pdgId())==11 or abs(decay_prod.pdgId())==13:
                    for photon in radiated_photons:
                        if sqrt(ROOT.Math.VectorUtil.DeltaR2(decay_prod.p4(),photon.p4()))<0.1:
                            decay_prod.setP4(decay_prod.p4()+photon.p4())
                    
        else:
            print "only W or Z boson allowed"
            exit()
        
        # reconstruct vector boson from the two decay products
        v_boson = decay_prods[0].p4()+decay_prods[1].p4()
        v_boson_pt = v_boson.pt()
        # fill the vector boson pt
        v_boson_pt_hist.Fill(v_boson_pt,weight*weight_xs/1000.)
        # fill histograms for scale variations
        for scale in scales:
            #print scale
            #print scales[scale]
            for i in range(lheinfo.product().weights().size()):
                #print lheinfo.product().weights().at(i).id
                if int(lheinfo.product().weights().at(i).id) == int(scales[scale]):
                    scale_weight = lheinfo.product().weights().at(i).wgt
                    #print scale_weight
                    v_boson_pt_hists[scale].Fill(v_boson_pt,weight*weight_xs/1000.*scale_weight/lhe_weight)
                    break

# write all to a file
file_.WriteTObject(v_boson_pt_hist)
for scale in scales:
    file_.WriteTObject(v_boson_pt_hists[scale])
file_.Close()
print "finished"    
                
