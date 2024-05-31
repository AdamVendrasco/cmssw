import FWCore.ParameterSet.Config as cms
import EventFilter.HGCalRawToDigi.HGCalRawToDigiFake_cfi

process = cms.Process("RAWTODIGI")

#Just an open data cms root file
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16MiniAODv2/ZZ_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/120000/BB3EB5DF-6B33-E44E-8F0F-646EF7A48DC1.root'
    )
)

hgcalDigis = EventFilter.HGCalRawToDigi.HGCalRawToDigiFake_cfi.HGCalRawToDigiFake.clone()

import EventFilter.HGCalRawToDigi.HFNoseRawToDigiFake_cfi

hfnoseDigis = EventFilter.HGCalRawToDigi.HFNoseRawToDigiFake_cfi.HFNoseRawToDigiFake.clone()

from Configuration.ProcessModifiers.premix_stage2_cff import premix_stage2
premix_stage2.toModify(hgcalDigis,
    eeDigis = 'mixData:HGCDigisEE',
    fhDigis = 'mixData:HGCDigisHEfront',
    bhDigis = 'mixData:HGCDigisHEback',
)
