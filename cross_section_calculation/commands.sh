# command to write the files for several datasets which are in a text file called datasets.txt using the dasgoclient
for i in $(cat datasets.txt); do dasgoclient --query="file dataset=$i" | head -n 30 > $(echo $i | cut -d"/" -f2 | cut -d"/" -f1)_FILES.txt;done
# command to run the cross section calculation over the files and print the result to a text file
for i in *FILES.txt; do cmsRun ana.py maxEvents=1000000 inputFiles_load=$i 2>&1 | tee ${i%_FILES.txt}_XS.txt;done
