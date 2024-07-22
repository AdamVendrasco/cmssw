import FWCore.ParameterSet.Config as cms

Phase2TrackerStubProducer = cms.EDProducer(
    'Phase2TrackerStubProducer',
    ProductLabel = cms.InputTag("Phase2TrackerDigiToRawProducer")
)
