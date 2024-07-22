#include "CondFormats/DataRecord/interface/Phase2TrackerCablingRcd.h"
#include "CondFormats/SiStripObjects/interface/Phase2TrackerCabling.h"
#include "DataFormats/Common/interface/DetSet.h"
#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/DetId/interface/DetIdCollection.h"
#include "DataFormats/FEDRawData/interface/FEDNumbering.h"
#include "DataFormats/FEDRawData/interface/FEDRawDataCollection.h"
#include "DataFormats/Phase2TrackerDigi/interface/Phase2TrackerDigi.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "DataFormats/Phase2TrackerCluster/interface/Phase2TrackerCluster1D.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDBuffer.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDChannel.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDHeader.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDRawChannelUnpacker.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/Phase2TrackerFEDZSChannelUnpacker.h"
#include "EventFilter/Phase2TrackerRawToDigi/interface/utils.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "CondFormats/DataRecord/interface/Phase2TrackerCablingRcd.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"

namespace Phase2Tracker {

  class Phase2TrackerDigiProducer : public edm::stream::EDProducer<> {
  public:
    /// constructor
    Phase2TrackerDigiProducer(const edm::ParameterSet& pset);
    /// default constructor
    ~Phase2TrackerDigiProducer() override = default;
    void beginRun(edm::Run const&, edm::EventSetup const&) override;
    void produce(edm::Event&, const edm::EventSetup&) override;

  private:
    std::map<int, std::pair<int, int>> stackMap_;
    const edm::ESGetToken<Phase2TrackerCabling, Phase2TrackerCablingRcd> ph2CablingESToken_;
    const edm::ESGetToken<TrackerGeometry, TrackerDigiGeometryRecord> geomToken_;
    const edm::ESGetToken<TrackerTopology, TrackerTopologyRcd> topoToken_;
    const edm::EDGetTokenT<FEDRawDataCollection> token_;
    const edm::EDPutTokenT<edm::DetSetVector<Phase2TrackerDigi>> putToken_;
    const edm::EDPutTokenT<edmNew::DetSetVector<Phase2TrackerCluster1D>> putTokenSparsified_;
    const TrackerGeometry* tkGeom_ = nullptr;
    const TrackerTopology* tTopo_ = nullptr;
    const Phase2TrackerCabling* cabling_ = nullptr;
    class Registry {
    public:
      /// constructor
      Registry(uint32_t aDetid, uint16_t firstStrip, size_t indexInVector, uint16_t numberOfDigis)
          : detid(aDetid), first(firstStrip), index(indexInVector), length(numberOfDigis) {}
      /// < operator to sort registries
      bool operator<(const Registry& other) const {
        return (detid != other.detid ? detid < other.detid : first < other.first);
      }
      /// public data members
      uint32_t detid;
      uint16_t first;
      size_t index;
      uint16_t length;
    };
  };
}  // namespace Phase2Tracker

#include "FWCore/Framework/interface/MakerMacros.h"
typedef Phase2Tracker::Phase2TrackerDigiProducer Phase2TrackerDigiProducer;
DEFINE_FWK_MODULE(Phase2TrackerDigiProducer);

using namespace std;

namespace Phase2Tracker {

Phase2TrackerDigiProducer::Phase2TrackerDigiProducer(const edm::ParameterSet& pset)
       : ph2CablingESToken_(esConsumes<Phase2TrackerCabling, Phase2TrackerCablingRcd, edm::Transition::BeginRun>()),
         //       : ph2CablingESToken_(esConsumes()),
        geomToken_(esConsumes<TrackerGeometry, TrackerDigiGeometryRecord, edm::Transition::BeginRun>()),
        topoToken_(esConsumes<TrackerTopology, TrackerTopologyRcd, edm::Transition::BeginRun>()),
        token_(consumes<FEDRawDataCollection>(pset.getParameter<edm::InputTag>("ProductLabel"))),
        putToken_(produces<edm::DetSetVector<Phase2TrackerDigi>>("Unsparsified")),
        putTokenSparsified_(produces<edmNew::DetSetVector<Phase2TrackerCluster1D>>("Sparsified")) {}

  void Phase2TrackerDigiProducer::beginRun(edm::Run const& run, edm::EventSetup const& es) {
    // fetch cabling from event setup
    cabling_ = &es.getData(ph2CablingESToken_);

    // FIXME: build map of stacks to compensate for missing trackertopology methods
    tkGeom_ = &es.getData(geomToken_);
    tTopo_ = &es.getData(topoToken_);

    for (auto iu = tkGeom_->detUnits().begin(); iu != tkGeom_->detUnits().end(); ++iu) {
      unsigned int detId_raw = (*iu)->geographicalId().rawId();
      DetId detId = DetId(detId_raw);
      if (detId.det() == DetId::Detector::Tracker) {
        // build map of upper and lower for each module
        if (tTopo_->isLower(detId) != 0) {
          stackMap_[tTopo_->stack(detId)].first = detId;
        }
        if (tTopo_->isUpper(detId) != 0) {
          stackMap_[tTopo_->stack(detId)].second = detId;
        }
      }
    }  // end loop on detunits
  }

  void Phase2TrackerDigiProducer::produce(edm::Event& event, const edm::EventSetup& es) {
    std::vector<Registry> proc_work_registry_;
    std::vector<Phase2TrackerDigi> proc_work_digis_;

    // NEW
    auto clusters = std::make_unique<edmNew::DetSetVector<Phase2TrackerCluster1D>>();

    // Retrieve FEDRawData collection
    edm::Handle<FEDRawDataCollection> buffers;
    event.getByToken(token_, buffers);

    // Analyze strip tracker FED buffers in data
    std::vector<int> feds = cabling_->listFeds();
    // Fix from Ian
    //for (size_t fedIndex = Phase2Tracker::FED_ID_MIN; fedIndex <= Phase2Tracker::CMS_FED_ID_MAX; ++fedIndex) {
    for (int fedIndex : feds) {
      const FEDRawData& fed = buffers->FEDData(fedIndex);
      if (fed.size() == 0)
        continue;
      // construct buffer
      Phase2Tracker::Phase2TrackerFEDBuffer buffer(fed.data(), fed.size());
      // Skip FED if buffer is not a valid tracker FEDBuffer
      if (buffer.isValid() == 0) {
        LogTrace("Phase2TrackerDigiProducer") << "[Phase2Tracker::Phase2TrackerDigiProducer::" << __func__ << "]: \n";
        LogTrace("Phase2TrackerDigiProducer") << "Skipping invalid buffer for FED nr " << fedIndex << endl;
        continue;
      }

#ifdef EDM_ML_DEBUG
      std::ostringstream ss;
      ss << " -------------------------------------------- " << endl;
      ss << " buffer debug ------------------------------- " << endl;
      ss << " -------------------------------------------- " << endl;
      ss << " buffer size : " << buffer.bufferSize() << endl;
      ss << " fed id      : " << *fedIndex << endl;
      ss << " -------------------------------------------- " << endl;
      ss << " tracker header debug ------------------------" << endl;
      ss << " -------------------------------------------- " << endl;
      LogTrace("Phase2TrackerDigiProducer") << ss.str();
      ss.clear();
      ss.str("");
#endif

      Phase2TrackerFEDHeader tr_header = buffer.trackerHeader();

#ifdef EDM_ML_DEBUG
      ss << " Version  : " << hex << setw(2) << (int)tr_header.getDataFormatVersion() << endl;
      ss << " Mode     : " << hex << setw(2) << tr_header.getDebugMode() << endl;
      ss << " Type     : " << hex << setw(2) << (int)tr_header.getEventType() << endl;
      ss << " Readout  : " << hex << setw(2) << tr_header.getReadoutMode() << endl;
      ss << " Condition Data : " << (tr_header.getConditionData() ? "Present" : "Absent") << "\n";
      ss << " Data Type      : " << (tr_header.getDataType() ? "Real" : "Fake") << "\n";
      ss << " Status   : " << hex << setw(16) << (int)tr_header.getGlibStatusCode() << endl;
      ss << " FE stat  : ";
      for (int i = MAX_FE_PER_FED - 1; i >= 0; i--) {
        if ((tr_header.frontendStatus())[i]) {
          ss << "1";
        } else {
          ss << "0";
        }
      }
      ss << endl;
      ss << " Nr CBC   : " << hex << setw(16) << (int)tr_header.getNumberOfCBC() << endl;
      ss << " FE/Chip status : ";
      std::vector<Phase2TrackerFEDFEDebug> all_fe_debug = tr_header.CBCStatus();
      std::vector<Phase2TrackerFEDFEDebug>::iterator FE_it;
      for (FE_it = all_fe_debug.begin(); FE_it < all_fe_debug.end(); FE_it++) {
        if (FE_it->IsOn()) {
          ss << " FE L1ID: " << endl;
          ss << "    " << hex << setw(4) << FE_it->getFEL1ID()[0] << dec << endl;
          ss << "    " << hex << setw(4) << FE_it->getFEL1ID()[1] << dec << endl;
          for (int i = 0; i < 16; i++) {
            ss << " Chip Error" << hex << setw(1) << FE_it->getChipError(i) << dec << endl;
            ss << " Chip L1ID " << hex << setw(4) << FE_it->getChipL1ID(i) << dec << endl;
            ss << " Chip PA   " << hex << setw(4) << FE_it->getChipPipelineAddress(i) << dec << endl;
          }
        }
      }
      LogTrace("Phase2TrackerDigiProducer") << ss.str();
      ss.clear();
      ss.str("");
      ss << " -------------------------------------------- " << endl;
      ss << " Payload  ----------------------------------- " << endl;
      ss << " -------------------------------------------- " << endl;
#endif
      // check readout mode
      if (tr_header.getReadoutMode() == READOUT_MODE_PROC_RAW) {
        // loop channels
        int ichan = 0;
        for (int ife = 0; ife < MAX_FE_PER_FED; ife++) {
          for (int icbc = 0; icbc < MAX_CBC_PER_FE; icbc++) {
            const Phase2TrackerFEDChannel& channel = buffer.channel(ichan);
            if (channel.length() > 0) {
              // get detid from cabling
              const Phase2TrackerModule mod = cabling_->findFedCh(std::make_pair(fedIndex, ife));
              uint32_t detid = mod.getDetid();
#ifdef EDM_ML_DEBUG
              ss << dec << " id from cabling : " << detid << endl;
              ss << dec << " reading channel : " << icbc << " on FE " << ife;
              ss << dec << " with length  : " << (int)channel.length() << endl;
#endif
              // container for this channel's digis
              std::vector<Phase2TrackerDigi> stripsTop;
              std::vector<Phase2TrackerDigi> stripsBottom;

              // unpacking data
              // TODO : set Y position in digi as a function of the side of the CBC
              Phase2TrackerFEDRawChannelUnpacker unpacker = Phase2TrackerFEDRawChannelUnpacker(channel);
              while (unpacker.hasData()) {
                if (unpacker.stripOn()) {
                  if (unpacker.stripIndex() % 2) {
                    stripsTop.push_back(Phase2TrackerDigi((int)(STRIPS_PER_CBC * icbc + unpacker.stripIndex()) / 2, 0));
#ifdef EDM_ML_DEBUG
                    ss << "t";
#endif
                  } else {
                    stripsBottom.push_back(
                        Phase2TrackerDigi((int)(STRIPS_PER_CBC * icbc + unpacker.stripIndex()) / 2, 0));
#ifdef EDM_ML_DEBUG
                    ss << "b";
#endif
                  }
                } else {
#ifdef EDM_ML_DEBUG
                  ss << "_";
#endif
                }
                unpacker++;
              }
#ifdef EDM_ML_DEBUG
              ss << endl;
              LogTrace("Phase2TrackerDigiProducer") << ss.str();
              ss.clear();
              ss.str("");
#endif

              // store beginning and end of this digis for this detid and add this registry to the list
              // and store data
              // FIXME : detid scheme should be taken from topology / geometry
              Registry regItemTop(
                  stackMap_[detid].second, STRIPS_PER_CBC * icbc / 2, proc_work_digis_.size(), stripsTop.size());
              proc_work_registry_.push_back(regItemTop);
              proc_work_digis_.insert(proc_work_digis_.end(), stripsTop.begin(), stripsTop.end());
              Registry regItemBottom(
                  stackMap_[detid].first, STRIPS_PER_CBC * icbc / 2, proc_work_digis_.size(), stripsBottom.size());
              proc_work_registry_.push_back(regItemBottom);
              proc_work_digis_.insert(proc_work_digis_.end(), stripsBottom.begin(), stripsBottom.end());
            }
            ichan++;
          }
        }  // end loop on channels
      } else if (tr_header.getReadoutMode() == READOUT_MODE_ZERO_SUPPRESSED) {
        // loop channels
        int ichan = 0;
        for (int ife = 0; ife < MAX_FE_PER_FED; ife++) {
          // get fedid from cabling
          // BODGE FIX from Ian: this crashed, as it assumes all FED input channels are connected to a module. Can we find prettier solution?
          uint32_t detid = 0;
          try {
             const Phase2TrackerModule mod = cabling_->findFedCh(std::make_pair(fedIndex, ife));
             detid = mod.getDetid();
          }
          catch (...) {
            edm::LogWarning("Phase2TrackerDigiProducer")<<"FED with unconnected input channel found, making code unhappy "<<fedIndex<<" "<<ife;
          }

          // container for this module's digis
          std::vector<Phase2TrackerCluster1D> clustersTop;
          std::vector<Phase2TrackerCluster1D> clustersBottom;
          // looping over concentrators (4 virtual concentrators in case of PS)
          for (int iconc = 0; iconc < 4; iconc++) {
            const Phase2TrackerFEDChannel& channel = buffer.channel(ichan);
            if (channel.length() > 0) {
#ifdef EDM_ML_DEBUG
              ss << dec << " id from cabling : " << detid << endl;
              ss << dec << " reading channel : " << iconc << " on FE " << ife;
              ss << dec << " with length  : " << (int)channel.length() << endl;
#endif
              // create appropriate unpacker
              if (channel.dettype() == DET_Son2S) {
                Phase2TrackerFEDZSSon2SChannelUnpacker unpacker = Phase2TrackerFEDZSSon2SChannelUnpacker(channel);
                while (unpacker.hasData()) {
                  unpacker.Merge();
#ifdef EDM_ML_DEBUG
                  ss << std::dec << " Son2S " << (int)unpacker.clusterX() << " " << (int)unpacker.clusterSize() << " "
                     << (int)unpacker.chipId() << endl;
#endif
                  // BODGE FIX from Ian -- Must understand why strip number wrong!
                  if (unpacker.clusterX() < 1016) {
                    if (unpacker.rawX() % 2) {
                       clustersTop.push_back(
                          Phase2TrackerCluster1D(unpacker.clusterX(), unpacker.clusterY(), unpacker.clusterSize()));
                    } else {
                       clustersBottom.push_back(
                          Phase2TrackerCluster1D(unpacker.clusterX(), unpacker.clusterY(), unpacker.clusterSize()));
                    }
                  } else {
                      edm::LogError("Phase2TrackerDigiProducer")<<"MESS UP 2S: STRIP NUMBER OUT OF RANGE  "<<unpacker.clusterX()<<" "<<unpacker.clusterY()<<" "<<unpacker.clusterSize();
                  }                  
                  unpacker++;
                }
              } else if (channel.dettype() == DET_SonPS) {
                Phase2TrackerFEDZSSonPSChannelUnpacker unpacker = Phase2TrackerFEDZSSonPSChannelUnpacker(channel);
                while (unpacker.hasData()) {
                  unpacker.Merge();
#ifdef EDM_ML_DEBUG
                  ss << std::dec << " SonPS " << (int)unpacker.clusterX() << " " << (int)unpacker.clusterSize() << " "
                     << (int)unpacker.chipId() << endl;
#endif
                  // BODGE FIX from Ian -- Must understand why strip number wrong!
                  if (unpacker.clusterX() < 1016) {
                     clustersTop.push_back(Phase2TrackerCluster1D(
                      unpacker.clusterX(), unpacker.clusterY(), unpacker.clusterSize(), unpacker.threshold()));
                  } else {
                     edm::LogError("Phase2TrackerDigiProducer")<<"MESS UP SonPS: STRIP NUMBER OUT OF RANGE  "<<unpacker.clusterX()<<" "<<unpacker.clusterY()<<" "<<unpacker.clusterSize();
                  }
                  unpacker++;
                }
              } else if (channel.dettype() == DET_PonPS) {
                Phase2TrackerFEDZSPonPSChannelUnpacker unpacker = Phase2TrackerFEDZSPonPSChannelUnpacker(channel);
                while (unpacker.hasData()) {
                  unpacker.Merge();
#ifdef EDM_ML_DEBUG
                  ss << std::dec << " PonPS " << (int)unpacker.clusterX() << " " << (int)unpacker.clusterSize() << " "
                     << (int)unpacker.clusterY() << " " << (int)unpacker.chipId() << endl;
#endif
                  // BODGE FIX from Ian -- Must understand why strip number wrong!
                  if (unpacker.clusterX() < 1016) {
                     clustersBottom.push_back(
                      Phase2TrackerCluster1D(unpacker.clusterX(), unpacker.clusterY(), unpacker.clusterSize()));
                  } else {
                     edm::LogError("Phase2TrackerDigiProducer")<<"MESS UP PonPS: STRIP NUMBER OUT OF RANGE  "<<unpacker.clusterX()<<" "<<unpacker.clusterY()<<" "<<unpacker.clusterSize();
                  }
                  unpacker++;
                }
              }
#ifdef EDM_ML_DEBUG
              ss << endl;
              LogTrace("Phase2TrackerDigiProducer") << ss.str();
              ss.clear();
              ss.str("");
#endif
            }  // end reading CBC's channel
            ichan++;
          }  // end loop on channels
          if (detid > 0) {
            std::vector<Phase2TrackerCluster1D>::iterator it;
            {
              // outer detid is defined as inner detid + 1 or module detid + 2
              edmNew::DetSetVector<Phase2TrackerCluster1D>::FastFiller spct(*clusters, stackMap_[detid].second);
              for (it = clustersTop.begin(); it != clustersTop.end(); it++) {
                spct.push_back(*it);
              }
            }
            {
              edmNew::DetSetVector<Phase2TrackerCluster1D>::FastFiller spcb(*clusters, stackMap_[detid].first);
              for (it = clustersBottom.begin(); it != clustersBottom.end(); it++) {
                spcb.push_back(*it);
              }
            }
          }
        }  // end loop on FE
           // store digis in edm collections
      } else {
        // readout modes are checked in getreadoutMode(), so we should never end up here
      }
    }
    // sort and store Unsparsified digis
    std::sort(proc_work_registry_.begin(), proc_work_registry_.end());
    std::vector<edm::DetSet<Phase2TrackerDigi>> sorted_and_merged;
    std::vector<Registry>::iterator it = proc_work_registry_.begin(), it2 = it + 1, end = proc_work_registry_.end();
    while (it < end) {
      sorted_and_merged.push_back(edm::DetSet<Phase2TrackerDigi>(it->detid));
      std::vector<Phase2TrackerDigi>& digis = sorted_and_merged.back().data;
      // first count how many digis we have
      size_t len = it->length;
      for (it2 = it + 1; (it2 != end) && (it2->detid == it->detid); ++it2) {
        len += it2->length;
      }
      // reserve memory
      digis.reserve(len);
      // push them in
      for (it2 = it + 0; (it2 != end) && (it2->detid == it->detid); ++it2) {
        digis.insert(digis.end(), &proc_work_digis_[it2->index], &proc_work_digis_[it2->index + it2->length]);
      }
      it = it2;
    }
    //edm::DetSetVector<Phase2TrackerDigi> proc_raw_dsv( sorted_and_merged, true );
    //pr->swap( proc_raw_dsv );
    //event.put(std::unique_ptr<edm::DetSetVector<Phase2TrackerDigi>>(pr), "Unsparsified");

    //Is this correct?..Jerome did the above
    event.emplace(putToken_, sorted_and_merged, true);

    // store Sparsified Digis
    event.emplace(putTokenSparsified_, std::move(*clusters));
  }
}  // namespace Phase2Tracker
