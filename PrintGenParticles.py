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

events = Events (['file:///nfs/dust/cms/user/mwassmer/DarkMatter/testfile/0CB860A0-35C7-E611-BE26-549F35AF44E3.root'])

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
                #print "     daughters"
                #for pa in packed:
                        #mother = pa.mother(0)
                        #if mother and isAncestor(p,mother) :
                              #print "     PdgId : %s   pt : %s  eta : %s   phi : %s m : %s e: %s px: %s py: %s pz: %s" %(pa.pdgId(),pa.pt(),pa.eta(),pa.phi(),pa.mass(),pa.energy(),pa.px(),pa.py(),pa.pz())
