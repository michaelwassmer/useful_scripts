import ROOT
import os
import sys

file = ROOT.TFile.Open(str(sys.argv[1]))

template_names = set()
systematics_names = set()
problematic_systs = set()

# get the names of all nominal templates
# and "node" in key.GetName()
#  and "ttbar" in key.GetName() and not ("ttbarW" in key.GetName() or "ttbarZ" in key.GetName()
for key in file.GetListOfKeys():
    if not "up" in key.GetName().lower() and not "down" in key.GetName().lower() and key.GetName() not in template_names:
        template_names.add(key.GetName())
    
for element in template_names:
    print element

# get list of all shape uncertainties
for key in file.GetListOfKeys():
    if ("Up" in key.GetName() or "Down" in key.GetName()) and key.GetName().find("bin")==-1 and key.GetName().count("_CMS")==1:
        index = key.GetName().find("_CMS")
        systematic_name = key.GetName()[index:]
        systematic_name = systematic_name.replace("Up","").replace("Down","")
        if systematic_name not in systematics_names and "finaldiscr" not in systematic_name:
            systematics_names.add(systematic_name)

for element in systematics_names:
    print element
    
print "-------------------------------------------------"

template_dict = {}
systematic_dict = {}

# dictionaries to count the number of occurences
for systematic in systematics_names:
    template_dict[systematic]=[]
for systematic in systematics_names:
    systematic_dict[systematic]=0
    
for systematic_name in systematics_names:
    for histo in template_names:
        if "data" in histo or "Single" in histo:
            continue
        histo_nom = file.Get(histo)
        histo_up = file.Get(histo+systematic_name+"Up")
        print histo+systematic_name
        histo_down = file.Get(histo+systematic_name+"Down")
        #print "nom: ",histo_nom.Integral()," up: ",histo_up.Integral()," down: ",histo_down.Integral()
        try:
            if histo_nom.Integral()>0. and histo_up.Integral()!=0. and histo_down.Integral()!=0.:
                up = (histo_up.Integral()-histo_nom.Integral())/histo_nom.Integral()
                down = (histo_down.Integral()-histo_nom.Integral())/histo_nom.Integral()
                if up*down>0. and abs(up)>0.01 and abs(down)>0.01:
                    problematic_systs.add(histo+systematic_name)
                    systematic_dict[systematic_name]+=1
                    template_dict[systematic_name].append(histo)
                    print "Up: ",up, " Down: ",down 
        except AttributeError:
            continue
                
                
#print problematic_systs
#print template_dict
#print systematic_dict
#for key in template_dict:
    #print key," ",template_dict[key]

#for key in systematic_dict:
    #print key," ",systematic_dict[key]
    
sorted_systematics = sorted(systematic_dict,key=systematic_dict.__getitem__)

for syst in sorted_systematics:
    print "--------------------------------------------------------------------------------------"
    print "--------------------------------------------------------------------------------------"
    print syst," ",systematic_dict[syst]
    print "--------------------------------------------------------------------------------------"
    for template in template_dict[syst]:
        print template
