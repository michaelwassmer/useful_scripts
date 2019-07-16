import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

def isAncestor(a,p) :
        if a == p :
                return True
        for i in xrange(0,p.numberOfMothers()) :
                if isAncestor(a,p.mother(i)) :
                         return True
        return False

def FindAllMothers(particle):
    mother_ids = []
    #print "particle id ",particle.pdgId()
    #print "# mothers ",particle.numberOfMothers()
    for i in range(particle.numberOfMothers()):
        #print "mother id ",particle.mother(i).pdgId()
        mother_ids.append(particle.mother(i).pdgId())
        next_mothers_ids = FindAllMothers(particle.mother(i))
        for next_mother_id in next_mothers_ids:
            mother_ids.append(next_mother_id)
    return mother_ids

events = Events (sys.argv[1:])

handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")

# loop over events
count= 0
for event in events:
    print "----------------------------------------------------------------"
    event.getByLabel (labelPacked, handlePacked)
    event.getByLabel (labelPruned, handlePruned)
    # get the product
    packed = handlePacked.product()
    pruned = handlePruned.product()

    for p in pruned :
        print "PdgId : %s   pt : %s  eta : %s   phi : %s   m : %s e: %s px: %s py: %s pz: %s status: %s" %(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mass(),p.energy(),p.px(),p.py(),p.pz(),p.status())    
        #print "daughters"
        #mothers = FindAllMothers(p)
        #print mothers
        #if abs(p.pdgId())==5 and 6 not in mothers and -6 not in mothers:
            #print "!!!!!!!!!B QUARK NOT FROM TOP!!!!!!!!!!!!" 
            #print "mothers"
            #print mothers
            #print "PdgId : %s   pt : %s  eta : %s   phi : %s   m : %s e: %s px: %s py: %s pz: %s status: %s" %(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mass(),p.energy(),p.px(),p.py(),p.pz(),p.status())
        #for pa in packed:
            #mother = pa.mother(0)
            #if mother and isAncestor(p,mother) :
                #print "     PdgId : %s   pt : %s  eta : %s   phi : %s m : %s e: %s px: %s py: %s pz: %s" %(pa.pdgId(),pa.pt(),pa.eta(),pa.phi(),pa.mass(),pa.energy(),pa.px(),pa.py(),pa.pz())
