// -*- C++ -*-
//
// Package:    EDModules/RawDataProducer
// Class:      RawDataProducer
//
/**\class RawDataProducer RawDataProducer.cc EDModules/RawDataProducer/plugins/RawDataProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Adam Vendrasco
//         Created:  Mon, 22 Jul 2024 07:54:16 GMT
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include <fstream>
#include <string>
#include <vector>

//
// class declaration
//

class RawDataProducer : public edm::stream::EDProducer<> {
public:
  explicit RawDataProducer(const edm::ParameterSet&);
  ~RawDataProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginStream(edm::StreamID) override;
  void produce(edm::Event&, const edm::EventSetup&) override;
  void endStream() override;

  std::string inputFileName_; // Declare the member variable here
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
RawDataProducer::RawDataProducer(const edm::ParameterSet& iConfig):
    inputFileName_(iConfig.getParameter<std::string>("inputFileName")) // Initialize the member variable
{
  //register your products
  produces<std::vector<int>>("rawData");
}

RawDataProducer::~RawDataProducer() {
  // do anything here that needs to be done at destruction time
  // (e.g. close files, deallocate resources etc.)
  //
  // please remove this method altogether if it would be left empty
}

//
// member functions
//

// ------------ method called to produce the data  ------------
void RawDataProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;

  // Read the raw data from the text file
  std::ifstream inputFile(inputFileName_);
  std::vector<int> rawData;
  int value;
  while (inputFile >> value) {
    rawData.push_back(value);
  }

  // Create the product
  auto rawDataProduct = std::make_unique<std::vector<int>>(rawData);

  // Put the product into the event
  iEvent.put(std::move(rawDataProduct), "rawData");
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void RawDataProducer::beginStream(edm::StreamID) {
  // please remove this method if not needed
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void RawDataProducer::endStream() {
  // please remove this method if not needed
}

// ------------ method called when starting to processes a run  ------------
/*
void
RawDataProducer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void
RawDataProducer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void
RawDataProducer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
RawDataProducer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void RawDataProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RawDataProducer);

