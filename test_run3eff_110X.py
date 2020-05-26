#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from L1NtupleAnalyzer import L1NtupleAnalyzer

inputFiles = ['../store/L1Ntuple_DY_EMU_RAW_100k_cmssw_11_0_0_patch1_noCSC.root']
#inputFiles = ['../store/L1Ntuple_DY_EMU_RAW_100k_cmssw_11_0_0_patch1.root']

handles = {}

use_tf = False

use_emu = False

# ______________________________________________________________________________
if __name__ == '__main__':
  analyzer = L1NtupleAnalyzer(inputFiles, handles, firstEvent=None, maxEvents=40, use_emu=use_emu)

  n = 0
  t = 0.

  analyzer.beginLoop()

  for ievt, evt in enumerate(analyzer.processLoop()):
    #print('Processing event: %i' % ievt)
    if use_tf:
      muons = analyzer.handles['muons_tf']
    else:
      muons = analyzer.handles['muons']

    for muon in muons:
      if use_tf:
        print(muon.tfMuonHwPt, muon.tfMuonHwEta, muon.tfMuonHwPhi, muon.tfMuonHwSign, muon.tfMuonBx)
      else:
        print(muon.muonEt, muon.muonEta, muon.muonPhi, muon.muonChg, muon.muonBx)

      n += 1
      if use_tf:
        t += muon.tfMuonHwPt
      else:
        t += muon.muonEt

  analyzer.endLoop()

  t /= n
  print('n:', n, 't:', t)
