#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from L1NtupleAnalyzer import L1NtupleAnalyzer

inputFiles = ['../store/L1Ntuple_DY_EMU_RAW_100k_cmssw_11_0_0_patch1_noCSC.root']

handles = {
  #'muons': ('BXVector<l1t::Muon>', 'simGmtStage2Digis')
  #'muons_emtf': ('BXVector<l1t::RegionalMuonCand>', 'simEmtfDigis:EMTF')
}

# ______________________________________________________________________________
if __name__ == '__main__':
  analyzer = L1NtupleAnalyzer(inputFiles, handles, firstEvent=None, maxEvents=10)

  n = 0

  analyzer.beginLoop()

  for ievt, evt in enumerate(analyzer.processLoop()):
    evt_l1, evt_tf = evt
    #print(type(evt_l1), type(evt_l1.nMuons), type(evt_l1.muonEt))
    #print(type(evt_tf), type(evt_tf.nTfMuons), type(evt_tf.tfMuonHwPt))
    print(len(evt_l1.muonEt), len(evt_l1.muonEta))
    print(len(evt_tf.tfMuonHwPt), len(evt_tf.tfMuonHwEta))
    n += 1

  analyzer.endLoop()

  print('n:', n)
