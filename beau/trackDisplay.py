#!/usr/bin/env python3

import tkinter as tk

class TrackDisplayTkinter:
    def __init__(self, window, track):
        self.frame = window
        self.boxes = displayTrack(window, track)

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

class BoxDisplay:
    def __init__(self, widget):
        self.widget = widget
        self.defaultBackground = widget.cget('bg')

    def setContent(self, content, color):
        self.widget.config(text = content, fg = color)

    def setBackground(self, color):
        if color == "default":
            color = self.defaultBackground
        self.widget.config(bg = color)

    def clear(self):
        self.widget.config(text = "", fg = "black", bg = self.defaultBackground)


# private methods

def displayTrack(window, track):
    boxesDisplays = []
    column = 0
    bigRow = 0
    while (track.getRoadType(column) != "out"):
        square = []
        for row in range(2):
            lane = getLabel(window, track.getRoadType(column))
            setGrid(lane, column, row)
            square.append(BoxDisplay(lane))
        lane = invisible(window)
        setGrid(lane, column, 2)
        square.append(BoxDisplay(lane))
        boxesDisplays.append(square)
        column += 1
    return boxesDisplays

maxColumn = 30
def setGrid(label, square, lane):
    corridor = int(square / maxColumn)
    label.grid(row = 3 * corridor + 2 - lane, column = square % maxColumn, padx = 1, pady = 1)

def getLabel(window, roadType):
    if roadType == "start":
        return slot(window, 'goldenrod')

    if roadType == "end":
        return slot(window, 'goldenrod')

    if roadType == "ascent":
        return slot(window, 'red')

    if roadType == "descent":
        return slot(window, 'blue')

    if roadType == "target":
        return slot(window, 'green')

    return slot(window, 'black')

def slot(window, border):
    return tk.Label(window, text = "", highlightthickness = 1, highlightbackground = border, width = 3)

def invisible(window):
    return tk.Label(window, width = 3)


from visualtests import *
from tracks import *

class TrackTester(VisualTester):
    def display(self, track):
        displayTrack(self.frames.new(), track)

    def testCorsoPaseo(self):
        self.display(corsoPaseo())

    def testColDuBallon(self):
        self.display(colDuBallon())

    def testHauteMontagne(self):
        self.display(hauteMontagne())

    def testClassicissima(self):
        self.display(classicissima())

    def testRonde(self):
        self.display(rondeVanWevelgem())

    def testFirenzeMilano(self):
        self.display(firenzeMilano())


if __name__ == "__main__":
    runVisualTestsInWindow(TrackTester)
