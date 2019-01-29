import ROOT
import sys
from array import array
files = sys.argv[1:]
#ROOT.ROOT.EnableImplicitMT(4)
chain=ROOT.TChain("MVATree")
for file in files:
    chain.Add(file)

all = ROOT.TH1D("all","all",1,0.,2.)
ttlf = ROOT.TH1D("ttlf","ttlf",1,0.,2.)
ttcc = ROOT.TH1D("ttcc","ttcc",1,0.,2.)
ttb = ROOT.TH1D("ttb","ttb",1,0.,2.)
tt2b = ROOT.TH1D("tt2b","tt2b",1,0.,2.)
ttbb = ROOT.TH1D("ttbb","ttbb",1,0.,2.)

chain.SetBranchStatus("*",0)
chain.SetBranchStatus("Weight_GEN_nom",1)
chain.SetBranchStatus("GenEvt_I_TTPlusCC",1)
chain.SetBranchStatus("GenEvt_I_TTPlusBB",1)

weight_gen_nom = array('f',[-1.])
ttcc_flag = array('i',[-1])
ttbb_flag = array('i',[-1])

chain.SetBranchAddress("Weight_GEN_nom",weight_gen_nom)
chain.SetBranchAddress("GenEvt_I_TTPlusCC",ttcc_flag)
chain.SetBranchAddress("GenEvt_I_TTPlusBB",ttbb_flag)

print "#Entries: ",chain.GetEntries()
for i in range(chain.GetEntries()):
    if i%10000==0:
        print i
    chain.GetEntry(i)
    all.Fill(1.,weight_gen_nom[0])
    if ttbb_flag[0]==0 and ttcc_flag[0]==0:
        ttlf.Fill(1.,weight_gen_nom[0])
    elif ttbb_flag[0]==0 and ttcc_flag[0]==1:
        ttcc.Fill(1.,weight_gen_nom[0])
    elif ttbb_flag[0]==1 and ttcc_flag[0]==0:
        ttb.Fill(1.,weight_gen_nom[0])
    elif ttbb_flag[0]==2 and ttcc_flag[0]==0:
        tt2b.Fill(1.,weight_gen_nom[0])
    elif ttbb_flag[0]==3 and ttcc_flag[0]==0:
        ttbb.Fill(1.,weight_gen_nom[0])
    
print "Entries: "
print "all: ",all.GetEntries()
print "ttlf: ",ttlf.GetEntries()
print "ttcc: ",ttcc.GetEntries()
print "ttb: ",ttb.GetEntries()
print "tt2b: ",tt2b.GetEntries()
print "ttbb: ",ttbb.GetEntries()

print "Integrals: "
print "all: ",all.Integral()
print "ttlf: ",ttlf.Integral()
print "ttcc: ",ttcc.Integral()
print "ttb: ",ttb.Integral()
print "tt2b: ",tt2b.Integral()
print "ttbb: ",ttbb.Integral()

print "Integral fractions: "
print "all/all: ",all.Integral()/all.Integral()
print "ttlf/all: ",ttlf.Integral()/all.Integral()
print "ttcc/all: ",ttcc.Integral()/all.Integral()
print "ttb/all: ",ttb.Integral()/all.Integral()
print "tt2b/all: ",tt2b.Integral()/all.Integral()
print "ttbb/all: ",ttbb.Integral()/all.Integral()
