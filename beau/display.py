#!/usr/bin/env python3

from visualtests import *
from trackDisplay import displayTrack, empty
from track import Track
import tkinter as tk

def displayRiderAtPosition(boardWidgets, rider, position):
    square, lane = position[0], position[1]
    widget = boardWidgets[square][lane]
    widget.config(text = rider.shade, fg = rider.color)


from time import sleep
class RoadDisplay():
    def __init__(self, frame, track):
        self.frame = frame
        self.trackWidgets = displayTrack(frame, track)
        self.frame.update()
        self.defaultBackground = self.trackWidgets[0][0].cget('bg')
        self.decorators = []

    def addRoadDecorator(self, decorator):
        self.decorators.append(decorator)

    def move(self, rider, start, end):
        self.empty(start)
        displayRiderAtPosition(self.trackWidgets, rider, end)

    def setBackground(self, rider, color):
        if color== "default":
            color = self.defaultBackground
        self.widget(rider).config(bg = color)

    def widget(self, rider):
        square, lane = rider.position()
        return self.trackWidgets[square][lane]

    def empty(self, position):
        empty(self.trackWidgets[position[0]][position[1]])

    def endOfTurnUpdate(self):
        removeTokens(self.trackWidgets)
        for decorator in self.decorators:
            for squareDisplay in decorator.displayOnTrack():
                self.decorate(squareDisplay)
        self.frame.update()

    def update(self):
        self.frame.update()

    def decorate(self, squareDisplay):
        widget = self.trackWidgets[squareDisplay.square][squareDisplay.lane]
        widget.config(fg = squareDisplay.color, text = squareDisplay.text)



def removeTokens(trackWidgets):
    for square in trackWidgets:
        for lane in square:
            empty(lane)


class SquareDisplay:
    def __init__(self, square, lane, color, text):
        self.square = square
        self.lane = lane
        self.color = color
        self.text = text


