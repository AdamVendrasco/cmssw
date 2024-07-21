#include "EventFilter/Phase2TrackerRawToDigi/interface/MyEDAnalyzer.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MyEDAnalyzer : public edm::EDAnalyzer {
public:
    explicit MyEDAnalyzer(const edm::ParameterSet&);
    ~MyEDAnalyzer() override;

private:
    void analyze(const edm::Event&, const edm::EventSetup&) override;
};

MyEDAnalyzer::MyEDAnalyzer(const edm::ParameterSet&) {}
MyEDAnalyzer::~MyEDAnalyzer() {}

void MyEDAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Analysis code here
}

DEFINE_FWK_MODULE(MyEDAnalyzer);

