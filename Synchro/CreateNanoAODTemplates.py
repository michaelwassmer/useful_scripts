from __future__ import print_function
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-R", action="store_true", dest="readids", default=False)
parser.add_option("-W", action="store_true", dest="writeids", default=False)
parser.add_option("--readIDFile",action="store",dest="readIDFile", default="")
parser.add_option("--writeIDFile",action="store",dest="writeIDFile", default="")
parser.add_option("--templateFile",action="store",dest="templateFile", default="")
parser.add_option("-d", action="store_true", dest="isdata", default=False)

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
#from sets import Set

def FillVectorPtEta(vector_pt,vector_eta,hist_pt,hist_eta,ptmin=-1.,etamax=999.):
    for pt,eta in zip(vector_pt,vector_eta):
        if pt > ptmin and abs(eta) < etamax:
            hist_pt.Fill(pt)
            hist_eta.Fill(eta)

#id_tuples = []
ids = set()
if options.readIDFile:
    with open(options.readIDFile, 'r') as fp:
        for line in fp:
            line_as_list = line.replace("\n","").split(",")
            run = int(line_as_list[0])
            lumi = int(line_as_list[1])
            eventid = int(line_as_list[2])
            if (run,lumi,eventid) in ids:
                print("duplicate !!! this should never happen !!!")
                exit()
            else:
                ids.add((run,lumi,eventid))

#ids = set(id_tuples)

#print ids

files = args

pfmet_pt_hist = ROOT.TH1D("PFMET_pt","PFMET pt",50,0,1000)
pfmet_phi_hist = ROOT.TH1D("PFMET_phi","PFMET phi",64,-3.2,3.2)
puppimet_pt_hist = ROOT.TH1D("PUPPIMET_pt","PUPPIMET pt",50,0,1000)
puppimet_phi_hist = ROOT.TH1D("PUPPIMET_phi","PUPPIMET phi",64,-3.2,3.2)
n_ak15jets_hist = ROOT.TH1D("nAK15Puppi","nAK15Puppi",6,-0.5,5.5)
ak15jet_pt_hist = ROOT.TH1D("AK15Jet_pt","AK15Jet pt",50,0,1000)
ak15jet_eta_hist = ROOT.TH1D("AK15Jet_eta","AK15Jet eta",48,-2.4,2.4)
ak4jet_pt_hist = ROOT.TH1D("AK4Jet_pt","AK4Jet pt",50,0,1000)
ak4jet_eta_hist = ROOT.TH1D("AK4Jet_eta","AK4Jet eta",48,-2.4,2.4)
electron_pt_hist = ROOT.TH1D("Electron_pt","Electron pt",50,0,500)
electron_eta_hist = ROOT.TH1D("Electron_eta","Electron eta",50,-2.5,2.5)
muon_pt_hist = ROOT.TH1D("Muon_pt","Muon pt",50,0,500)
muon_eta_hist = ROOT.TH1D("Muon_eta","Muon eta",50,-2.5,2.5)
photon_pt_hist = ROOT.TH1D("Photon_pt","Photon pt",50,0,500)
photon_eta_hist = ROOT.TH1D("Photon_eta","Photon eta",50,-2.5,2.5)

chain = ROOT.TChain("Events")
for file in files:
    chain.Add(file)

chain.SetBranchStatus("*",0)

chain.SetBranchStatus("run",1)
chain.SetBranchStatus("luminosityBlock",1)
chain.SetBranchStatus("event",1)

chain.SetBranchStatus("MET_pt",1)
chain.SetBranchStatus("MET_phi",1)

chain.SetBranchStatus("PuppiMET_pt",1)
chain.SetBranchStatus("PuppiMET_phi",1)

chain.SetBranchStatus("nAK15Puppi",1)
chain.SetBranchStatus("AK15Puppi_pt",1)
chain.SetBranchStatus("AK15Puppi_eta",1)

#chain.SetBranchStatus("nJet",1)
chain.SetBranchStatus("Jet_pt",1)
chain.SetBranchStatus("Jet_eta",1)

#chain.SetBranchStatus("nElectron",1)
chain.SetBranchStatus("Electron_pt",1)
chain.SetBranchStatus("Electron_eta",1)

#chain.SetBranchStatus("nMuon",1)
chain.SetBranchStatus("Muon_pt",1)
chain.SetBranchStatus("Muon_eta",1)

#chain.SetBranchStatus("nPhoton",1)
chain.SetBranchStatus("Photon_pt",1)
chain.SetBranchStatus("Photon_eta",1)

chain.SetBranchStatus("Flag_HBHENoiseFilter",1)
chain.SetBranchStatus("Flag_HBHENoiseIsoFilter",1)
chain.SetBranchStatus("Flag_globalSuperTightHalo2016Filter",1)
chain.SetBranchStatus("Flag_EcalDeadCellTriggerPrimitiveFilter",1)
chain.SetBranchStatus("Flag_goodVertices",1)
chain.SetBranchStatus("Flag_BadPFMuonFilter",1)
chain.SetBranchStatus("Flag_eeBadScFilter",1)

print("need to loop over ",chain.GetEntries()," events")

for number,event in enumerate(chain):
    if number % 10000 == 0:
        print(number)
    
    met_filter = event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_globalSuperTightHalo2016Filter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_goodVertices and event.Flag_BadPFMuonFilter
    if options.isdata:
        met_filter = met_filter and event.Flag_eeBadScFilter
    
    if not (event.MET_pt>200. and event.nAK15Puppi>0 and met_filter):
        continue
    
    if options.writeids:
        if (event.run,event.luminosityBlock,event.event) in ids:
            print("duplicate !!! this should never happen !!!")
            exit()
        else:
            ids.add((event.run,event.luminosityBlock,event.event))
    
    if options.readids and (not ((event.run,event.luminosityBlock,event.event) in ids)):
        #print "not in id list"
        continue
    else:
        pfmet_pt = event.MET_pt
        pfmet_phi = event.MET_phi
        puppimet_pt = event.PuppiMET_pt
        puppimet_phi = event.PuppiMET_phi
        n_ak15jets = event.nAK15Puppi
        ak15jet_pts = event.AK15Puppi_pt
        ak15jet_etas = event.AK15Puppi_eta
        ak4jet_pts = event.Jet_pt
        ak4jet_etas = event.Jet_eta
        electron_pts = event.Electron_pt
        electron_etas = event.Electron_eta
        muon_pts = event.Muon_pt
        muon_etas = event.Muon_eta
        photon_pts = event.Photon_pt
        photon_etas = event.Photon_eta
                        
        pfmet_pt_hist.Fill(pfmet_pt)
        pfmet_phi_hist.Fill(pfmet_phi)
        puppimet_pt_hist.Fill(puppimet_pt)
        puppimet_phi_hist.Fill(puppimet_phi)
        n_ak15jets_hist.Fill(n_ak15jets)
        
        FillVectorPtEta(ak15jet_pts,ak15jet_etas,ak15jet_pt_hist,ak15jet_eta_hist)
        FillVectorPtEta(ak4jet_pts,ak4jet_etas,ak4jet_pt_hist,ak4jet_eta_hist,20.,2.5)
        FillVectorPtEta(electron_pts,electron_etas,electron_pt_hist,electron_eta_hist)
        FillVectorPtEta(muon_pts,muon_etas,muon_pt_hist,muon_eta_hist)
        FillVectorPtEta(photon_pts,photon_etas,photon_pt_hist,photon_eta_hist)


hist_file = ROOT.TFile.Open(options.templateFile,"RECREATE")
hist_file.WriteTObject(pfmet_pt_hist)
hist_file.WriteTObject(puppimet_pt_hist)
hist_file.WriteTObject(pfmet_phi_hist)
hist_file.WriteTObject(puppimet_phi_hist)
hist_file.WriteTObject(n_ak15jets_hist)
hist_file.WriteTObject(ak15jet_pt_hist)
hist_file.WriteTObject(ak15jet_eta_hist)
hist_file.WriteTObject(ak4jet_pt_hist)
hist_file.WriteTObject(ak4jet_eta_hist)
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
