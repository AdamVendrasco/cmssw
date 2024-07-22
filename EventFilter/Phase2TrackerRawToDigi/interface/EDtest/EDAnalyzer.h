// interface/MyEDAnalyzer.h
#ifndef EventFilter_Phase2TrackerRawToDigi_MyEDAnalyzer_h
#define EventFilter_Phase2TrackerRawToDigi_MyEDAnalyzer_h

#include "FWCore/Framework/interface/EDAnalyzer.h"

class MyEDAnalyzer : public edm::EDAnalyzer {
public:
    explicit MyEDAnalyzer(const edm::ParameterSet&);
    ~MyEDAnalyzer() override;

private:
    void analyze(const edm::Event&, const edm::EventSetup&) override;
};

#endif

