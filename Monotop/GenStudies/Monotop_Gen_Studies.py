from __future__ import print_function
from optparse import OptionParser
from math import *

usage = "Usage: %prog [options] input_file.root\n"
parser = OptionParser(usage=usage)
parser.add_option("--files",action="store_true", dest="files", help="flag to tell the script that it should loop over local files", default=False)
parser.add_option("--maxevents", action="store", dest="maxevents", help="maximum number of events to loop over", default="10000")
parser.add_option("--txtfile",action="store_true", dest="txtfile", help="flat to tell the script whether a txt file with the desired files is given", default=False)

(options, args) = parser.parse_args()

import ROOT
from DataFormats.FWLite import Events, Handle
import Utilities.General.cmssw_das_client as das_client

ROOT.gStyle.SetOptStat(0)

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
    dataset_name = dataset_name.replace("-","_")
    index_1 = dataset_name.find("Mphi_")
    index_2 = dataset_name.find("Mchi_")
    #print(index_1,index_2)
    number_1 = ""
    number_2 = ""
    for char in dataset_name[index_1+5:]:
        #print(char)
        if not char.isdigit(): break
        number_1+=char
    for char in dataset_name[index_2+5:]:
        #print(char)
        if not char.isdigit(): break
        number_2+=char
    print("Mphi="+number_1+" Mchi="+number_2)
    return number_1,number_2



max_events = int(options.maxevents)

files = []
mphi,mchi = find_masses(args[0])

if not options.files:
    sample_das_string = args[0]
    file_info = get_files(sample_das_string)
    n_events = 0
    for i in range(len(file_info)):
        if n_events < max_events:
            files.append(str(file_info[i][0]))
            n_events+=file_info[i][1]

else:
    n_events = 0
    files_all = None
    if not options.txtfile:
        files_all = args
    else:
        with open(args[0], "r") as txtfile:
            lines = txtfile.readlines()
            files_all = [line.rstrip('\n') for line in lines]
            #print(files_all)
    for file in files_all:
        print("file: ",file)
        if n_events < max_events:
            files.append(str(file))
            root_file=ROOT.TFile.Open(str(file),"READ")
            n_events+=root_file.Get("Events").GetEntries()
            root_file.Close()

print(files)
print(n_events)

# product labels and handles
handlePruned = Handle("std::vector<reco::GenParticle>")
handlePacked = Handle("std::vector<pat::PackedGenParticle>")
eventinfo = Handle("GenEventInfoProduct")
#lheinfo = Handle("LHEEventProduct")
handleGenJets = Handle("std::vector<reco::GenJet>")

labelPruned = "prunedGenParticles"
labelPacked = "packedGenParticles"
labelWeight = "generator"
#labelLHE = "externalLHEProducer"
labelGenJets = "slimmedGenJets"

top_pt = ROOT.TH1F("Top_Pt"+"_Mphi_"+mphi+"_Mchi_"+mchi,"Vector Monotop M_{#phi}="+mphi+" M_{#chi}="+mchi,20,0,2000)
top_pt.GetXaxis().SetTitle("Top Quark/Antiquark p_{T}[GeV]")

dm_pt = ROOT.TH1F("DM_Pt"+"_Mphi_"+mphi+"_Mchi_"+mchi,"Vector Monotop M_{#phi}="+mphi+" M_{#chi}="+mchi,20,0,2000)
dm_pt.GetXaxis().SetTitle("Dark Matter p_{T}[GeV]")

med_pt = ROOT.TH1F("Med_Pt"+"_Mphi_"+mphi+"_Mchi_"+mchi,"Vector Monotop M_{#phi}="+mphi+" M_{#chi}="+mchi,20,0,2000)
med_pt.GetXaxis().SetTitle("Vector Mediator p_{T}[GeV]")

dr_max_b_q_qbar = ROOT.TH1F("Max_DeltaR_b_q_qbar"+"_Mphi_"+mphi+"_Mchi_"+mchi,"Vector Monotop M_{#phi}="+mphi+" M_{#chi}="+mchi,20,0,6)
dr_max_b_q_qbar.GetXaxis().SetTitle("Maximum #Delta R(b/#bar{b},q,#bar{q'})")

dr_max_b_q_qbar_top_pt = ROOT.TH2F("Max_DeltaR_b_q_qbar_Top_Pt","",20,0,2000,20,0,6)
dr_max_b_q_qbar_top_pt.GetXaxis().SetTitle("Top Quark/Antiquark p_{T}[GeV]")
dr_max_b_q_qbar_top_pt.GetYaxis().SetTitle("Maximum #Delta R(b/#bar{b},q,#bar{q'})")
dr_max_b_q_qbar_top_pt.GetZaxis().SetTitle("Arbitrary units")

m_w_sm = ROOT.TH1F("M_W_SM","",20,0,100)
m_w_sm.GetXaxis().SetTitle("m_{T}[GeV]")
m_w_dm = ROOT.TH1F("M_W_DM"+"_Mphi_"+mphi+"_Mchi_"+mchi,"Vector Monotop M_{#phi}="+mphi+" M_{#chi}="+mchi,20,0,400)
m_w_dm.GetXaxis().SetTitle("m_{T}[GeV]")

genjet_pt = ROOT.TH1F("Jet_Pt"+"_Mphi_"+mphi+"_Mchi_"+mchi,"Vector Monotop M_{#phi}="+mphi+" M_{#chi}="+mchi,20,0,1000)
genjet_pt.GetXaxis().SetTitle("GenJet p_{T}[GeV]")

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
        #event.getByLabel(labelLHE, lheinfo)
        event.getByLabel(labelGenJets, handleGenJets)
        # get the products (prunedGenParticles collection, GenEventInfoProduct and LHEEventProduct)
        pruned = handlePruned.product()
        weight = eventinfo.product().weight()
        #lhe_weight = lheinfo.product().originalXWGTUP()
        genjets = handleGenJets.product()
        
        everything_found = False
        top_p4 = None
        top_found = False
        dm_1_p4 = None
        dm_2_p4 = None
        dm_1_found = False
        dm_2_found = False
        med_p4 = None
        b_p4 = None
        q_p4 = None
        qbar_p4 = None
        b_found = False
        q_found = False
        qbar_found = False
        lepton_p4 = None
        lepton_found = False
        neutrino_p4 = None
        neutrino_found = False
        
        for p in pruned:
            #print (p.pdgId())
            if everything_found: break
            if abs(p.pdgId())==6 and p.isHardProcess():
                top_found = True
                top_p4 = p.p4()
            if p.pdgId()==5000521 and p.isPromptFinalState():
                dm_1_found = True
                dm_1_p4 = p.p4()
            if p.pdgId()==-5000521 and p.isPromptFinalState():
                dm_2_found = True
                dm_2_p4 = p.p4()
            if abs(p.pdgId())==5 and p.isHardProcess() and abs(p.mother(0).pdgId())==6:
                b_found = True
                b_p4 = p.p4()
            if (p.pdgId()==1 or p.pdgId()==2 or p.pdgId()==3 or p.pdgId()==4) and p.isHardProcess() and abs(p.mother(0).pdgId())==24:
                q_found = True
                q_p4 = p.p4()
            if (p.pdgId()==-1 or p.pdgId()==-2 or p.pdgId()==-3 or p.pdgId()==-4) and p.isHardProcess() and abs(p.mother(0).pdgId())==24:
                qbar_found = True
                qbar_p4 = p.p4()
            if (abs(p.pdgId()==11) or abs(p.pdgId())==13 or abs(p.pdgId())==15) and p.isHardProcess() and abs(p.mother(0).pdgId())==24:
                lepton_found = True
                lepton_p4 = p.p4()
            if (abs(p.pdgId()==12) or abs(p.pdgId())==14 or abs(p.pdgId())==16) and p.isHardProcess() and abs(p.mother(0).pdgId())==24:
                neutrino_found = True
                neutrino_p4 = p.p4()
            
            
            everything_found = top_found and dm_1_found and dm_2_found and b_found and ((q_found and qbar_found) or (lepton_found and neutrino_found))
        
        
        top_pt.Fill(top_p4.pt(),weight)
        if b_found and q_found and qbar_found:
            dR_b_q = sqrt(ROOT.Math.VectorUtil.DeltaR2(b_p4, q_p4))
            dR_b_qbar = sqrt(ROOT.Math.VectorUtil.DeltaR2(b_p4, qbar_p4))
            dR_q_qbar = sqrt(ROOT.Math.VectorUtil.DeltaR2(q_p4, qbar_p4))
            max_dr = max(dR_b_q,dR_b_qbar,dR_q_qbar)
            dr_max_b_q_qbar.Fill(max_dr,weight)
            dr_max_b_q_qbar_top_pt.Fill(top_p4.pt(),max_dr,weight)
        if b_found and lepton_found and neutrino_found:
            met_p4 = (dm_1_p4+dm_2_p4)+neutrino_p4
            m_w_neutrino = ROOT.TMath.Sqrt(2.*lepton_p4.pt()*neutrino_p4.pt()*(1-ROOT.TMath.Cos(ROOT.TVector2.Phi_mpi_pi(lepton_p4.phi()-neutrino_p4.phi()))))
            m_w_met = ROOT.TMath.Sqrt(2.*lepton_p4.pt()*met_p4.pt()*(1-ROOT.TMath.Cos(ROOT.TVector2.Phi_mpi_pi(lepton_p4.phi()-met_p4.phi()))))
            m_w_sm.Fill(m_w_neutrino,weight)
            m_w_dm.Fill(m_w_met,weight)
        dm_pt.Fill(dm_1_p4.pt(),weight)
        dm_pt.Fill(dm_2_p4.pt(),weight)
        med_pt.Fill((dm_1_p4+dm_2_p4).pt(),weight)
        
        for genjet in genjets:
            genjet_pt.Fill(genjet.pt(),weight)

top_pt.Scale(1./top_pt.Integral())
#top_pt.Draw("hist")
#raw_input("bla")
dm_pt.Scale(1./dm_pt.Integral())
#dm_pt.Draw("hist")
#raw_input("bla")
med_pt.Scale(1./med_pt.Integral())
dr_max_b_q_qbar.Scale(1./dr_max_b_q_qbar.Integral())
dr_max_b_q_qbar_top_pt.Scale(1./dr_max_b_q_qbar_top_pt.Integral())
m_w_sm.Scale(1./m_w_sm.Integral())
m_w_dm.Scale(1./m_w_dm.Integral())
genjet_pt.Scale(1./genjet_pt.Integral())

output_file = ROOT.TFile.Open("GenStudies_"+"Mphi_"+mphi+"_Mchi_"+mchi+".root","RECREATE")
output_file.WriteTObject(top_pt)
output_file.WriteTObject(dm_pt)
output_file.WriteTObject(med_pt)
output_file.WriteTObject(dr_max_b_q_qbar)
output_file.WriteTObject(dr_max_b_q_qbar_top_pt)
output_file.WriteTObject(m_w_sm)
output_file.WriteTObject(m_w_dm)
output_file.WriteTObject(genjet_pt)
output_file.Close()
