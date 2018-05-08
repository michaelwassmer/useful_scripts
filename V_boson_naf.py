import Utilities.General.cmssw_das_client as das_client
import sys
import ROOT
import stat
import os
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

def split_files(files,splitting):
    events=0
    file_splitting = []
    job = []
    for i,file in enumerate(files):
        job.append(file)
        file_ = ROOT.TFile.Open(file)
        tree = file_.Get("Events")
        events+=tree.GetEntries()
        if events>=splitting or i==(len(files)-1):
            file_splitting.append(job)
            events=0
            job = []
    return file_splitting

def print_shell_script(files,postfix):
    script=""
    script+="#!/bin/bash\n"
    script+="export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch\n"
    script+="source $VO_CMS_SW_DIR/cmsset_default.sh\n"
    script+="cd /nfs/dust/cms/user/mwassmer/DarkMatter/CMSSW_8_0_26_patch2//src\n"
    script+="eval `scram runtime -sh`\n"
    script+="cd /nfs/dust/cms/user/mwassmer/DarkMatter/useful_scripts/root_files\n"
    script+="python /nfs/dust/cms/user/mwassmer/DarkMatter/useful_scripts/V_boson_pt_reweighting.py "+postfix
    for file in files:
        script+=" "+file
    filename = 'scripts/z_boson_pt_'+postfix+'.sh'
    f=open(filename,'w')
    f.write(script)
    f.close()
    print 'created script',filename
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


files = get_first_file(str(sys.argv[1]).replace('"',''))
file_splitting = split_files(files,500000)
print file_splitting
for i,files in enumerate(file_splitting):
    print_shell_script(files,str(i))
