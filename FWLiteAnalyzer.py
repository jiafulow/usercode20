#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import six
from ROOT import gROOT, gSystem, AutoLibraryLoader
from DataFormats.FWLite import Events, Handle

# A simple FWLite-based python analyzer
# Based on https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
# Some snippets of codes are stolen from PhysicsTools/Heppy

class FWLiteAnalyzer(object):

  def __init__(self, inputFiles=None, handles=None, firstEvent=None, maxEvents=None):
    gROOT.SetBatch()  # don't pop up canvases

    if inputFiles:
      if isinstance(inputFiles, str):
        self.inputFiles = [inputFiles]
      else:
        self.inputFiles = inputFiles
    else:
      self.inputFiles = []

    self.events = Events(self.inputFiles)

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
    self.getHandles(evt)
    return

  def getHandles(self, evt):
    for k, v in six.iteritems(self.handles):
      label = self.handle_labels[k]
      evt.getByLabel(label, v)
    return


# ______________________________________________________________________________
if __name__ == '__main__':
  #print('Loading FW Lite')
  gSystem.Load('libFWCoreFWLite')
  gROOT.ProcessLine('FWLiteEnabler::enable();')

  analyzer = FWLiteAnalyzer(inputFiles='pippo.root')
  analyzer.analyze()
