# test/MyEDProducer_cfg.py
import FWCore.ParameterSet.Config as cms

process = cms.Process("MyProducer")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:input.root')
)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))

process.myProducer = cms.EDProducer('MyEDProducer')

process.p = cms.Path(process.myProducer)

