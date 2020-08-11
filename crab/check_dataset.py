from __future__ import print_function
from CRABClient.UserUtilities import getLumiListInValidFiles
from WMCore.DataStructs.LumiList import LumiList
import sys
import csv

dataset_csv = sys.argv[1]
with open(dataset_csv) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['dataset']=='' or row['boosted_dataset']=='':
            continue
        print(row['dataset'], row['boosted_dataset'])
        original_task_lumis = getLumiListInValidFiles(dataset=row['boosted_dataset'], dbsurl='phys03')
        officalLumiMask = getLumiListInValidFiles(dataset=row['dataset'], dbsurl='global')
        remaining = officalLumiMask - original_task_lumis
        print(remaining)
