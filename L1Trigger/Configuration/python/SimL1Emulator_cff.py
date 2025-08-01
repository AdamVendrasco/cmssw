import FWCore.ParameterSet.Config as cms

# Defines the L1 Emulator sequence for simulation use-case subsystem emulators
# run on the results of previous (in the hardware chain) subsystem emulator:
#  
#     SimL1Emulator = cms.Sequence(...)
#
# properly configured for the current Era (e.g. Run1, 2015, or 2016).  Also
# configures event setup producers appropriate to the current Era, to handle
# conditions which are not yet available in the GT.
#
# Author List
# Jim Brooke, 24 April 2008
# Vasile Mihai Ghete, 2009
# Jim Brooke, Michael Mulhearn, 2015
# Vladimir Rekovic 2016,2017

# Notes on Inputs:

# ECAL TPG emulator and HCAL TPG run in the simulation sequence in order to be able 
# to use unsuppressed digis produced by ECAL and HCAL simulation, respectively
# in Configuration/StandardSequences/python/Digi_cff.py
# SimCalorimetry.Configuration.SimCalorimetry_cff
# which calls
# SimCalorimetry.Configuration.ecalDigiSequence_cff
# SimCalorimetry.Configuration.hcalDigiSequence_cff

#
# At the moment, there is no emulator available for upgrade HF Trigger Primitives,
# so these missing (required!) inputs are presently ignored by downstream modules.
#

from L1Trigger.L1TCalorimeter.simDigis_cff import *
from L1Trigger.L1TMuon.simDigis_cff import *
from L1Trigger.Configuration.SimL1TechnicalTriggers_cff import *
from L1Trigger.L1TZDC.L1TZDCEmulation_cff import *
from L1Trigger.L1TGlobal.simDigis_cff import *

# define a core which can be extented in customizations:
SimL1EmulatorCoreTask = cms.Task(
    SimL1TCalorimeterTask,
    SimL1TMuonTask,
    SimL1TechnicalTriggersTask,
    L1TZDCEmulationTask,
    SimL1TGlobalTask
)
SimL1EmulatorCore = cms.Sequence(SimL1EmulatorCoreTask)

SimL1EmulatorTask = cms.Task(SimL1EmulatorCoreTask)
SimL1Emulator = cms.Sequence( SimL1EmulatorTask )

# 
# Emulators are configured from DB (GlobalTags)
#

from L1Trigger.L1TGlobal.GlobalParameters_cff import *

# 2017 EMTF and TwinMux emulator use payloads from DB, not yet in GT,
# soon to be removed when availble in GTs
from L1Trigger.L1TTwinMux.fakeTwinMuxParams_cff import *

_phase2_siml1emulator = SimL1EmulatorTask.copy()

# ########################################################################
# ########################################################################
#
# Phase-2 
#
# ########################################################################
# ########################################################################

# ########################################################################
# Phase-2 Trigger Primitives
# ########################################################################
from L1Trigger.DTTriggerPhase2.CalibratedDigis_cfi import *
CalibratedDigis.dtDigiTag = "simMuonDTDigis"
_phase2_siml1emulator.add(CalibratedDigis)
from L1Trigger.DTTriggerPhase2.dtTriggerPhase2PrimitiveDigis_cfi import *
_phase2_siml1emulator.add(dtTriggerPhase2PrimitiveDigis)
from L1Trigger.DTTriggerPhase2.dtTriggerPhase2Showers_cfi import *
_phase2_siml1emulator.add(dtTriggerPhase2Shower)

# HGCAL TP 
# ########################################################################
from  L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff import *
_phase2_siml1emulator.add(L1THGCalTriggerPrimitivesTask)
 
# ########################################################################
# Phase 2 L1T
# ########################################################################

# Barrel and EndCap EGamma
# ########################################################################
from L1Trigger.L1CaloTrigger.l1tEGammaCrystalsEmulatorProducer_cfi import *
_phase2_siml1emulator.add(l1tEGammaClusterEmuProducer)

from L1Trigger.L1CaloTrigger.l1tPhase2L1CaloEGammaEmulator_cfi import *
_phase2_siml1emulator.add(l1tPhase2L1CaloEGammaEmulator)

from L1Trigger.L1CaloTrigger.l1tPhase2L1CaloEGammaEmulator_cfi import *
_phase2_siml1emulator.add(l1tPhase2L1CaloEGammaEmulator)

from L1Trigger.L1CaloTrigger.l1tPhase2CaloPFClusterEmulator_cfi import *
_phase2_siml1emulator.add(l1tPhase2CaloPFClusterEmulator)

from L1Trigger.L1CaloTrigger.l1tPhase2GCTBarrelToCorrelatorLayer1Emulator_cfi import *
_phase2_siml1emulator.add(l1tPhase2GCTBarrelToCorrelatorLayer1Emulator)

# Barrel and EndCap CaloJet/HT/NNCaloTau
# ########################################################################
# ----    Produce the calibrated tower collection combining Barrel, HGCal, HF
from L1Trigger.L1CaloTrigger.l1tTowerCalibrationProducer_cfi import *
l1tTowerCalibration = l1tTowerCalibrationProducer.clone(
  L1HgcalTowersInputTag = ("l1tHGCalTowerProducer","HGCalTowerProcessor",""),
  l1CaloTowers = ("l1tEGammaClusterEmuProducer","L1CaloTowerCollection","")
)
# ----    Produce the simulated L1CaloJets
from L1Trigger.L1CaloTrigger.l1tCaloJetProducer_cfi import *
l1tCaloJet = l1tCaloJetProducer.clone (
    l1CaloTowers = ("l1tTowerCalibration","L1CaloTowerCalibratedCollection",""),
    L1CrystalClustersInputTag = ("l1tEGammaClusterEmuProducer", "","")
)
# ----    Produce the simulated CaloJet HTT Sums
from L1Trigger.L1CaloTrigger.l1tCaloJetHTTProducer_cfi import *
l1tCaloJetHTT = l1tCaloJetHTTProducer.clone(
    BXVCaloJetsInputTag = ("L1CaloJet", "CaloJets") 
)
# ----    Produce the NNCaloTau
from L1Trigger.L1CaloTrigger.l1tNNCaloTauProducer_cfi import *
_phase2_siml1emulator.add(l1tNNCaloTauProducer)

from L1Trigger.L1CaloTrigger.l1tNNCaloTauEmulator_cfi import *
_phase2_siml1emulator.add(l1tNNCaloTauEmulator)

# ---- Produce the emulated CaloJets and Taus
from L1Trigger.L1CaloTrigger.l1tPhase2CaloJetEmulator_cff import *

_phase2_siml1emulator.add(l1tTowerCalibration)
_phase2_siml1emulator.add(l1tCaloJet)
_phase2_siml1emulator.add(l1tCaloJetHTT)
_phase2_siml1emulator.add(l1tCaloJetsTausTask)

# Overlap and EndCap Muon Track Finder
# ########################################################################
from L1Trigger.L1TMuonOverlapPhase2.simOmtfPhase2Digis_cfi import *
_phase2_siml1emulator.add(simOmtfPhase2Digis)

from L1Trigger.L1TMuonEndCapPhase2.simCscTriggerPrimitiveDigisForEMTF_cfi import *
from L1Trigger.L1TMuonEndCapPhase2.rpcRecHitsForEMTF_cfi import *
from L1Trigger.L1TMuonEndCapPhase2.simEmtfDigisPhase2_cfi import *

_phase2_siml1emulator.add(simCscTriggerPrimitiveDigisForEMTF)
_phase2_siml1emulator.add(rpcRecHitsForEMTF)
_phase2_siml1emulator.add(simEmtfDigisPhase2)

# ########################################################################
# Phase-2 L1T - TrackTrigger dependent modules
# ########################################################################

from L1Trigger.L1TTrackMatch.l1tGTTInputProducer_cfi import *
from L1Trigger.L1TTrackMatch.l1tTrackSelectionProducer_cfi import *
from L1Trigger.L1TTrackMatch.l1tTrackVertexAssociationProducer_cfi import *
from L1Trigger.VertexFinder.l1tVertexProducer_cfi import *
from L1Trigger.L1TTrackMatch.DisplacedVertexProducer_cfi import *

# Track Conversion, Track Selection, Vertex Finding
_phase2_siml1emulator.add(l1tGTTInputProducer)
_phase2_siml1emulator.add(l1tGTTInputProducerExtended)
_phase2_siml1emulator.add(l1tTrackSelectionProducer)
_phase2_siml1emulator.add(l1tTrackSelectionProducerExtended)
_phase2_siml1emulator.add(l1tVertexFinder)
_phase2_siml1emulator.add(l1tVertexProducer)
_phase2_siml1emulator.add(l1tVertexFinderEmulator)
_phase2_siml1emulator.add(DisplacedVertexProducer) #Should rename to l1tDisplacedVertexProducer

# Emulated GMT Muons (Tk + Stub, Tk + MuonTFT, StandaloneMuon)
# ########################################################################
from L1Trigger.Phase2L1GMT.gmt_cfi  import *
l1tStubsGmt = gmtStubs.clone()
l1tKMTFMuonsGmt = gmtKMTFMuons.clone(
  stubs      = cms.InputTag('l1tStubsGmt','kmtf'),
)
l1tFwdMuonsGmt = gmtFwdMuons.clone(
    stubs  = 'l1tStubsGmt:tps'
)
l1tSAMuonsGmt = gmtSAMuons.clone(
  barrelPrompt      = cms.InputTag('l1tKMTFMuonsGmt:prompt'),
  barrelDisp        = cms.InputTag('l1tKMTFMuonsGmt:displaced'),
  forwardPrompt     = cms.InputTag('l1tFwdMuonsGmt:prompt'),
  forwardDisp     = cms.InputTag('l1tFwdMuonsGmt:displaced')
)
l1tTkMuonsGmt = gmtTkMuons.clone(
    srcStubs  = 'l1tStubsGmt:tps'
)
_phase2_siml1emulator.add( l1tStubsGmt )
_phase2_siml1emulator.add( l1tKMTFMuonsGmt )
_phase2_siml1emulator.add( l1tFwdMuonsGmt )
_phase2_siml1emulator.add( l1tSAMuonsGmt )
_phase2_siml1emulator.add( l1tTkMuonsGmt )

# Tracker Objects
# ########################################################################
from L1Trigger.L1TTrackMatch.l1tTrackJets_cfi import *
from L1Trigger.L1TTrackMatch.l1tTrackFastJets_cfi import *
from L1Trigger.L1TTrackMatch.l1tTrackerEtMiss_cfi import *
from L1Trigger.L1TTrackMatch.l1tTrackerHTMiss_cfi import *

#Selected and Associated tracks for Jets and Emulated Jets
_phase2_siml1emulator.add(l1tTrackSelectionProducerForJets)
_phase2_siml1emulator.add(l1tTrackSelectionProducerExtendedForJets)
_phase2_siml1emulator.add(l1tTrackVertexAssociationProducerForJets)
_phase2_siml1emulator.add(l1tTrackVertexAssociationProducerExtendedForJets)

#Selected and Associated tracks for EtMiss and Emulated EtMiss
_phase2_siml1emulator.add(l1tTrackSelectionProducerForEtMiss)
_phase2_siml1emulator.add(l1tTrackSelectionProducerExtendedForEtMiss)
_phase2_siml1emulator.add(l1tTrackVertexAssociationProducerForEtMiss)
_phase2_siml1emulator.add(l1tTrackVertexAssociationProducerExtendedForEtMiss)

#Track Jets, Track Only Et Miss, Track Only HT Miss
_phase2_siml1emulator.add(l1tTrackJets)
_phase2_siml1emulator.add(l1tTrackJetsExtended)
_phase2_siml1emulator.add(l1tTrackFastJets)
_phase2_siml1emulator.add(l1tTrackerEtMiss)
_phase2_siml1emulator.add(l1tTrackerHTMiss)

#Emulated Track Jets, Track Only Et Miss, Track Only HT Miss
from L1Trigger.L1TTrackMatch.l1tTrackJetsEmulation_cfi import *
_phase2_siml1emulator.add(l1tTrackJetsEmulation)
_phase2_siml1emulator.add(l1tTrackJetsExtendedEmulation)

from L1Trigger.L1TTrackMatch.l1tTrackerEmuEtMiss_cfi import *
_phase2_siml1emulator.add(l1tTrackerEmuEtMiss)

from L1Trigger.L1TTrackMatch.l1tTrackerEmuHTMiss_cfi import *
_phase2_siml1emulator.add(l1tTrackerEmuHTMiss)
_phase2_siml1emulator.add(l1tTrackerEmuHTMissExtended)

from L1Trigger.L1TTrackMatch.l1tTrackTripletEmulation_cfi import *
_phase2_siml1emulator.add(l1tTrackTripletEmulation)


# PF Candidates
# ########################################################################
from L1Trigger.Phase2L1ParticleFlow.l1ctLayer1_cff import *
from L1Trigger.Phase2L1ParticleFlow.l1ctLayer2EG_cff import *
_phase2_siml1emulator.add(L1TLayer1TaskInputsTask, L1TLayer1Task, L1TLayer2EGTask)

# PF Jet
# ########################################################################
# Describe here l1PFJets_a_la_Phase1 Task
# ###############################
from L1Trigger.L1CaloTrigger.Phase1L1TJets_9x9_cff import *
L1TPFJetsPhase1Task_9x9 = cms.Task( l1tPhase1JetProducer9x9, l1tPhase1JetCalibrator9x9, l1tPhase1JetSumsProducer9x9)
_phase2_siml1emulator.add(L1TPFJetsPhase1Task_9x9)

from L1Trigger.L1CaloTrigger.Phase1L1TJets_9x9trimmed_cff import *
L1TPFJetsPhase1Task_9x9trimmed = cms.Task(  l1tPhase1JetProducer9x9trimmed, l1tPhase1JetCalibrator9x9trimmed, l1tPhase1JetSumsProducer9x9trimmed)
_phase2_siml1emulator.add(L1TPFJetsPhase1Task_9x9trimmed)

from L1Trigger.Phase2L1ParticleFlow.l1tHPSPFTauProducer_cfi import *
_phase2_siml1emulator.add(l1tHPSPFTauProducer)

# PF MET
# ########################################################################
from L1Trigger.Phase2L1ParticleFlow.l1pfJetMet_cff import *
_phase2_siml1emulator.add(L1TPFJetsTask)
_phase2_siml1emulator.add(L1TPFJetsEmulationTask)

from L1Trigger.Phase2L1ParticleFlow.l1tMETPFProducer_cfi import *
_phase2_siml1emulator.add(l1tMETPFProducer)
_phase2_siml1emulator.add(l1tMETMLProducer)


# NNTaus
# ########################################################################
from L1Trigger.Phase2L1ParticleFlow.L1NNTauProducer_cff import *
_phase2_siml1emulator.add(l1tNNTauProducerPuppi)

# SC4NGJets
# ########################################################################
from L1Trigger.Phase2L1ParticleFlow.l1tSC4NGJetProducer_cfi import *
_phase2_siml1emulator.add(l1tSC4NGJetProducer)

# BJets
# ########################################################################
from L1Trigger.Phase2L1ParticleFlow.L1BJetProducer_cff import *
_phase2_siml1emulator.add(L1TBJetsTask)

# LLPJets
# ########################################################################
from L1Trigger.Phase2L1ParticleFlow.TOoLLiPProducer_cff import *
_phase2_siml1emulator.add(L1TTOoLLiPTask)

# --> add modules
from Configuration.Eras.Modifier_phase2_trigger_cff import phase2_trigger
phase2_trigger.toReplaceWith( SimL1EmulatorTask , _phase2_siml1emulator)
