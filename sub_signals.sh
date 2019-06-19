python scripts/BaselineSelector.py -s signals -i v2_20170606 -o def_cmva_btagfix &
sleep 1200
python scripts/BaselineSelector.py -s signals -i v2_20170606 -o def_cmva_btagfix --jetCorr 0 &
sleep 1200
python scripts/BaselineSelector.py -s signals -i v2_20170606 -o def_cmva_btagfix --jetCorr 1 &
sleep 1200
python scripts/BaselineSelector.py -s signals -i v2_20170606 -o def_cmva_btagfix --jetCorr 2 &
sleep 1200
python scripts/BaselineSelector.py -s signals -i v2_20170606 -o def_cmva_btagfix --jetCorr 3 &
sleep 2400
hadd /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix/HHTo4B_pangea.root /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JESdown/*.root
hadd /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JESup/HHTo4B_pangea.root /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JESup/*.root
hadd /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JESdown/HHTo4B_pangea.root /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JESdown/*.root
hadd /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JERup/HHTo4B_pangea.root /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JERup/*.root
hadd /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JERdown/HHTo4B_pangea.root /lustre/cmswork/hh/alp_moriond_base/def_cmva_btagfix_JERdown/*.root
