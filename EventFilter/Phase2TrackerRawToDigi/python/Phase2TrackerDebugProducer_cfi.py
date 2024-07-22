import FWCore.ParameterSet.Config as cms

Phase2TrackerDebugProducer = cms.EDProducer(
    'Phase2TrackerDebugProducer',
    ProductLabel = cms.InputTag("Phase2TrackerDigiToRawProducer")
)
