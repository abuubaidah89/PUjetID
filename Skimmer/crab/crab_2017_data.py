import sys
import crab_common 
import helpers

crab_common.config.General.requestName = crab_common.reqNamePrefix+'Data17_'+crab_common.version

crab_common.config.JobType.maxJobRuntimeMin = 480

crab_common.config.JobType.scriptArgs = [
'isMC=0',
'era=2017',
]

crab_common.config.Data.inputDataset     = '/DoubleMuon/Run2017B_ver1-Nano1June2019_ver1-v1/NANOAOD' #Dummy. Doesnt matter
crab_common.config.Data.outputDatasetTag = crab_common.reqNamePrefix+'Data17_'+crab_common.version #Dummy. Doesnt matter

if __name__ == '__main__':
  #
  # Read in txt file with list of samples
  #
  f = open(sys.argv[1]) 
  samplelist =  helpers.GetSampleList(f)
  print "Will send crab jobs for the following samples:"
  for dataset in samplelist:
    print dataset
  print "\n\n"

  from CRABClient.UserUtilities import getUsernameFromSiteDB
  from CRABAPI.RawCommand import crabCommand
  for i, dataset in enumerate(samplelist):
    print "%d/%d:Sending CRAB job: %s" % (i+1,len(samplelist), dataset)
    crab_common.config.Data.inputDataset = dataset
    #
    # Have to make unique requestName. pain in the ass really
    # Sample naming convention is a bit dumb and makes this more difficult.
    #
    primaryName   = dataset.split('/')[1]
    secondaryName = dataset.split('/')[2]
    secondaryName = secondaryName.replace("Nano1June2019","Data17NanoAODv5") #CHECK
    #
    requestName = primaryName + "_" + secondaryName
    requestName = crab_common.reqNamePrefix + "_" + requestName + "_" + crab_common.version
    crab_common.config.General.requestName   = requestName
    #  
    outputDatasetTag = crab_common.reqNamePrefix + "_" + secondaryName + "_" + crab_common.version 
    crab_common.config.Data.outputDatasetTag = outputDatasetTag 
    #
    print requestName , " | ", outputDatasetTag, "\n"
    crabCommand('submit', config = crab_common.config)
