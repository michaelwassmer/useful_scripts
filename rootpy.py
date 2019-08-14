#! /usr/bin/env python
from __future__ import print_function
import ROOT
import sys
from optparse import OptionParser
import os

def main():
    parser = OptionParser(usage="usage: %prog [options] file1 file2")
    parser.add_option("-t", "--treename", dest="treename",help="give the name of the TTree in the files",type="string",default="MVATree")
    (options, args) = parser.parse_args()
    #print options
    #print args
    chain=ROOT.TChain(options.treename)
    inputfiles=[str(filename) for filename in args]
    #print inputfiles
    for file in inputfiles:
        f=ROOT.TFile.Open(file)
        if not f:
            continue
        if f.IsZombie():
            f.Close()
            continue
        if f.TestBit(ROOT.TFile.kRecovered):
            f.Close()
            continue
        f.Close()
        chain.Add(file)

    print("created chain",chain.GetName(),"with")
    print(chain.GetEntries(),"entries")
    print(chain.GetNbranches(),"branches")
    print(chain.GetNtrees(),"files")
    print("python object is called chain")
    print("now you can work with the chain, e.g. do chain.GetEntries()")
    return chain

if __name__== "__main__":
    chain=main()
