import ROOT
import sys

file1_str = str(sys.argv[1])
file2_str = str(sys.argv[2])

if len(sys.argv)>3:
    systematic_str = str(sys.argv[3])
else:
    systematic_str=""

file1 = ROOT.TFile.Open(file1_str)
file2 = ROOT.TFile.Open(file2_str)

tree1 = file1.Get("MVATree")
tree2 = file2.Get("MVATree")

print tree1.GetEntries()
print tree2.GetEntries()

if tree1.GetEntries()!=tree2.GetEntries():
    print "trees dont have the same number of events"
    exit()

branches1 = tree1.GetListOfBranches()
branches1_str = [branch.GetName() for branch in branches1]
branches2 = tree2.GetListOfBranches()
branches2_str = [branch.GetName() for branch in branches2]

if branches1_str!=branches2_str:
    print "something wrong with branches"
    exit()

if len(branches1)!=len(branches2):
    print "files dont have the same number of branches"
    exit()
    
test1=[]
for event1 in tree1:
    for branch1 in branches1:
        var1 = getattr(event1,branch1.GetName())
        test1.append(var1)
test2=[]  
for event2 in tree2:
    for branch2 in branches2:
        var2 = getattr(event2,branch2.GetName()) 
        test2.append(var2)
            
if test1!=test2:
    print "files not the same"
    exit()

if len(test1)!=len(test2):
    print "files not the same"
    exit()

for i in range(len(test1)):
    if test1[i]!=test2[i]:
        print "files not the same"
        exit()

print "files are the same"
#file1.Dump()
#file2.Dump()
  
#file1.Print()
#file2.Print()
