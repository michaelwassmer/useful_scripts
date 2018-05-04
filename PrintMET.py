# this script print the trigger paths / filters of a MINIAOD file you give as an argument
# trigger paths if you use TriggerResults::HLT
# filters if you use TriggerResults::RECO for data or TriggerResults::PAT for mc
import ROOT
import sys
import Utilities.General.cmssw_das_client as das_client
from DataFormats import FWLite
ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.FWLiteEnabler.enable()
ROOT.gSystem.Load('libDataFormatsFWLite.so')
ROOT.gROOT.SetBatch(True)

file_prefix="root://xrootd-cms.infn.it//"

def get_first_file(dataset_name):
    print dataset_name
    data=das_client.get_data("file dataset="+dataset_name)
    files=[]
    for d in data['data']:
        #print d
        for f in d['file']:
            #print f
            #if not 'nevents' in f:
                #continue
            files.append(file_prefix+f['name'])
    return files

files = get_first_file(str(sys.argv[1]).replace('"',''))
#print files
file_names = [str(file) for file in files]
print file_names
sample = str(sys.argv[2])

events = FWLite.Events(file_names)
met = FWLite.Handle('std::vector<pat::MET>')
eventinfo = FWLite.Handle('GenEventInfoProduct')
label =	'slimmedMETs'
root_file = ROOT.TFile("/nfs/dust/cms/user/mwassmer/DarkMatter/useful_scripts/met_histos_"+sample+".root","RECREATE")
hist = ROOT.TH1D("met_pt_unw","met_pt_unweighted",150,0.,2000.)
hist_w = ROOT.TH1D("met_pt_w","met_pt_weighted",150,0.,2000.)
hist.Sumw2()
hist_w.Sumw2()
canvas = ROOT.TCanvas()
for number,event in enumerate(events):
    event.getByLabel(label, met)
    event.getByLabel('generator', eventinfo)
    met_pt = met.product()[0].pt()
    weight = eventinfo.product().weight()
    if(number % 10000==0):
        print number
        #print met_pt
        #print weight
    hist.Fill(met_pt)
    hist_w.Fill(met_pt,weight)
print "unweighted histogram: integral ",hist.Integral()
print "unweighted histogram: entries ",hist.GetEntries()
print "weighted histogram: integral ",hist_w.Integral()
print "weighted histogram: entries ",hist_w.GetEntries()
hist.Draw("hist")
canvas.SaveAs("MET_unweighted_"+sample+".pdf")
hist_w.Draw("hist")
canvas.SaveAs("MET_weighted_"+sample+".pdf")
root_file.WriteTObject(hist)
root_file.WriteTObject(hist_w)
root_file.Close()

