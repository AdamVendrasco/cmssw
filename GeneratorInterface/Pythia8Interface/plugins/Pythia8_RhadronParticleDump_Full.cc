#include "GeneratorInterface/Pythia8Interface/interface/CustomHook.h"
#include "Pythia8/UserHooks.h"
#include "Pythia8/ParticleData.h"

#include <fstream>
#include <string>
#include <iomanip>
#include <memory>

using namespace Pythia8;

class DumpPythia8RhadronData_Full : public UserHooks {
public:
  DumpPythia8RhadronData_Full(const edm::ParameterSet& pset) { }

  ~DumpPythia8RhadronData_Full() override { }

  bool canVetoProcessLevel() override { return true; }

  bool doVetoProcessLevel(Event& event) override {
    static bool hasDumped = false;
    if (!hasDumped && event.size() > 0) {
      dumpRhadronTable();
      hasDumped = true;
    }
    return false;
  }

private:
  void dumpRhadronTable() {
    std::ofstream outR("Pythia8_RhadronParticleDump_Full.dat");
    if (outR) {
      outR << "Block MASS and RHADRON PROPERTIES  #\n";
      outR << "#  PDG code   mass [GeV]  spin(2S+1)  charge(e)  colType  tau0 [mm]  tauCalc [mm]   particle\n";
      for (auto it = particleDataPtr->begin(); it != particleDataPtr->end(); ++it) {
        std::shared_ptr<ParticleDataEntry> entry = it->second;
        if (!entry) continue;
        const std::string& name = entry->name();
        if (!name.empty() && (name.find("~g") != std::string::npos)) {
          int pdgId         = entry->id();
          double mass_GeV   = entry->m0();
          int spin2Splus1   = entry->spinType();
          double charge     = entry->chargeType() / 3.0;
          int colType       = entry->colType();
          double tau0       = entry->tau0();
          double tauCalc    = entry->tauCalc();

          outR << std::setw(9)  << pdgId
               << std::fixed << std::setprecision(3)
               << std::setw(12) << mass_GeV
               << std::setw(8)  << spin2Splus1
               << std::setw(12) << charge
               << std::setw(9)  << colType
               << std::setw(12) << tau0
               << std::setw(14) << tauCalc
               << "    # " << name << "\n";
        }
      }
      outR.close();
    }
  }
};

// Register with the same (new) class name
REGISTER_USERHOOK(DumpPythia8RhadronData_Full);
