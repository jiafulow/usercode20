#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import six
from ROOT import gROOT, gSystem, AutoLibraryLoader, TChain
#from DataFormats.FWLite import Events, Handle

# A simple FWLite-based python analyzer
# Based on https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
# Some snippets of codes are stolen from PhysicsTools/Heppy

class L1NtupleAnalyzer(object):

  def __init__(self, inputFiles=None, handles=None, firstEvent=None, maxEvents=None):
    gROOT.SetBatch()  # don't pop up canvases

    if inputFiles:
      if isinstance(inputFiles, str):
        self.inputFiles = [inputFiles]
      else:
        self.inputFiles = inputFiles
    else:
      self.inputFiles = []

    l1tree = 'l1UpgradeTree/L1UpgradeTree'
    #l1tree = 'l1UpgradeEmuTree/L1UpgradeTree'
    tftree = 'l1UpgradeTfMuonTree/L1UpgradeTfMuonTree'
    #tftree = 'l1UpgradeTfMuonEmuTree/L1UpgradeTfMuonTree'

    cc_l1 = TChain(l1tree)
    cc_tf = TChain(tftree)
    for f in self.inputFiles:
      cc_l1.Add(f)
      cc_tf.Add(f)
    self.events = six.moves.zip(cc_l1, cc_tf)

    self.handles = {}
    self.handle_labels = {}
    if handles:
      for k, v in six.iteritems(handles):
        self.handles[k] = Handle(v[0])
        self.handle_labels[k] = v[1]

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
    #self.getHandles(evt)
    return

  def getHandles(self, evt):
    for k, v in six.iteritems(self.handles):
      label = self.handle_labels[k]
      evt.getByLabel(label, v)
    return


# ______________________________________________________________________________
if __name__ == '__main__':
  #print('Loading FW Lite')
  #gSystem.Load('libFWCoreFWLite')
  #gROOT.ProcessLine('FWLiteEnabler::enable();')

  analyzer = L1NtupleAnalyzer(inputFiles='pippo.root')
  analyzer.analyze()
