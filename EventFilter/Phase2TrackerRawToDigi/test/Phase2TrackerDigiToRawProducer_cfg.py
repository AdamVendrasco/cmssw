import FWCore.ParameterSet.Config as cms
import sys

process = cms.Process("DigiToRaw")
#process.load( "FWCore.MessageLogger.MessageLogger_cfi" )
process.MessageLogger = cms.Service(
  "MessageLogger", 
   destinations = cms.untracked.vstring ('jobOutput'), # Name of output file
   categories = cms.untracked.vstring('Phase2TrackerDigiToRawProducer','Phase2TrackerDigiProducer','Phase2TrackerFEDBuffer'),
   jobOutput = cms.untracked.PSet(
     enableStatistics = cms.untracked.bool(True),
     # Threshold=DEBUG for specified L1Trk categories (=argument of edm::Log*()) 
     # & threshold=ERROR for everything else (since WARNING limit=0).
     threshold = cms.untracked.string("DEBUG"),
     DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     INFO = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     WARNING = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     # Specified categories
     Phase2TrackerDigiToRawProducer = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     Phase2TrackerDigiProducer = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     Phase2TrackerFEDBuffer = cms.untracked.PSet(limit = cms.untracked.int32(-1))
   )
)

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("/store/relval/CMSSW_14_0_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_133X_mcRun4_realistic_v1_STD_2026D98_PU200_RV229-v1/2580000/0b2b0b0b-f312-48a8-9d46-ccbadc69bbfd.root")
)

process.load('DummyCablingTxt_cfi')
process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerDigiToRawProducer_cfi')
process.Phase2TrackerDigiToRawProducer.ProductLabel = cms.InputTag("siPhase2Clusters")

process.load('Configuration.Geometry.GeometryExtended2026D98Reco_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
# Temporary change until we switch to D110 geometry.
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '140X_mcRun4_realistic_v3', '')

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('digi2raw.root'),
    outputCommands = cms.untracked.vstring(
      # 'drop *',
      'keep *_Phase2TrackerDigiToRawProducer_*_*'
      )
    )

process.p = cms.Path(process.Phase2TrackerDigiToRawProducer)

process.e = cms.EndPath(process.out)

# Automatic addition of the customisation function from #SLHCUpgradeSimulations.Configuration.combinedCustoms
#from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023tilted4021
#call to customisation function cust_2023tilted4021 imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
#process = cust_2023tilted4021(process)

