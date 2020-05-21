#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from FWLiteAnalyzer import FWLiteAnalyzer

inputFiles = ['step2.root']

handles = {
  #'muons': ('BXVector<l1t::Muon>', 'simGmtStage2Digis')
  'muons_tf': ('BXVector<l1t::RegionalMuonCand>', 'simEmtfDigis:EMTF')
}

# ______________________________________________________________________________
if __name__ == '__main__':
  analyzer = FWLiteAnalyzer(inputFiles, handles)

  n = 0
  t = 0.

  analyzer.beginLoop()

  for ievt, evt in enumerate(analyzer.processLoop()):
    #muons = analyzer.handles['muons'].product()
    muons = analyzer.handles['muons_tf'].product()

    for bx in range(muons.getFirstBX(), muons.getLastBX()+1):
      muons_in_bx = [muons.at(bx, i) for i in range(muons.size(bx))]
      for muon in muons_in_bx:
        #print(muon.pt(), muon.eta(), muon.phi(), muon.charge())
        print(muon.hwPt(), muon.hwEta(), muon.hwPhi(), muon.hwSign())
        n += 1
        t += muon.hwPt()

  analyzer.endLoop()

  t /= n
  print('t:', t)
