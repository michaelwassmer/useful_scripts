from __future__ import print_function
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-R", action="store_true", dest="readids", default=False)
parser.add_option("-W", action="store_true", dest="writeids", default=False)
parser.add_option("--readIDFile",action="store",dest="readIDFile", default="")
parser.add_option("--writeIDFile",action="store",dest="writeIDFile", default="")
parser.add_option("--templateFile",action="store",dest="templateFile", default="")

(options, args) = parser.parse_args()

if options.readids == options.writeids:
    print("either --readids or --writeids must be set, but not both")
    exit()
if options.readids and options.readIDFile=="":
    print("readids option requires readIDFile")
    exit()
if options.writeids and options.writeIDFile=="":
    print("writeids option requires writeIDFile")
    exit()
if options.templateFile == "":
    print("template output file name required")
    exit()

import ROOT
import sys

from DataFormats import FWLite

ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.FWLiteEnabler.enable()
ROOT.gSystem.Load('libDataFormatsFWLite.so')
ROOT.gROOT.SetBatch(True)

def FillVectorPtEta(vector,hist_pt,hist_eta,ptmin=-1.,etamax=999.):
    for element in vector:
        if element.pt() > ptmin and abs(element.eta()) < etamax:
            hist_pt.Fill(element.pt())
            hist_eta.Fill(element.eta())


files = args
#print(files)

events = FWLite.Events(files)

#eventinfo_handle = FWLite.Handle("edm::EventAuxiliary")
pfmet_handle = FWLite.Handle("std::vector<pat::MET")
puppimet_handle = FWLite.Handle("std::vector<pat::MET")
ak15jet_handle = FWLite.Handle("std::vector<pat::Jet>")
ak4jet_handle = FWLite.Handle("std::vector<pat::Jet>")
ak4puppijet_handle = FWLite.Handle("std::vector<pat::Jet>")
electron_handle = FWLite.Handle("std::vector<pat::Electron>")
muon_handle = FWLite.Handle("std::vector<pat::Muon>")
photon_handle = FWLite.Handle("std::vector<pat::Photon>")

#eventinfo_label = "EventAuxiliary"
pfmet_label = "slimmedMETs::SKIM"
puppimet_label = "slimmedMETsPuppi::SKIM"
ak15jet_label = "AK15PFPuppiComplete"
ak4jet_label = "selectedPatJetsAK4PFCHS::SKIM"
ak4puppijet_label = "selectedPatJetsAK4PFPuppi::SKIM"
electron_label = "slimmedElectrons::SKIM"
muon_label = "slimmedMuons::RECO"
photon_label = "slimmedPhotons::SKIM"

pfmet_pt_hist = ROOT.TH1D("PFMET_pt","PFMET pt",50,0,1000)
pfmet_phi_hist = ROOT.TH1D("PFMET_phi","PFMET phi",64,-3.2,3.2)
puppimet_pt_hist = ROOT.TH1D("PUPPIMET_pt","PUPPIMET pt",50,0,1000)
puppimet_phi_hist = ROOT.TH1D("PUPPIMET_phi","PUPPIMET phi",64,-3.2,3.2)
ak15jet_pt_hist = ROOT.TH1D("AK15Jet_pt","AK15Jet pt",50,0,1000)
ak15jet_eta_hist = ROOT.TH1D("AK15Jet_eta","AK15Jet eta",48,-2.4,2.4)
ak4jet_pt_hist = ROOT.TH1D("AK4Jet_pt","AK4Jet pt",50,0,1000)
ak4jet_eta_hist = ROOT.TH1D("AK4Jet_eta","AK4Jet eta",48,-2.4,2.4)
ak4puppijet_pt_hist = ROOT.TH1D("AK4PUPPIJet_pt","AK4PUPPUJet pt",50,0,1000)
ak4puppijet_eta_hist = ROOT.TH1D("AK4PUPPIJet_eta","AK4PUPPIJet eta",48,-2.4,2.4)
electron_pt_hist = ROOT.TH1D("Electron_pt","Electron pt",50,0,500)
electron_eta_hist = ROOT.TH1D("Electron_eta","Electron eta",50,-2.5,2.5)
muon_pt_hist = ROOT.TH1D("Muon_pt","Muon pt",50,0,500)
muon_eta_hist = ROOT.TH1D("Muon_eta","Muon eta",50,-2.5,2.5)
photon_pt_hist = ROOT.TH1D("Photon_pt","Photon pt",50,0,500)
photon_eta_hist = ROOT.TH1D("Photon_eta","Photon eta",50,-2.5,2.5)

ids = set()
if options.readIDFile:
    with open(options.readIDFile, 'r') as fp:
        for line in fp:
            #print(line)
            line_as_list = line.replace("\n","").split(",")
            run = int(line_as_list[0])
            lumi = int(line_as_list[1])
            eventid = int(line_as_list[2])
            if (run,lumi,eventid) in ids:
                print("duplicate !!! this should never happen !!!")
                exit()
            else:
                ids.add((run,lumi,eventid))

for number,event in enumerate(events):
    if number % 10000 == 0:
        print(number)
    run = event.eventAuxiliary().run()
    lumi = event.eventAuxiliary().luminosityBlock()
    eventid = event.eventAuxiliary().event()
    if options.writeids:
        if (run,lumi,eventid) in ids:
            print("duplicate !!! this should never happen !!!")
            exit()
        else:
            ids.add((run,lumi,eventid))
    if options.readids and (not ((run,lumi,eventid) in ids)):
        #print "not in id list"
        continue
    #event.getByLabel(eventinfo_label,eventinfo_handle)
    event.getByLabel(pfmet_label,pfmet_handle)
    event.getByLabel(puppimet_label,puppimet_handle)
    event.getByLabel(ak15jet_label,ak15jet_handle)
    event.getByLabel(ak4jet_label,ak4jet_handle)
    event.getByLabel(ak4puppijet_label,ak4puppijet_handle)
    event.getByLabel(electron_label,electron_handle)
    event.getByLabel(muon_label,muon_handle)
    event.getByLabel(photon_label,photon_handle)
    #eventinfo = eventinfo_handle.product()
    pfmet = pfmet_handle.product()[0]
    puppimet = puppimet_handle.product()[0]
    ak15jets = ak15jet_handle.product()
    ak4jets = ak4jet_handle.product()
    ak4puppijets = ak4puppijet_handle.product()
    electrons = electron_handle.product()
    muons = muon_handle.product()
    photons = photon_handle.product()
    
    pfmet_pt_hist.Fill(pfmet.pt())
    pfmet_phi_hist.Fill(pfmet.phi())
    puppimet_pt_hist.Fill(puppimet.pt())
    puppimet_phi_hist.Fill(puppimet.phi())
    
    FillVectorPtEta(ak15jets,ak15jet_pt_hist,ak15jet_eta_hist,160.)
    FillVectorPtEta(ak4jets,ak4jet_pt_hist,ak4jet_eta_hist)
    FillVectorPtEta(ak4puppijets,ak4puppijet_pt_hist,ak4puppijet_eta_hist)
    FillVectorPtEta(electrons,electron_pt_hist,electron_eta_hist)
    FillVectorPtEta(muons,muon_pt_hist,muon_eta_hist)
    FillVectorPtEta(photons,photon_pt_hist,photon_eta_hist)



hist_file = ROOT.TFile.Open(options.templateFile,"RECREATE")
hist_file.WriteTObject(pfmet_pt_hist)
hist_file.WriteTObject(puppimet_pt_hist)
hist_file.WriteTObject(pfmet_phi_hist)
hist_file.WriteTObject(puppimet_phi_hist)
hist_file.WriteTObject(ak15jet_pt_hist)
hist_file.WriteTObject(ak15jet_eta_hist)
hist_file.WriteTObject(ak4jet_pt_hist)
hist_file.WriteTObject(ak4jet_eta_hist)
hist_file.WriteTObject(ak4puppijet_pt_hist)
hist_file.WriteTObject(ak4puppijet_eta_hist)
hist_file.WriteTObject(electron_pt_hist)
hist_file.WriteTObject(electron_eta_hist)
hist_file.WriteTObject(muon_pt_hist)
hist_file.WriteTObject(muon_eta_hist)
hist_file.WriteTObject(photon_pt_hist)
hist_file.WriteTObject(photon_eta_hist)
hist_file.Close()

if options.writeids:
    with open(options.writeIDFile, 'w') as fp:
        fp.write('\n'.join('{},{},{}'.format(x[0],x[1],x[2]) for x in ids))
