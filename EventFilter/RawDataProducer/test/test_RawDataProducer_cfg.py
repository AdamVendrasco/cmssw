import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

# Loads the configuration for your module
process.load("EventFilter.RawDataProducer.RawDataProducer_cfi")

# Configured the MessageLogger to send messages to stdout and stderr
process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('cout', 'cerr'),
    cout = cms.untracked.PSet(threshold = cms.untracked.string('INFO')),
    cerr = cms.untracked.PSet(threshold = cms.untracked.string('ERROR')
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Configured the source of the events (none in this case)
process.source = cms.Source("EmptySource")

process.p = cms.Path(process.rawDataProducer)

