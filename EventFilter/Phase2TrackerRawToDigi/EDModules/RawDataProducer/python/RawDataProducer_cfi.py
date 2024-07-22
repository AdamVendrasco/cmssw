import FWCore.ParameterSet.Config as cms
textfile = 'path/to/textfile'


rawDataProducer = cms.EDProducer('RawDataProducer',
  inputFileName = cms.string(textfile)
)

