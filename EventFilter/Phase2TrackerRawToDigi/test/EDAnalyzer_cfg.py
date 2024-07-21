# test/MyEDAnalyzer_cfg.py
import FWCore.ParameterSet.Config as cms

process = cms.Process("MyAnalyzer")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:input.root')
)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))

process.myAnalyzer = cms.EDAnalyzer('MyEDAnalyzer')

process.p = cms.Path(process.myAnalyzer)

