import FWCore.ParameterSet.Config as cms
import sys

process = cms.Process("RawToDigi")

#process.load( "FWCore.MessageLogger.MessageLogger_cfi" )
process.MessageLogger = cms.Service(
  "MessageLogger", 
   destinations = cms.untracked.vstring ('jobOutput'), # Name of output file
   categories = cms.untracked.vstring('Phase2TrackerDigiProducer','Phase2TrackerFEDBuffer','Phase2TrackerFEDFEDDebug','Phase2TrackerStubProducer'),
   jobOutput = cms.untracked.PSet(
     enableStatistics = cms.untracked.bool(True),
     # Threshold=DEBUG for specified L1Trk categories (=argument of edm::Log*()) 
     # & threshold=ERROR for everything else (since WARNING limit=0).
     threshold = cms.untracked.string("DEBUG"),
     DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     INFO = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     WARNING = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     # Specified categories
     Phase2TrackerDigiProducer = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     Phase2TrackerFEDBuffer = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     Phase2TrackerFEDFEDDebug = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     Phase2TrackerStubProducer = cms.untracked.PSet(limit = cms.untracked.int32(-1))
   )
)
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100))

process.source = cms.Source("PoolSource",
# use this to read testbeam .dat files
# process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring( 'file:digi2raw.root')
)


# use this to use hand-made testbeam cabling
#process.load('TestbeamCabling_cfi')
process.load('DummyCablingTxt_cfi')

process.load('Configuration.Geometry.GeometryExtended2026D98Reco_cff')
# process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerCommissioningDigiProducer_cfi')
# process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerDigiProducer_cfi')

process.load("Configuration.Geometry.GeometryExtended2026D98Reco_cff")
process.load("Configuration.Geometry.GeometryExtended2026D98_cff")
process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerDigiProducer_cfi')
process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerDebugProducer_cfi')
process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerStubProducer_cfi')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
# Temporary change until we switch to D110 geometry.
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

process.GlobalTag = GlobalTag(process.GlobalTag, '140X_mcRun4_realistic_v3', '')

# use these labels instead to run on raw data
#process.Phase2TrackerDigiProducer.ProductLabel = cms.InputTag("rawDataCollector")
#process.Phase2TrackerDebugProducer.ProductLabel = cms.InputTag("rawDataCollector")
#process.Phase2TrackerStubProducer.ProductLabel = cms.InputTag("rawDataCollector")
# process.Phase2TrackerDigiProducer.ProductLabel = cms.InputTag("rawDataCollector")
# process.Phase2TrackerCommissioningDigiProducer.ProductLabel = cms.InputTag("rawDataCollector")
# process.Phase2TrackerDigiProducer.ProductLabel = cms.InputTag("Phase2TrackerDigiToRawProducer")
# process.Phase2TrackerCommissioningDigiProducer.ProductLabel = cms.InputTag("Phase2TrackerDigiToRawProducer")


process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('rawtodigi.root'),
)

# process.p = cms.Path(process.Phase2TrackerDigiProducer*process.Phase2TrackerCommissioningDigiProducer)
#process.p = cms.Path(process.Phase2TrackerDigiProducer*process.Phase2TrackerDebugProducer*process.Phase2TrackerStubProducer)
process.p = cms.Path(process.Phase2TrackerDigiProducer)

process.e = cms.EndPath(process.out)

# # Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
# from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023tilted4021
# #call to customisation function cust_2023tilted4021 imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
# process = cust_2023tilted4021(process)

