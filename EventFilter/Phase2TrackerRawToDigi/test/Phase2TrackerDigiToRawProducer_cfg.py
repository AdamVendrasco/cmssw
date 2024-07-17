import FWCore.ParameterSet.Config as cms
import sys

process = cms.Process("DigiToRaw")
from MCsamples.RelVal_1400_D98.PU0_DisplacedSingleMuFlatPt1p5To8_cfi import *
inputMC = getCMSdataFromCards()
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger = cms.Service("MessageLogger",
        destinations  = cms.untracked.vstring('DigiToRawlogtrace' ),
        DigiToRawlogtrace      = cms.untracked.PSet( threshold  = cms.untracked.string('DEBUG') ),
        debugModules  = cms.untracked.vstring( 'Phase2TrackerDigiToRawProducer', 'Phase2TrackerFEDBuffer' )
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

# Input source
process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring( 'root://xrootd.ba.infn.it/'+sys.argv[-1])
    fileNames = cms.untracked.vstring(inputMC)
)

process.load('DummyCablingTxt_cfi')
process.load('EventFilter.Phase2TrackerRawToDigi.Phase2TrackerDigiToRawProducer_cfi')
process.Phase2TrackerDigiToRawProducer.ProductLabel = cms.InputTag("siPhase2Clusters")

process.load("Configuration.Geometry.GeometryExtended2026D98Reco_cff")
process.load("Configuration.Geometry.GeometryExtended2026D98_cff")

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
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
# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
#from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023tilted4021
#call to customisation function cust_2023tilted4021 imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
#process = cust_2023tilted4021(process)
