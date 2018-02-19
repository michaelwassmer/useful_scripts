import sys
import os
import stat
import glob
import csv

def ReadOutdirIndir(csv_file):
	mydict={}
	with open(csv_file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			indir =row['inputdir']
			outdir = row['outputdir']
			mydict[indir]=outdir
	return mydict
	
def CreateCopyScript(indir,outdir,file_extension,number_of_files):
        i = 0
        k = 0
	files = glob.glob(os.path.join(indir,file_extension))
	for file_ in files:
            if i%number_of_files==0:
                script='#!/bin/bash\n'
                filename=os.path.basename(os.path.normpath(indir))+'_'+str(k)+'.sh'
                filename='file_transfer_scripts/'+filename
                f=open(filename,'w')
	    script+='gfal-copy -n 1 "file:////'+file_+'" "srm://dcache-se-cms.desy.de:8443/'+outdir+'"\n'
	    if i%number_of_files==number_of_files-1 or i==len(files)-1:
                f.write(script)
                f.close()
                st = os.stat(filename)
                os.chmod(filename, st.st_mode | stat.S_IEXEC)
                k+=1
	    i+=1
	
def main(csv_file):
	mydict = ReadOutdirIndir(csv_file)
	for key_indir in mydict:
		CreateCopyScript(key_indir,mydict[key_indir],'*.root',1000)


if __name__ == "__main__":
    main(sys.argv[1])
	
