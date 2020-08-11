import ROOT
import sys
#from sets import Set

def FillVectorPtEta(vector_pt,vector_eta,hist_pt,hist_eta,ptmin=-1.,etamax=999.):
    for pt,eta in zip(vector_pt,vector_eta):
        if pt > ptmin and abs(eta) < etamax:
            hist_pt.Fill(pt)
            hist_eta.Fill(eta)

##id_tuples = []
#ids = set()
#with open('id_tuples_MiniAOD.txt', 'r') as fp:
    #for line in fp:
        #line_as_list = line.replace("\n","").split(",")
        #run = int(line_as_list[0])
        #lumi = int(line_as_list[1])
        #eventid = int(line_as_list[2])
        #if (run,lumi,eventid) in ids:
            #print "duplicate !!! this should never happen !!!"
            #exit()
        #else:
            #ids.add((run,lumi,eventid))

#ids = set(id_tuples)

#print ids

files = sys.argv[1:]

pfmet_pt_hist = ROOT.TH1D("PFMET_pt","PFMET pt",50,0,1000)
pfmet_phi_hist = ROOT.TH1D("PFMET_phi","PFMET phi",64,-3.2,3.2)
puppimet_pt_hist = ROOT.TH1D("PUPPIMET_pt","PUPPIMET pt",50,0,1000)
puppimet_phi_hist = ROOT.TH1D("PUPPIMET_phi","PUPPIMET phi",64,-3.2,3.2)
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

chain = ROOT.TChain("MVATree")
for file in files:
    chain.Add(file)

chain.SetBranchStatus("*",0)

chain.SetBranchStatus("Evt_Run",1)
chain.SetBranchStatus("Evt_Lumi",1)
chain.SetBranchStatus("Evt_ID",1)

chain.SetBranchStatus("Evt_Pt_MET",1)
chain.SetBranchStatus("Evt_Phi_MET",1)

chain.SetBranchStatus("Evt_Pt_MET_Puppi",1)
chain.SetBranchStatus("Evt_Phi_MET_Puppi",1)

#chain.SetBranchStatus("nAK15Puppi",1)
chain.SetBranchStatus("AK15Jet_Pt",1)
chain.SetBranchStatus("AK15Jet_Eta",1)

#chain.SetBranchStatus("nJet",1)
chain.SetBranchStatus("Jet_Pt",1)
chain.SetBranchStatus("Jet_Eta",1)

#chain.SetBranchStatus("nElectron",1)
chain.SetBranchStatus("LooseElectron_Pt",1)
chain.SetBranchStatus("LooseElectron_Eta",1)

#chain.SetBranchStatus("nMuon",1)
chain.SetBranchStatus("LooseMuon_Pt",1)
chain.SetBranchStatus("LooseMuon_Eta",1)

#chain.SetBranchStatus("nPhoton",1)
chain.SetBranchStatus("LoosePhoton_Pt",1)
chain.SetBranchStatus("LoosePhoton_Eta",1)

id_tuples = []

print "need to loop over ",chain.GetEntries()," events"

for number,event in enumerate(chain):
    if number % 1000 == 0:
        print number
    run = event.Evt_Run
    lumi = event.Evt_Lumi
    eventid = event.Evt_ID
    id_tuples.append((run,lumi,eventid))
    pfmet_pt = event.Evt_Pt_MET
    pfmet_phi = event.Evt_Phi_MET
    puppimet_pt = event.Evt_Pt_MET_Puppi
    puppimet_phi = event.Evt_Phi_MET_Puppi
    ak15jet_pts = event.AK15Jet_Pt
    ak15jet_etas = event.AK15Jet_Eta
    ak4jet_pts = event.Jet_Pt
    ak4jet_etas = event.Jet_Eta
    electron_pts = event.LooseElectron_Pt
    electron_etas = event.LooseElectron_Eta
    muon_pts = event.LooseMuon_Pt
    muon_etas = event.LooseMuon_Eta
    photon_pts = event.LoosePhoton_Pt
    photon_etas = event.LoosePhoton_Eta
    
    pfmet_pt_hist.Fill(pfmet_pt)
    pfmet_phi_hist.Fill(pfmet_phi)
    puppimet_pt_hist.Fill(puppimet_pt)
    puppimet_phi_hist.Fill(puppimet_phi)
    
    FillVectorPtEta(ak15jet_pts,ak15jet_etas,ak15jet_pt_hist,ak15jet_eta_hist)
    FillVectorPtEta(ak4jet_pts,ak4jet_etas,ak4jet_pt_hist,ak4jet_eta_hist,20.,2.5)
    FillVectorPtEta(electron_pts,electron_etas,electron_pt_hist,electron_eta_hist)
    FillVectorPtEta(muon_pts,muon_etas,muon_pt_hist,muon_eta_hist)
    FillVectorPtEta(photon_pts,photon_etas,photon_pt_hist,photon_eta_hist)


hist_file = ROOT.TFile.Open("Ntuple_templates.root","RECREATE")
hist_file.WriteTObject(pfmet_pt_hist)
hist_file.WriteTObject(puppimet_pt_hist)
hist_file.WriteTObject(pfmet_phi_hist)
hist_file.WriteTObject(puppimet_phi_hist)
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

with open('id_tuples_Ntuple.txt', 'w') as fp:
    fp.write('\n'.join('{},{},{}'.format(x[0],x[1],x[2]) for x in id_tuples))
