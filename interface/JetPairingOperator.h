
#pragma once

#include <algorithm>
#include <math.h>

#include "BaseOperator.h"
#include "Event.h"

#include "combinations.h"


inline void dijet_pairing_simple (std::vector<alp::Jet> & jets,
                           std::size_t n_fix_jets) {

  typedef std::vector<std::size_t>::iterator It;

  std::vector<std::size_t> jet_is(jets.size());
  std::iota(jet_is.begin(), jet_is.end(), 0);
  
  std::vector<std::size_t> min_is(jet_is.begin(), jet_is.end());
  double min_v = 100000 ;
  
  // iterate over all jet combinations for the non fixed jet 
  for_each_combination(jet_is.begin()+n_fix_jets, jet_is.begin()+4,
                       jet_is.end(), [&](It fo, It lo) -> bool {
    // iterate over all dijet pickings 
  	for_each_combination(jet_is.begin(), jet_is.begin()+2, 
                         jet_is.begin()+3, [&](It fi, It li) -> bool {
      // this could be done faster with VectorUtil function                   
  		double mass_one = (jets.at(*jet_is.begin()).p4_+ jets.at(*(jet_is.begin()+1)).p4_).M();
  		double mass_two = (jets.at(*(jet_is.begin()+2)).p4_+ jets.at(*(jet_is.begin()+3)).p4_).M();
      double mass_diff = std::abs(mass_one-mass_two);
      if ( mass_diff < min_v) {
        min_v = mass_diff; 
        min_is.clear();
        if (mass_one > mass_two) {
          min_is.insert(min_is.begin(), jet_is.begin(), jet_is.end());
        } else {
          min_is.insert(min_is.begin(), jet_is.begin()+2, jet_is.begin()+4);
          min_is.insert(min_is.begin()+2, jet_is.begin(), jet_is.begin()+2);
          min_is.insert(min_is.begin()+4, jet_is.begin()+4, jet_is.end());
        }
      }
      return false;
  	});
    return false;
  });
  
  // the fist pair of elements of the min_is variable are
  // the indexes of the fist pair and the folowign two
  // are indexes for the second pair 
  
  // use same order for jet collection (copy overhead as it is now)
  auto ordered_jets = std::vector<alp::Jet>{}; 
  for (std::size_t i = 0; i < jets.size(); i++ ) {
    ordered_jets.emplace_back(jets.at(min_is.at(i)));
  }
  for (std::size_t i = 0; i < jets.size(); i++ ) {
    jets.at(i) = ordered_jets.at(i);
  }  
}
 

template <class EventClass> class JetPairingOperator : public BaseOperator<EventClass> {

  public:

    typedef std::vector<std::size_t>::iterator It;
    std::size_t n_fix_jets_;
    std::string disc_;


    JetPairingOperator( std::size_t n_fix_jets = 3, 
                        std::string disc = "pfCombinedInclusiveSecondaryVertexV2BJetTags") :
    n_fix_jets_(n_fix_jets),
    disc_(disc) {}
    virtual ~JetPairingOperator() {}

    virtual bool process( EventClass & ev ) {

      dijet_pairing_simple(ev.jets_, n_fix_jets_);        

      // fill dijet objects
      ev.dijets_.clear();
      ev.dijets_.emplace_back(ev.jets_.at(0).p4_ + ev.jets_.at(1).p4_);
      ev.dijets_.emplace_back(ev.jets_.at(2).p4_ + ev.jets_.at(3).p4_);

      // fill dijet objects
      ev.dihiggs_.clear();
      ev.dihiggs_.emplace_back(ev.dijets_.at(0) + ev.dijets_.at(1));
     
      // sort in discriminator order 
      auto comparator = [&](alp::Jet a, alp::Jet b){ 
        return a.disc(disc_) < b.disc(disc_); };

      ev.free_is_.clear();
      if (n_fix_jets_ != 4) ev.free_is_.emplace_back(3);
      if (n_fix_jets_ == 4) ev.free_is_.emplace_back(
          std::distance(ev.jets_.begin(), std::min_element(ev.jets_.begin(), ev.jets_.begin()+4,comparator)));

      return true;
    }


    virtual std::string get_name() {
      auto name = std::string{"dijets_pair_selection_min_mass_diff_order_mass_"};
      name += std::to_string(3) + "first_jets_fixed";
      return name;
    }

};


template <class EventClass> class SetJetPairingOperator : public BaseOperator<EventClass> {

  public:

    typedef std::vector<std::size_t>::iterator It;
    std::string disc_;
    double d_value_;
    std::size_t n_min_disc_;


    SetJetPairingOperator( std::string disc, double d_value, std::size_t n_min_disc = 3  ) :
    	disc_(disc),
    	d_value_(d_value),
    	n_min_disc_(n_min_disc) {}
    virtual ~SetJetPairingOperator() {}

    virtual bool process( EventClass & ev ) {

    // sort in discriminator order 
    auto comparator = [&](alp::Jet a, alp::Jet b){ 
      return a.disc(disc_) > b.disc(disc_); };
    std::sort(ev.jets_.begin(), ev.jets_.end(), comparator );

    // count n jets which pass discriminator
    std::size_t n_pass_disc = std::count_if(ev.jets_.begin(),
                                            ev.jets_.end(),
                                            [&] (const alp::Jet & jet)
    	 {return (jet.disc(disc_) > d_value_);});
    // event discarded if not enough tagged jets
    if ( n_pass_disc < n_min_disc_ ) return false;

    // index vector
    std::vector<std::size_t> jet_is(ev.jets_.size());
    std::iota(jet_is.begin(), jet_is.end(), 0);
    // index vector of the best combination
    std::vector<std::size_t> min_is(jet_is.begin(), jet_is.end());
    double min_v = 100000 ;
    // to save chosen tagged jets
    std::vector<std::size_t> tag_is;

    // iterate over all tagged jet combinations 
    for_each_combination(jet_is.begin(), jet_is.begin()+n_min_disc_,
                         jet_is.begin()+n_pass_disc, [&](It fi, It li) -> bool {
      std::vector<std::size_t> tag_is_t;                   
      tag_is_t.insert(tag_is_t.begin(), jet_is.begin(), jet_is.begin()+n_min_disc_);
    	// iterate over all four jet combinations 
      for_each_combination(jet_is.begin()+n_min_disc_, jet_is.begin()+4,
                           jet_is.end(), [&](It fii, It lii) -> bool {
        // iterate over all dijet pickings 
      	for_each_combination(jet_is.begin(), jet_is.begin()+2, 
                             jet_is.begin()+3, [&](It fiii, It liii) -> bool {
          // this could be done faster with VectorUtil function                   
  				double mass_one = (ev.jets_.at(*jet_is.begin()).p4_+ ev.jets_.at(*(jet_is.begin()+1)).p4_).M();
  				double mass_two = (ev.jets_.at(*(jet_is.begin()+2)).p4_+ ev.jets_.at(*(jet_is.begin()+3)).p4_).M();
          double mass_diff = std::abs(mass_one-mass_two);
          if ( mass_diff < min_v) {
            tag_is = tag_is_t;
            min_v = mass_diff; 
            min_is.clear();
            if (mass_one > mass_two) {
              min_is.insert(min_is.begin(), jet_is.begin(), jet_is.end());
            } else {
              min_is.insert(min_is.begin(), jet_is.begin()+2, jet_is.begin()+4);
              min_is.insert(min_is.begin()+2, jet_is.begin(), jet_is.begin()+2);
              min_is.insert(min_is.begin()+4, jet_is.begin()+4, jet_is.end());
            }
          }
          return false;
       	});
        return false;
      });
      return false;
		});

      // the fist pair of elements of the min_is variable are
      // the indexes of the fist pair and the folowign two
      // are indexes for the second pair 

      std::vector<std::size_t> sel_is;
      sel_is.insert(sel_is.begin(), min_is.begin(), min_is.begin()+4);
      std::sort(tag_is.begin(), tag_is.end());  
      std::sort(sel_is.begin(), sel_is.end());  
      std::vector<std::size_t> dif_is;
      std::set_difference(sel_is.begin(), sel_is.end(),
                          tag_is.begin(), tag_is.end(),
                          std::inserter(dif_is, dif_is.begin()));

      ev.free_is_.clear();
      for (const auto & i : dif_is ) {
        ev.free_is_.emplace_back(std::distance(min_is.begin(),
                                 std::find(min_is.begin(), min_is.end(), i)));
      }
      



      // use same order for jet collection (copy overhead as it is now)
      auto ordered_jets = std::vector<alp::Jet>{}; 
      for (std::size_t i = 0; i < ev.jets_.size(); i++ ) {
        ordered_jets.emplace_back(ev.jets_.at(min_is.at(i)));
      }
      for (std::size_t i = 0; i < ev.jets_.size(); i++ ) {
        ev.jets_.at(i) = ordered_jets.at(i);
      }  
        

      // fill dijet objects
      ev.dijets_.clear();
      ev.dijets_.emplace_back(ev.jets_.at(0).p4_ + ev.jets_.at(1).p4_);
      ev.dijets_.emplace_back(ev.jets_.at(2).p4_ + ev.jets_.at(3).p4_);

      // fill dihiggs objects
      ev.dihiggs_.clear();
      ev.dihiggs_.emplace_back(ev.dijets_.at(0) + ev.dijets_.at(1));

      return true;
    }

    virtual std::string get_name() {
      auto name = std::string{"dijets_pair_selection_min_mass_diff_order_mass_"};
      name += std::to_string(n_min_disc_) + "n_min_disc";
      return name;
    }

};
