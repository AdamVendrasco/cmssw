import FWCore.ParameterSet.Config as cms

rawDataProducer = cms.EDProducer('RawDataProducer',
  inputFileName = cms.string('/afs/cern.ch/user/a/avendras/work/CMSSW_14_1_0_pre5/src/EventFilter/Phase2TrackerRawToDigi/test/detids_phase2.txt')
)

