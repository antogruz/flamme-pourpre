#!/usr/bin/env python3

from visualtests import *

class TokensDecorators():
    def __init__(self, frame, trackDisplay):
        self.frame = frame
        self.trackDisplay = trackDisplay
        self.decorators = []

    def addRoadDecorator(self, decorator):
        self.decorators.append(decorator)

    def update(self):
        self.trackDisplay.clearAll()
        for decorator in self.decorators:
            decorator.displayOnTrack()
        self.frame.update()

