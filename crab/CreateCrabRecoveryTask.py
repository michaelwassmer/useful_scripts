from __future__ import print_function
from optparse import OptionParser
#import json
import os
from CRABAPI.RawCommand import crabCommand
from WMCore.Configuration import loadConfigurationFile
from CRABClient.UserUtilities import getLumiListInValidFiles
from FWCore.PythonUtilities.LumiList import LumiList

cwd = os.getcwd()
print("Starting from current working directory: ", cwd)

# options parser
usage = "usage: %prog [options]"
parser = OptionParser()
parser.add_option(
    "-c", "--config", dest="config", type="string", default="", help="path to the original crab config file"
    )
parser.add_option(
    "-p", "--project", dest="project", type="string", default="", help="path to the crab project directory"
)
(options, args) = parser.parse_args()

# check path of given crab config
if not os.path.isfile(options.config):
    print("Given config file is not a valid file, please check! Exiting ...")
    exit()

# check path of given crab folder
if not os.path.isdir(options.project):
    print("Given project folder is not a valid directory, please check! Exiting ...")
    exit()

# read the path to the original crab config
original_config_file = os.path.realpath(options.config)
# read the path to the original crab project directory
crab_project_dir = os.path.realpath(options.project)

print("Original crab config: ", original_config_file)
print("Original crab project folder: ", crab_project_dir)

# read config from python file using the crab python api
print("Loading original crab config ...")
config = None
try:
    config = loadConfigurationFile(original_config_file)
except:
    print("Something went wrong loading the original crab config, please check! Exiting ...")
    exit()

config_sections = config.listSections_()
# read some needed options from the original crab config file
original_input_dataset, original_units_per_job, original_splitting, original_publication = None, None, None, None
if "Data" in config_sections:
    original_input_dataset = config.section_("Data").section_("inputDataset")
    original_units_per_job = config.section_("Data").section_("unitsPerJob")
    original_splitting = config.section_("Data").section_("splitting")
    original_publication = config.section_("Data").section_("publication")
original_request_name, original_workarea = None, None
if "General" in config_sections:
    original_request_name = config.section_("General").section_("requestName")
    original_workarea = config.section_("General").section_("workArea")
original_max_memory = None
if "JobType" in config_sections:
    original_max_memory = config.section_("JobType").section_("maxMemoryMB")

print("Original input dataset: ", original_input_dataset)

# change some options
# decrease the number of processed events per job
if original_splitting == "EventAwareLumiBased":
    config.section_("Data").__setattr__("unitsPerJob", int(original_units_per_job/10.))
elif original_splitting == "Automatic":
    config.section_("Data").__setattr__("unitsPerJob", 180)
print("Changed unitsPerJob from {} to {}".format(original_units_per_job, config.section_("Data").section_("unitsPerJob")))

# increase the requested memory if it is below the maximum value of single core jobs
if original_max_memory < 5000:
    config.section_("JobType").__setattr__("maxMemoryMB", 5000)
print("Changed maxMemoryMB from {} to {}".format(original_max_memory, config.section_("JobType").section_("maxMemoryMB")))

# adapt the request name and the work area
config.section_("General").__setattr__("requestName", original_request_name + "_recovery")
print("Changed requestName from {} to {}".format(original_request_name, config.section_("General").section_("requestName")))
config.section_("General").__setattr__("workArea", original_workarea + "_recovery")
print("Changed workArea from {} to {}".format(original_workarea, config.section_("General").section_("workArea")))

output = None
output_dataset = None

# find name of dataset published by orignal crab job
if original_publication:
    import subprocess
    try:
        output = subprocess.check_output(['crab status {}'.format(crab_project_dir)],shell=True)
    except subprocess.CalledProcessError as e:
        print("\n")
        print("!!! INFO: If the crab project folder is somewhere where you dont have write access, you can ignore the errors. !!!")
        print("\n")
        output = e.output.decode()
    output = str(output)
    output = output.split("\n")
    for line in output:
        if "Output dataset:" in line:
            output_dataset = line
            break
    output_dataset = output_dataset.replace("Output dataset:","")
    output_dataset = output_dataset.lstrip("\t")
    if output_dataset.startswith("/") and output_dataset.endswith("/USER"):
        print("Found published dataset: ", output_dataset)
    else:
        print("The originally published dataset name could not be determined, please check! Exiting ...")
        exit()
else:
    try:
        crabCommand('report', crab_project_dir)
    except IOError:
        print("You need write access for crab report. Exiting ...")
        exit()
    if not os.path.isfile(crab_project_dir + "/results/processedLumis.json"):
        print("processedLumis json was not found in crab project folder, please check! Exiting ...")
        exit()

# find dbs instance of original dataset
dbs_instance = "phys03" if "USER" in original_input_dataset else "global"

# get the lumis processed by the original crab job
original_task_lumis = None
if original_publication:
    original_task_lumis = getLumiListInValidFiles(dataset=output_dataset, dbsurl='phys03')
else:
    original_task_lumis = LumiList(crab_project_dir + "/results/processedLumis.json")

# get the lumis in the original input dataset
officialLumiMask = getLumiListInValidFiles(dataset=original_input_dataset, dbsurl=dbs_instance)

# get a possibly previously used lumi mask
previousLumiMask = None
if "lumiMask" in config.section_("Data").listSections_():
    previousLumiMask = LumiList(config.section_("Data").section_("lumiMask"))
    print("Previous lumi mask was found to be: ", config.section_("Data").section_("lumiMask"))

# lumi sections to exclude in recovery job
excludeLumiMask = None
if previousLumiMask:
    excludeLumiMask = officialLumiMask - previousLumiMask

# create lumi mask for recovery job
recoveryLumiMask = None
if previousLumiMask and excludeLumiMask:
    recoveryLumiMask = (officialLumiMask - original_task_lumis) - excludeLumiMask
else:
    recoveryLumiMask = officialLumiMask - original_task_lumis

# write lumi mask of recovery job into a json file
lumijson = original_config_file.replace(".py","_recovery.json")
try:
    recoveryLumiMask.writeJSON(lumijson)
except IOError:
    lumijson = os.path.join(cwd, os.path.basename(original_config_file).replace(".py","_recovery.json"))
    recoveryLumiMask.writeJSON(lumijson)

if not os.path.isfile(lumijson):
    print("Written lumimask json is not a valid file, please check! Exiting ...")
    exit()

print("Recovery job lumi mask: ", lumijson)

# use the lumi mask of the recovery job in the crab config
config.section_("Data").__setattr__("lumiMask", lumijson)

# write the crab config for the recovery job
recovery_config = original_config_file.replace(".py","_recovery.py")
try:
    with open(recovery_config,"w") as f_out:
        f_out.write(str(config))
except IOError:
    recovery_config = os.path.join(cwd, os.path.basename(original_config_file).replace(".py","_recovery.py"))
    with open(recovery_config,"w") as f_out:
        f_out.write(str(config))

# check if the crab config for the recovery job was written
if not os.path.isfile(recovery_config):
    print("Written recovery config is not a valid file, please check! Exiting ...")
    exit()

print("\n")
print("####################### recovery config to submit ############################")
print(recovery_config)
print("\n")