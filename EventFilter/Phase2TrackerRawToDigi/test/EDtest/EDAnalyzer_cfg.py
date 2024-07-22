# test/MyEDAnalyzer_cfg.py
import FWCore.ParameterSet.Config as cms
from MCsamples.RelVal_1400_D98.PU0_DisplacedSingleMuFlatPt1p5To8_cfi import *
inputMC = getCMSdataFromCards()

process = cms.Process("MyAnalyzer")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(inputMC)
)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))

process.myAnalyzer = cms.EDAnalyzer('MyEDAnalyzer')

process.p = cms.Path(process.myAnalyzer)









