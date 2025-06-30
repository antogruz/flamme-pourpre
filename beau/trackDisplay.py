#!/usr/bin/env python3

class TrackDisplay:
    def __init__(self, factory, track):
        self.boxes = displayTrack(factory, track)

    def clear(self, square, lane):
        self.boxes[square][lane].clear()

    def setContent(self, square, lane, content, color):
        self.boxes[square][lane].setContent(content, color)

    def setBackground(self, square, lane, color):
        self.boxes[square][lane].setBackground(color)

    def clearAll(self):
        for column in self.boxes:
            for box in column:
                box.clear()


def displayTrack(factory, track):
    boxes = []
    column = 0
    while (track.getRoadType(column) != "out"):
        square = []
        for row in range(track.getLaneCount(column)):
            box = factory.getBox(row, column)
            box.setBorder(colorFromRoadType(track.getRoadType(column)))
            square.append(box)
        
        square.append(factory.getBox(track.getLaneCount(column), column))
        boxes.append(square)
        column += 1
    return boxes

def colorFromRoadType(roadType):
    if roadType == "start":
        return 'goldenrod'
    if roadType == "end":
        return 'goldenrod'
    if roadType == "ascent":
        return 'red'
    if roadType == "descent":
        return 'blue'
    if roadType == "target":
        return 'green'
    if roadType == "refuel":
        return 'cyan2'
    if roadType == "stone":
        return 'burlywood1'
    return 'black'

from visualtests import *
from tkinterSpecific.boxes import buildBoxFactory
from tkinterSpecific.canvasBoxFactory import buildCanvasFactory
import random
from jeu.tracks import randomPresetTrack
from jeu.track import Track

class TrackTester(VisualTester):
    def display(self, track):
        TrackDisplay(self.factoryBuilder(self.frame), track)

    def testLaneOf3(self):
        self.display(Track([(10, "refuel", 3), (2, "ascent", 1), (1, "descent", 2)]))

    def testRandomPresetTrack(self):
        playersCount = random.randint(2, 5)
        self.display(randomPresetTrack(playersCount))

class CanvasTester(TrackTester):
    def __init__(self, window):
        self.factoryBuilder = buildCanvasFactory
        TrackTester.__init__(self, window)

class BoxTester(TrackTester):
    def __init__(self, window):
        self.factoryBuilder = buildBoxFactory
        TrackTester.__init__(self, window)


if __name__ == "__main__":
    runVisualTestsInWindow(CanvasTester)
   # runVisualTestsInWindow(BoxTester)
