#!/usr/bin/env python3

from visualtests import *

class RoadDisplay():
    def __init__(self, frame, trackDisplay):
        self.frame = frame
        self.trackDisplay = trackDisplay
        self.decorators = []

    def addRoadDecorator(self, decorator):
        self.decorators.append(decorator)

    def update(self):
        self.trackDisplay.clearAll()
        for decorator in self.decorators:
            for squareDisplay in decorator.displayOnTrack():
                self.decorate(squareDisplay)
        self.frame.update()

# Private methods

    def decorate(self, squareDisplay):
        self.trackDisplay.setContent(squareDisplay.square, squareDisplay.lane, squareDisplay.text, squareDisplay.color)



class SquareDisplay:
    def __init__(self, square, lane, color, text):
        self.square = square
        self.lane = lane
        self.color = color
        self.text = text


