// src/MyEDProducer.cc
#include "EventFilter/Phase2TrackerRawToDigi/interface/MyEDProducer.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MyEDProducer : public edm::EDProducer {
public:
    explicit MyEDProducer(const edm::ParameterSet&);
    ~MyEDProducer() override;

private:
    void produce(edm::Event&, const edm::EventSetup&) override;
};

MyEDProducer::MyEDProducer(const edm::ParameterSet&) {
    // Define your product here
}
MyEDProducer::~MyEDProducer() {}

void MyEDProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Your production code here
}

DEFINE_FWK_MODULE(MyEDProducer);

