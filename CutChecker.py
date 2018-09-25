import ROOT
import numpy as np

class CutChecker:
    """A class to do simple efficiency checks for kinematic cuts"""
    def __init__(self, 
                 pt_branchname="Electron_Pt", min_pt = 25, max_pt = 30, pt_steps = 5,
                 eta_branchname="Electron_Eta", min_eta = 2.1, max_eta = 2.5, eta_steps = 4,
                 files = None, max_events=100000):
        
        self.pt_branchname_ = pt_branchname
        self.min_pt_ = min_pt
        self.max_pt_ = max_pt
        self.pt_steps_ = pt_steps
        
        self.eta_branchname_ = eta_branchname
        self.min_eta_ = min_eta
        self.max_eta_ = max_eta
        self.eta_steps_ = eta_steps
        
        if files == None or not isinstance(files,list):
            print "You need to give a valid file list."
            print "It is a python list with file names as strings."
            print "e.g. [\"file1.root\",\"file2.root\"]"
            exit()
        else:
            self.files_ = files
            
        self.chain = ROOT.TChain("MVATree")
        for file_ in self.files_:
            self.chain.Add(file_)
        self.chain.SetBranchStatus("*",0)
        self.chain.SetBranchStatus(self.pt_branchname_,1)
        self.chain.SetBranchStatus(self.eta_branchname_,1)
        self.chain.SetBranchStatus("Weight_XS",1)
        self.chain.SetBranchStatus("Weight_GEN_nom",1)
        print "Files have ",self.chain.GetEntries()," entries."
        
        if max_events<=0:
            self.max_events_ = 999999999
        else:
            self.max_events_ = max_events
        
        self.histos_dict = {}
    
    def GetEfficiencies(self):
        for pt in np.linspace(self.min_pt_,self.max_pt_,self.pt_steps_+1,endpoint=True):
            for eta in np.linspace(self.min_eta_,self.max_eta_,self.eta_steps_+1,endpoint=True):
                self.histos_dict[(pt,eta)]=ROOT.TH1D("Yield"+"_pt_"+str(pt)+"_eta_"+str(eta),"Yield"+"_pt_"+str(pt)+"_eta_"+str(eta),1,0.5,1.5)
                self.histos_dict[(pt,eta)].Sumw2()
        event_count = 0
        for event in self.chain:
            if event_count%10000==0:
                print event_count
            if event_count>self.max_events_:
                break
            weight = getattr(event,"Weight_XS")*getattr(event,"Weight_GEN_nom")
            for pt in np.linspace(self.min_pt_,self.max_pt_,self.pt_steps_+1,endpoint=True):
                for eta in np.linspace(self.min_eta_,self.max_eta_,self.eta_steps_+1,endpoint=True):
                    if len(list(getattr(event,self.pt_branchname_)))<1 or len(list(getattr(event,self.eta_branchname_)))<1:
                        continue
                    if getattr(event,self.pt_branchname_)[0]>=pt and abs(getattr(event,self.eta_branchname_)[0])<=eta:
                        self.histos_dict[(pt,eta)].Fill(1.,weight)
            event_count+=1
    
    def PlotEfficiencies(self):
        self.GetEfficiencies()
        effs = ROOT.TH2D("Efficiencies","cut efficiencies",self.pt_steps_,self.min_pt_,self.max_pt_,self.eta_steps_,self.min_eta_,self.max_eta_)
        effs.GetXaxis().SetTitle(self.pt_branchname_)
        effs.GetYaxis().SetTitle(self.eta_branchname_)
        binwidth_x = (self.max_pt_-self.min_pt_)/self.pt_steps_
        binwidth_y = (self.max_eta_-self.min_eta_)/self.eta_steps_
        for pt in np.linspace(self.min_pt_,self.max_pt_,self.pt_steps_+1,endpoint=True):
            for eta in np.linspace(self.min_eta_,self.max_eta_,self.eta_steps_+1,endpoint=True):
                bin_ = effs.FindBin(pt+0.1*binwidth_x,eta-0.1*binwidth_y)
                print pt, eta, bin_, 
                effs.SetBinContent(bin_,self.histos_dict[(pt,eta)].Integral()/self.histos_dict[(self.min_pt_,self.max_eta_)].Integral())
        return effs
