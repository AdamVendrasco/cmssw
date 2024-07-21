// interface/MyEDProducer.h
#ifndef EventFilter_Phase2TrackerRawToDigi_MyEDProducer_h
#define EventFilter_Phase2TrackerRawToDigi_MyEDProducer_h

#include "FWCore/Framework/interface/EDProducer.h"

class MyEDProducer : public edm::EDProducer {
public:
    explicit MyEDProducer(const edm::ParameterSet&);
    ~MyEDProducer() override;

private:
    void produce(edm::Event&, const edm::EventSetup&) override;
};

#endif

