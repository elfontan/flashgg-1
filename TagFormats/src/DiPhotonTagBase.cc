#include "flashgg/MicroAODFormats/interface/DiPhotonCandidate.h"
#include "flashgg/TagFormats/interface/DiPhotonTagBase.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"

using namespace flashgg;

DiPhotonTagBase::DiPhotonTagBase(){
  category_number_ = -1;
}

DiPhotonTagBase::DiPhotonTagBase(edm::Ptr<flashgg::DiPhotonCandidate> diPho,edm::Ptr<DiPhotonMVAResult> mvaRes) {
  mva_result_ = *mvaRes;
  category_number_ = -1;
  dipho_ = diPho;

  /*
  addDaughter(*diPho);
  AddFourMomenta addP4;
  addP4.set(*this);
  mva_result_ = *mvaRes; // copies 
  category_number_ = -1;
  std::cout << " In DiPhotonTagBase::DiPhotonTagBase and my numberOfDaughters() is " << numberOfDaughters() << std::endl;
  const flashgg::DiPhotonCandidate* test = dynamic_cast<const flashgg::DiPhotonCandidate*> (daughter(0));
  std::cout << " test = " << test << std::endl;
  if (test != NULL) std::cout << " test->getSumPt() = " << test->getSumPt() << std::endl;
  std::cout << " daughter(0)->pt() " << daughter(0)->pt() << std::endl;
  const flashgg::DiPhotonCandidate* test2 = dynamic_cast<const flashgg::DiPhotonCandidate*> (daughter(0));
  std::cout << " test2 = " << test2 << std::endl;
  if (test2 != NULL) std::cout << " test2->getSumPt() = " << test2->getSumPt() << std::endl;
  */

}

const DiPhotonCandidate* DiPhotonTagBase::diPhoton() const {
  return dipho_.get();
  /*
  std::cout << " In DiPhotonTagBase::diPhoton, and my numberOfDaughters() is " << numberOfDaughters() << std::endl;
  const flashgg::DiPhotonCandidate* test = dynamic_cast<const flashgg::DiPhotonCandidate*> (daughter(0));
  std::cout << " test = " << test << std::endl;
  if (test != NULL) std::cout << " test->getSumPt() = " << test->getSumPt() << std::endl;
  return dynamic_cast<const flashgg::DiPhotonCandidate*> (daughter(0));
  */
}
const DiPhotonMVAResult DiPhotonTagBase::diPhotonMVA() const {
  return mva_result_;
}

bool DiPhotonTagBase::operator <(DiPhotonTagBase const& b) {
  // For choosing which of two tags OF THE SAME TYPE are of higher priority
  // Comparison of different tags not currently supported - is it ever needed?
  // Overloading may be appropriate if different tags have different priorities

  if (getCategoryNumber() == b.getCategoryNumber()) {
    return (getSumPt() < b.getSumPt()); 
  } else {
    return (getCategoryNumber() < b.getCategoryNumber());
  }
}

bool DiPhotonTagBase::operator >(DiPhotonTagBase const& b) {
  // see operator < above

  if (getCategoryNumber() == b.getCategoryNumber()) {
    return (getSumPt() > b.getSumPt());
  } else {
    return (getCategoryNumber() > b.getCategoryNumber());
  }
}
