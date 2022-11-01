import FWCore.ParameterSet.Config as cms

from DQMOffline.Alignment.DiMuonMassBiasClient_cfi import DiMuonMassBiasClient as diMuonMassBiasClient

# Z-> mm
__selectionName = 'TkAlDiMuonAndVertex'
ALCARECOTkAlZMuMuMassBiasClient = diMuonMassBiasClient.clone(
    FolderName = "AlCaReco/"+__selectionName,
    fitBackground = True,
    useRooCMSShape = True,
    fit_par = dict(mean_par = [90., 89., 100.],    # parameters of the mass pole
                   width_par = [2.49, 2.48, 2.50], # natural width of the Z
                   sigma_par = [1.5, 0.0, 10.0])   # detector smearing
)

alcaTkAlZMuMuBiasClients = cms.Sequence(ALCARECOTkAlZMuMuMassBiasClient)

# J/psi -> mm
__selectionName = 'TkAlJpsiMuMu'
ALCARECOTkAlJpsiMuMuMassBiasClient = diMuonMassBiasClient.clone(
    FolderName = "AlCaReco/"+__selectionName,
    fitBackground = True,
    useRooCMSShape = False,
    fit_par = dict(mean_par = [3.09, 2.7, 3.4],   # parameters of the mass pole
                   width_par = [1.0, 0.0, 5.0],
                   sigma_par = [1.0, 0.0, 5.0])
)

alcaTkAlJpsiMuMuBiasClients = cms.Sequence(ALCARECOTkAlJpsiMuMuMassBiasClient)

# Upsilon -> mm
__selectionName = 'TkAlUpsilonMuMu'
ALCARECOTkAlUpsilonMuMuMassBiasClient = diMuonMassBiasClient.clone(
    FolderName = "AlCaReco/"+__selectionName,
    fitBackground = True,
    useRooCMSShape = False,
    fit_par = dict(mean_par = [9.46, 8.9, 9.9],  # parameters of the mass pole
                   width_par = [1.0, 0.0, 5.0],
                   sigma_par = [1.0, 0.0, 5.0])
)

alcaTkAlUpsilonMuMuBiasClients = cms.Sequence(ALCARECOTkAlUpsilonMuMuMassBiasClient)
