#! /usr/bin/env python
import ROOT
import sys

def main():
    chain=ROOT.TChain("MVATree")
    inputfiles=[str(filename) for filename in sys.argv[1:]]
    #print inputfiles
    for file in inputfiles:
        chain.Add(file)

    print "created chain ",chain.GetName()," with ",chain.GetEntries()," entries"
    print "python object is called chain"
    return chain

if __name__== "__main__":
    chain=main()
