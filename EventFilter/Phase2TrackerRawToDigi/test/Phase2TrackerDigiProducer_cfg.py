import FWCore.ParameterSet.Config as cms
import sys

process = cms.Process("RawToDigi")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger = cms.Service("MessageLogger",
        destinations  = cms.untracked.vstring('logtrace' ),
        logtrace      = cms.untracked.PSet( threshold  = cms.untracked.string('DEBUG') ),
        debugModules  = cms.untracked.vstring( 'Phase2TrackerDigiProducer', 'Phase2TrackerFEDBuffer', 'Phase2TrackerFEDFEDebug', 'Phase2TrackerStubProducer' )
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10))


process.source = cms.Source("PoolSource",
# use this to read testbeam .dat files
# process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring( 'file://digi2raw.root')
)


# use this to use hand-made testbeam cabling
process.load('TestbeamCabling_cfi')
# process.load('DummyCablingTxt_cfi')

# process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff')
# process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerCommissioningDigiProducer_cfi')
# process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerDigiProducer_cfi')
process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerDigiProducer_cfi')
process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerDebugProducer_cfi')
process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerStubProducer_cfi')

process.load("Configuration.Geometry.GeometryExtended2026D98Reco_cff")
process.load("Configuration.Geometry.GeometryExtended2026D98_cff")

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# use these labels instead to run on raw data
process.Phase2TrackerDigiProducer.ProductLabel = cms.InputTag("rawDataCollector")
process.Phase2TrackerDebugProducer.ProductLabel = cms.InputTag("rawDataCollector")
process.Phase2TrackerStubProducer.ProductLabel = cms.InputTag("rawDataCollector")
# process.Phase2TrackerDigiProducer.ProductLabel = cms.InputTag("rawDataCollector")
# process.Phase2TrackerCommissioningDigiProducer.ProductLabel = cms.InputTag("rawDataCollector")
# process.Phase2TrackerDigiProducer.ProductLabel = cms.InputTag("Phase2TrackerDigiToRawProducer")
# process.Phase2TrackerCommissioningDigiProducer.ProductLabel = cms.InputTag("Phase2TrackerDigiToRawProducer")


process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('rawtodigi.root'),
)

# process.p = cms.Path(process.Phase2TrackerDigiProducer*process.Phase2TrackerCommissioningDigiProducer)
process.p = cms.Path(process.Phase2TrackerDigiProducer*process.Phase2TrackerDebugProducer*process.Phase2TrackerStubProducer)

process.e = cms.EndPath(process.out)

# # Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
# from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023tilted4021
# #call to customisation function cust_2023tilted4021 imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
# process = cust_2023tilted4021(process)

