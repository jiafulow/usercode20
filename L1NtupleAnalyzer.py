#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import six
from ROOT import gROOT, gSystem, AutoLibraryLoader, TChain
#from DataFormats.FWLite import Events, Handle

# See https://github.com/cms-sw/cmssw/blob/master/L1Trigger/L1TNtuples/interface/L1AnalysisL1UpgradeDataFormat.h

class L1Muon(object):
  def __init__(self,
               muonEt,
               muonEta,
               muonPhi,
               muonEtaAtVtx,
               muonPhiAtVtx,
               muonIEt,
               muonIEta,
               muonIPhi,
               muonIEtaAtVtx,
               muonIPhiAtVtx,
               muonIDEta,
               muonIDPhi,
               muonChg,
               muonIso,
               muonQual,
               muonTfMuonIdx,
               muonBx):
    self.muonEt = muonEt
    self.muonEta = muonEta
    self.muonPhi = muonPhi
    self.muonEtaAtVtx = muonEtaAtVtx
    self.muonPhiAtVtx = muonPhiAtVtx
    self.muonIEt = muonIEt
    self.muonIEta = muonIEta
    self.muonIPhi = muonIPhi
    self.muonIEtaAtVtx = muonIEtaAtVtx
    self.muonIPhiAtVtx = muonIPhiAtVtx
    self.muonIDEta = muonIDEta
    self.muonIDPhi = muonIDPhi
    self.muonChg = muonChg
    self.muonIso = muonIso
    self.muonQual = muonQual
    self.muonTfMuonIdx = muonTfMuonIdx
    self.muonBx = muonBx

# See https://github.com/cms-sw/cmssw/blob/master/L1Trigger/L1TNtuples/interface/L1AnalysisL1UpgradeTfMuonDataFormat.h

class TFMuon(object):
  def __init__(self,
               tfMuonHwPt,
               tfMuonHwEta,
               tfMuonHwPhi,
               tfMuonGlobalPhi,
               tfMuonHwSign,
               tfMuonHwSignValid,
               tfMuonHwQual,
               tfMuonLink,
               tfMuonProcessor,
               tfMuonTrackFinderType,
               tfMuonHwHF,
               tfMuonBx,
               tfMuonWh,
               tfMuonTrAdd):
    self.tfMuonHwPt = tfMuonHwPt
    self.tfMuonHwEta = tfMuonHwEta
    self.tfMuonHwPhi = tfMuonHwPhi
    self.tfMuonGlobalPhi = tfMuonGlobalPhi
    self.tfMuonHwSign = tfMuonHwSign
    self.tfMuonHwSignValid = tfMuonHwSignValid
    self.tfMuonHwQual = tfMuonHwQual
    self.tfMuonLink = tfMuonLink
    self.tfMuonProcessor = tfMuonProcessor
    self.tfMuonTrackFinderType = tfMuonTrackFinderType
    self.tfMuonHwHF = tfMuonHwHF
    self.tfMuonBx = tfMuonBx
    self.tfMuonWh = tfMuonWh
    self.tfMuonTrAdd = tfMuonTrAdd

# A simple FWLite-based python analyzer
# Based on https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
# Some snippets of codes are stolen from PhysicsTools/Heppy

class L1NtupleAnalyzer(object):

  def __init__(self, inputFiles=None, handles=None, firstEvent=None, maxEvents=None, use_emu=False):
    gROOT.SetBatch()  # don't pop up canvases

    if inputFiles:
      if isinstance(inputFiles, str):
        self.inputFiles = [inputFiles]
      else:
        self.inputFiles = inputFiles
    else:
      self.inputFiles = []

    if use_emu:
      l1tree = 'l1UpgradeEmuTree/L1UpgradeTree'
      tftree = 'l1UpgradeTfMuonEmuTree/L1UpgradeTfMuonTree'
    else:
      l1tree = 'l1UpgradeTree/L1UpgradeTree'
      tftree = 'l1UpgradeTfMuonTree/L1UpgradeTfMuonTree'

    cc_l1 = TChain(l1tree)
    cc_tf = TChain(tftree)
    for f in self.inputFiles:
      cc_l1.Add(f)
      cc_tf.Add(f)
    self.events = six.moves.zip(cc_l1, cc_tf)

    self.handles = {}
    self.handle_labels = {}
    #if handles:
    #  for k, v in six.iteritems(handles):
    #    self.handles[k] = Handle(v[0])
    #    self.handle_labels[k] = v[1]
    self.handles['muons'] = []
    self.handles['muons_tf'] = []

    if firstEvent:
      self.firstEvent = firstEvent
    else:
      self.firstEvent = 0

    if maxEvents:
      self.maxEvents = maxEvents
    else:
      self.maxEvents = 0x7FFFFFFFFFFFFFFF  # TChain::kBigNumber
    return

  def analyze(self):
    self.beginLoop()
    for evt in self.processLoop():
      pass
    self.endLoop()
    return

  def beginLoop(self):
    return

  def endLoop(self):
    return

  def processLoop(self):
    for ievt, evt in enumerate(self.events):
      if ievt < self.firstEvent:
        continue
      if ievt == self.firstEvent + self.maxEvents:
        break
      #if (ievt % 1000) == 0:
      #  print('Processing event: %i' % ievt)
      self.process(evt)
      yield evt
    return

  def process(self, evt):
    self.getHandles(evt)
    return

  def getHandles(self, evt):
    evt_l1, evt_tf = evt

    zipped = six.moves.zip(evt_l1.muonEt,
                           evt_l1.muonEta,
                           evt_l1.muonPhi,
                           evt_l1.muonEtaAtVtx,
                           evt_l1.muonPhiAtVtx,
                           evt_l1.muonIEt,
                           evt_l1.muonIEta,
                           evt_l1.muonIPhi,
                           evt_l1.muonIEtaAtVtx,
                           evt_l1.muonIPhiAtVtx,
                           evt_l1.muonIDEta,
                           evt_l1.muonIDPhi,
                           evt_l1.muonChg,
                           evt_l1.muonIso,
                           evt_l1.muonQual,
                           evt_l1.muonTfMuonIdx,
                           evt_l1.muonBx)
    del self.handles['muons'][:]
    for z in zipped:
      self.handles['muons'].append(L1Muon(*z))

    zipped = six.moves.zip(evt_tf.tfMuonHwPt,
                           evt_tf.tfMuonHwEta,
                           evt_tf.tfMuonHwPhi,
                           evt_tf.tfMuonGlobalPhi,
                           evt_tf.tfMuonHwSign,
                           evt_tf.tfMuonHwSignValid,
                           evt_tf.tfMuonHwQual,
                           evt_tf.tfMuonLink,
                           evt_tf.tfMuonProcessor,
                           evt_tf.tfMuonTrackFinderType,
                           evt_tf.tfMuonHwHF,
                           evt_tf.tfMuonBx,
                           evt_tf.tfMuonWh,
                           evt_tf.tfMuonTrAdd)
    del self.handles['muons_tf'][:]
    for z in zipped:
      self.handles['muons_tf'].append(TFMuon(*z))
    return


# ______________________________________________________________________________
if __name__ == '__main__':
  #print('Loading FW Lite')
  #gSystem.Load('libFWCoreFWLite')
  #gROOT.ProcessLine('FWLiteEnabler::enable();')

  analyzer = L1NtupleAnalyzer(inputFiles='pippo.root')
  analyzer.analyze()
