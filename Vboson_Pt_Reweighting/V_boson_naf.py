import Utilities.General.cmssw_das_client as das_client
import sys
import ROOT
import stat
import os
file_prefix="root://xrootd-cms.infn.it//"

def get_files(dataset_name):
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

def split_files_into_jobs(files,events_per_job):
    events=0
    file_splitting = []
    files_in_job = []
    for i,file in enumerate(files):
        print "file ",i
        files_in_job.append(file)
        file_ = ROOT.TFile.Open(file)
        tree = None
        try:
            tree = file_.Get("Events")
        except ReferenceError:
            file_.Close()
            continue
        events+=tree.GetEntries()
        file_.Close()
        if events>=events_per_job or i==(len(files)-1):
            file_splitting.append(files_in_job)
            events=0
            files_in_job = []
    return file_splitting

def print_shell_script(boson,postfix,files):
    script=""
    script+="#!/bin/bash\n"
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh\n"
    script+="cd /nfs/dust/cms/user/mwassmer/DarkMatter/CMSSW_8_0_26_patch2//src\n"
    script+="eval `scram runtime -sh`\n"
    if not os.path.isdir("root_files"):
        os.mkdir("root_files")
    script+="cd /nfs/dust/cms/user/mwassmer/DarkMatter/useful_scripts/root_files\n"
    script+="python /nfs/dust/cms/user/mwassmer/DarkMatter/useful_scripts/V_boson_pt_reweighting.py "+boson+" "+postfix
    for file in files:
        script+=" "+file
    if not os.path.isdir("scripts"):
        os.mkdir("scripts")
    filename = 'scripts/'+boson+'_boson_pt_'+postfix+'.sh'
    f=open(filename,'w')
    f.write(script)
    f.close()
    print 'created script',filename
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)

boson = str(sys.argv[1])
if not (boson=="Zvv" or boson=="Zll" or boson=="W"):
    print "first argument has to be Z or W"
    exit()
files = get_files(str(sys.argv[2]).replace('"',''))
file_splitting = split_files_into_jobs(files,1)
print file_splitting
for i,files in enumerate(file_splitting):
    print_shell_script(boson,str(i),files)
