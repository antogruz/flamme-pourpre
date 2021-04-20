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
            self.frame = self.frames.new(self.window)
        except:
            pass

    def testTrack(self):
        track = Track([(1, "start"), (1, "normal"), (1, "ascent"), (1, "descent"), (1, "end")])
        displayTrack(self.frame, track)

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
        displayBoard(self.frame, track, riders)

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
        widgets = displayTrack(self.frame, track)
        displayRanking(widgets, riders)

    def testAnimatedRider(self):
        track = Track([(10, "normal")])
        rider = Rider(rouleurShade, "green", (0, 0))
        display = RoadDisplay(self.frame, track,  [rider])
        display.animate(rider, [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)])

from time import sleep
class RoadDisplay():
    def __init__(self, frame, track, riders):
        self.frame = frame
        self.trackWidgets = displayTrack(frame, track)
        displayRiders(self.trackWidgets, riders)
        self.frame.update()

    def animate(self, rider, path):
        for i in range(len(path) - 1):
            sleep(0.3)
            self.move(rider, path[i], path[i + 1])

    def move(self, rider, start, end):
        self.empty(start)
        displayRiderAtPosition(self.trackWidgets, rider, end)
        self.frame.update()

    def empty(self, position):
        empty(self.trackWidgets[position[0]][position[1]])


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


def displayRiders(boardWidgets, riders):
    for rider in riders:
        displayRider(boardWidgets, rider)


def displayRanking(boardWidgets, riders):
    for i, r in enumerate(riders):
        displayRiderAtPosition(boardWidgets, r, (len(boardWidgets) - 1 - i, 2))



if __name__ == "__main__":
    tester = VisualTester()
    tester.window = tk.Tk()
    tester.window.title("Visual tests")
    tester.frames = Frames()
    tester.runTests()
    tester.window.mainloop()
