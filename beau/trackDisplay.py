#!/usr/bin/env python3

import tkinter as tk
from tkinterSpecific.boxes import BoxFactory

class TrackDisplayTkinter:
    def __init__(self, window, track):
        factory = BoxFactory(window)
        self.frame = window
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
        return 'brown'
    return 'black'

from visualtests import *
from tracks import *

class TrackTester(VisualTester):
    def display(self, track):
        factory = BoxFactory(self.frame)
        displayTrack(factory, track)

    def testColDuBallon(self):
        self.display(colDuBallon())

    def testStage10_2(self):
        self.display(stage10(2))

    def testStage10_5(self):
        self.display(stage10(5))

    def testLaneOf3(self):
        self.display(Track([(10, "refuel", 3), (2, "ascent", 1), (1, "descent", 2)]))


if __name__ == "__main__":
    runVisualTestsInWindow(TrackTester)
