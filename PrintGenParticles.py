# import ROOT package functionalities
import ROOT
# import sys package functionalities
import sys
# import needed FrameworkLite objects
from DataFormats.FWLite import Events, Handle
# import math package functionalities
from math import *

# function to find out whether a is an ancestor of p
def isAncestor(a,p) :
        if a == p :
                return True
        for i in xrange(0,p.numberOfMothers()) :
                if isAncestor(a,p.mother(i)) :
                         return True
        return False

# function to find all mother particles of particle
def FindAllMothers(particle):
    mother_ids = []
    #print("particle id ",particle.pdgId())
    #print("# mothers ",particle.numberOfMothers())
    for i in range(particle.numberOfMothers()):
        #print("mother id ",particle.mother(i).pdgId())
        mother_ids.append(particle.mother(i).pdgId())
        next_mothers_ids = FindAllMothers(particle.mother(i))
        for next_mother_id in next_mothers_ids:
            mother_ids.append(next_mother_id)
    return mother_ids

input_files = sys.argv[1:]
events = Events (input_files)

# container for pruned generator particles
handlePruned  = Handle ("std::vector<reco::GenParticle>")
# container for packed generator particles
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
# label to retrieve pruned generator particles
labelPruned = ("prunedGenParticles")
# label to retrieve packed generator particles
labelPacked = ("packedGenParticles")

# loop over events
for counter,event in enumerate(events):
    if counter > 0:
        break
    print("----------------------------------------------------------------")
    # retrieve packed generator particles and put them into the container defined above
    event.getByLabel (labelPacked, handlePacked)
    # retrieve pruned generator particles and put them into the container defined above
    event.getByLabel (labelPruned, handlePruned)
    # get the packed generator particle container (to not have to work with pointers)
    packed = handlePacked.product()
    # get the pruned generator particle container (to not have to work with pointers)
    pruned = handlePruned.product()

    # loop over pruned generator particles
    for p in pruned :
        print("PdgId : {}   pt : {:.2f}  eta : {:.2f}   phi : {:.2f}   m : {:.2f} e: {:.2f} px: {:.2f} py: {:.2f} pz: {:.2f} status: {}".format(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mass(),p.energy(),p.px(),p.py(),p.pz(),p.status()))
        #mothers = FindAllMothers(p)
        #print("mothers")
        #print(mothers)
        #print("daughters")
        #for pa in packed:
            #mother = pa.mother(0)
            #if mother and isAncestor(p,mother) :
                #print("     PdgId : %s   pt : %s  eta : %s   phi : %s m : %s e: %s px: %s py: %s pz: %s" %(pa.pdgId(),pa.pt(),pa.eta(),pa.phi(),pa.mass(),pa.energy(),pa.px(),pa.py(),pa.pz()))
