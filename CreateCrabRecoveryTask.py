from __future__ import print_function
from optparse import OptionParser
import json

usage = "usage: %prog [options]"
parser = OptionParser()
parser.add_option(
    "-c", "--config", dest="config", type="string", default="", help="path to the original crab config file"
    )
parser.add_option(
    "-p", "--project", dest="project", type="string", default="", help="path to the crab project directory"
)
parser.add_option("-l", "--local", action="store_true", dest="local", default=False)
(options, args) = parser.parse_args()

# read the path to the original crab config
original_config_file = options.config
# read the path to the original crab project directory
crab_project_dir = options.project

output_dataset_json_file = crab_project_dir + "/results/outputDatasetsLumis.json"

# read in the original crab config file
original_config_as_list = None
with open(original_config_file) as f_in:
    original_config_as_list = f_in.readlines()

#print("original crab config:")
#print("-----------------------------------------------------")
#for line in original_config_as_list:
    #print(line)

# read some needed options from the original crab config file
original_input_dataset = None
request_name = None
max_memory_mb = None
for line in original_config_as_list:
    if "inputDataset" in line:
        original_input_dataset = line.split("=")[1].strip().replace('"','')
    if "requestName" in line:
        request_name = line.split("=")[1].strip().replace('"','')
    if "unitsPerJob" in line:
        units_per_job = line.split("=")[1].strip().replace('"','')
    if "maxMemoryMB" in line:
        max_memory_mb = line.split("=")[1].strip().replace('"','')

# read the outputDataset lumi json ...
output_json_as_dict = None
with open(output_dataset_json_file) as output_json:
    output_json_as_dict = json.load(output_json)

# ... and extract the name of the published dataset created by the original crab task
output_dataset = None
for key in output_json_as_dict:
    if "USER" in key:
        output_dataset = key.strip()

#print output_dataset

# start to modify the original crab config to create a recovery task
modified_config_as_list = []
for line in original_config_as_list:
    if "import" in line:
        continue
    if "requestName" in line or "workArea" in line:
        modified_config_as_list.append(line.replace("\n","")+'+"_recovery"'+"\n")
    elif "unitsPerJob" in line:
        modified_config_as_list.append(line.replace(units_per_job,"180"))
    elif "maxMemoryMB" in line:
        modified_config_as_list.append(line.replace(max_memory_mb,"5000"))
    else:
        modified_config_as_list.append(line)
# get the lumis processed by the original crab job
modified_config_as_list.append("\n")
if not options.local:
    modified_config_as_list.append("original_task_lumis = getLumiListInValidFiles(dataset=\"{}\", dbsurl='phys03')".format(output_dataset))
else:
    modified_config_as_list.append("original_task_lumis = LumiList(\"" + crab_project_dir + "/results/processedLumis.json\")")
modified_config_as_list.append("\n")
# get the lumis in the original input dataset
modified_config_as_list.append("officialLumiMask = getLumiListInValidFiles(dataset=\"{}\", dbsurl='global')".format(original_input_dataset))
modified_config_as_list.append("\n")
# find the lumis which have not been processed by the original crab job
modified_config_as_list.append("recoveryLumiMask = officialLumiMask - original_task_lumis")
modified_config_as_list.append("\n")
# write these lumis to a json
modified_config_as_list.append("recoveryLumiMask.writeJSON(\"{}\")".format(request_name+"_recovery.json"))
modified_config_as_list.append("\n")
# read the json as a lumimask for the recovery crab task
modified_config_as_list.append("config.Data.lumiMask = \"{}\"".format(request_name+"_recovery.json"))
modified_config_as_list.append("\n")

import_statements = ["from CRABClient.UserUtilities import config, getLumiListInValidFiles\n","from WMCore.DataStructs.LumiList import LumiList\n"]

#for line in import_statements+modified_config_as_list:
    #print(line)

with open(request_name+"_recovery.py","w") as f_out:
    f_out.writelines(import_statements+modified_config_as_list)

