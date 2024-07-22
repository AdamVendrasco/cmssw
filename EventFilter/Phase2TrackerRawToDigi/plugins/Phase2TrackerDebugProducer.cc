#include "CondFormats/DataRecord/interface/Phase2TrackerCablingRcd.h"
#include "CondFormats/SiStripObjects/interface/Phase2TrackerCabling.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"
#include "DataFormats/DetId/interface/DetIdCollection.h"
#include "DataFormats/FEDRawData/interface/FEDRawDataCollection.h"
#include "DataFormats/FEDRawData/interface/FEDNumbering.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDBuffer.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDChannel.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDHeader.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDFEDebug.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/utils.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"
#include <sstream>
#include <iomanip>
#include <ext/algorithm>

using namespace std;

namespace Phase2Tracker {

  class Phase2TrackerDebugProducer : public edm::stream::EDProducer<> {
  public:
    Phase2TrackerDebugProducer(const edm::ParameterSet& pset);
    ~Phase2TrackerDebugProducer() override = default;
    virtual void beginRun(edm::Run const&, edm::EventSetup const&);
    virtual void produce(edm::Event&, const edm::EventSetup&) override;

  private:
    const edm::ESGetToken<Phase2TrackerCabling, Phase2TrackerCablingRcd> ph2CablingESToken_;
    edm::EDGetTokenT<FEDRawDataCollection> token_;
    const Phase2TrackerCabling* cabling_ = nullptr;
    std::map<int, std::pair<int, int>> stackMap_;
    DetIdCollection detids_;
  };

  Phase2TrackerDebugProducer::Phase2TrackerDebugProducer(const edm::ParameterSet& pset)
      : ph2CablingESToken_(esConsumes<Phase2TrackerCabling, Phase2TrackerCablingRcd, edm::Transition::BeginRun>()) {
    // define product
    produces<edmNew::DetSetVector<Phase2TrackerFEDFEDebug>>("Debugs");
    token_ = consumes<FEDRawDataCollection>(pset.getParameter<edm::InputTag>("ProductLabel"));
  }

  void Phase2TrackerDebugProducer::beginRun(edm::Run const& run, edm::EventSetup const& es) {
    cabling_ = &es.getData(ph2CablingESToken_);
  }

  void Phase2TrackerDebugProducer::produce(edm::Event& event, const edm::EventSetup& es) {
    std::unique_ptr<edmNew::DetSetVector<Phase2TrackerFEDFEDebug>> debugs(
        new edmNew::DetSetVector<Phase2TrackerFEDFEDebug>());
    // Retrieve FEDRawData collection
    edm::Handle<FEDRawDataCollection> buffers;
    event.getByToken(token_, buffers);

    // Analyze strip tracker FED buffers in data
    std::vector<int> feds = cabling_->listFeds();
    std::vector<int>::iterator fedIndex;
    for (fedIndex = feds.begin(); fedIndex != feds.end(); ++fedIndex) {
      const FEDRawData& fed = buffers->FEDData(*fedIndex);
      if (fed.size() == 0)
        continue;
      // construct buffer
      Phase2Tracker::Phase2TrackerFEDBuffer buffer(fed.data(), fed.size());
      // Skip FED if buffer is not a valid tracker FEDBuffer
      if (buffer.isValid() == 0) {
        LogTrace("Phase2TrackerDebugProducer") << "[Phase2Tracker::Phase2TrackerDebugProducer::" << __func__ << "]: \n";
        LogTrace("Phase2TrackerDebugProducer") << "Skipping invalid buffer for FED nr " << *fedIndex << endl;
        continue;
      }
      std::vector<Phase2TrackerFEDFEDebug> all_fed_debugs = buffer.trackerHeader().CBCStatus();
      std::vector<bool> fe_status = buffer.trackerHeader().frontendStatus();
      // loop on FE
      for (int ife = 0; ife < MAX_FE_PER_FED; ife++) {
        if (fe_status[ife]) {
          // get fedid from cabling
          const Phase2TrackerModule mod = cabling_->findFedCh(std::make_pair(*fedIndex, ife));
          uint32_t detid = mod.getDetid();
          // fill one debug using fastfiller
          edmNew::DetSetVector<Phase2TrackerFEDFEDebug>::FastFiller spct(*debugs, detid);
          spct.push_back(all_fed_debugs[ife]);
        }
      }  // end loop on FE
    }    // en loop on FED
    // store debugs
    event.put(std::move(debugs), "Debugs");
  }
}  // namespace Phase2Tracker

#include "FWCore/Framework/interface/MakerMacros.h"
typedef Phase2Tracker::Phase2TrackerDebugProducer Phase2TrackerDebugProducer;
DEFINE_FWK_MODULE(Phase2TrackerDebugProducer);
