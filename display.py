#!/usr/bin/env python3

from unittests import *
from trackDisplay import displayTrack, empty
from track import Track
import tkinter as tk
from frames import Frames
from riderDisplay import *

class VisualTester(Tester):
    def __init__(self):
        try:
            self.frame = self.frames.new()
        except:
            pass

    def testTrack(self):
        track = Track([(1, "start"), (1, "normal"), (1, "ascent"), (1, "descent"), (1, "end")])
        RoadDisplay(self.frame, track)

    def testRiders(self):
        track = Track([(10, "normal")])
        riders = [
                Rider(rouleurShade, "green", (0, 0)),
                Rider(rouleurShade, "black", (0, 1)),
                Rider(rouleurShade, "red", (2, 0)),
                Rider(rouleurShade, "blue", (9, 1)),
                Rider(sprinteurShade, "green", (3, 1)),
                Rider(sprinteurShade, "black", (4, 0)),
                Rider(sprinteurShade, "red", (6, 2)),
                Rider(sprinteurShade, "blue", (8, 0))
            ]
        RoadDisplay(self.frame, track).displayRiders(riders)


    def testRanking(self):
        track = Track([(10, "normal")])
        riders = [
                Rider(rouleurShade, "green", (0, 0)),
                Rider(rouleurShade, "black", (0, 1)),
                Rider(rouleurShade, "red", (2, 0)),
                Rider(rouleurShade, "blue", (9, 1)),
                Rider(sprinteurShade, "green", (3, 1)),
                Rider(sprinteurShade, "black", (4, 0)),
                Rider(sprinteurShade, "red", (6, 2)),
                Rider(sprinteurShade, "blue", (8, 0))
            ]
        display = RoadDisplay(self.frame, track)
        display.ranking(riders)


from time import sleep
class RoadDisplay():
    def __init__(self, frame, track):
        self.frame = frame
        self.trackWidgets = displayTrack(frame, track)
        self.frame.update()
        self.defaultBackground = self.trackWidgets[0][0].cget('bg')

    def ranking(self, ridersArrived):
        displayRanking(self.trackWidgets, ridersArrived)

    def displayRiders(self, riders):
        removeTokens(self.trackWidgets)
        for rider in riders:
            displayRider(self.trackWidgets, rider)
        self.update()

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

    def update(self):
        self.frame.update()


def removeTokens(trackWidgets):
    for square in trackWidgets:
        for lane in square:
            empty(lane)

class Rider:
    def __init__(self, shade, color, pos):
        self.shade = shade
        self.color = color
        self.pos = pos

    def position(self):
        return self.pos


def displayBoard(window, road, riders):
    trackWidgets = displayTrack(window, road)
    displayRiders(trackWidgets, riders)
    return trackWidgets




def displayRanking(boardWidgets, riders):
    for i, r in enumerate(riders):
        displayRiderAtPosition(boardWidgets, r, (len(boardWidgets) - 1 - i, 2))



if __name__ == "__main__":
    tester = VisualTester()
    window = tk.Tk()
    window.title("Visual tests")
    tester.frames = Frames(window)
    tester.runTests()
    window.mainloop()
