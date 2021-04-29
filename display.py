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
        RoadDisplay(self.frame, track, [])

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
        RoadDisplay(self.frame, track, riders)

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
        display = RoadDisplay(self.frame, track, [])
        display.ranking(riders)

    def testZAnimatedRider(self):
        track = Track([(10, "normal")])
        rider = Rider(rouleurShade, "green", (0, 0))
        display = RoadDisplay(self.frame, track,  [rider])
        display.animate(rider, [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)])

    def testZExhaustRiders(self):
        track = Track([(10, "normal")])
        rouleur = Rider(rouleurShade, "green", (0, 0))
        sprinteur = Rider(sprinteurShade, "red", (3, 0))
        display = RoadDisplay(self.frame, track, [rouleur, sprinteur])
        display.exhaust(sprinteur)
        display.exhaust(rouleur)

    def testUpdate(self):
        track = Track([(1, "normal"), (1, "target")])
        rider = Rider(rouleurShade, "green", (0, 0))
        display = RoadDisplay(self.frame, track, [rider])
        rider.pos = (1, 0)
        display.update()


from time import sleep
class RoadDisplay():
    def __init__(self, frame, track, riders, clock = 0.3):
        self.frame = frame
        self.riders = riders
        self.trackWidgets = displayTrack(frame, track)
        displayRiders(self.trackWidgets, riders)
        self.frame.update()
        self.clock = clock

    def ranking(self, ridersArrived):
        displayRanking(self.trackWidgets, ridersArrived)


    def animate(self, rider, path):
        for i in range(len(path) - 1):
            sleep(self.clock)
            self.move(rider, path[i], path[i + 1])

    def move(self, rider, start, end):
        self.empty(start)
        displayRiderAtPosition(self.trackWidgets, rider, end)
        self.frame.update()

    def exhaust(self, rider):
        widget = self.widget(rider)
        originalBg = widget.cget('bg')
        for color in ["yellow", "red", originalBg]:
            self.setBg(widget, color)
            sleep(self.clock)

    def setBg(self, widget, color):
        widget.config(bg = color)
        self.frame.update()


    def widget(self, rider):
        square, lane = rider.position()
        return self.trackWidgets[square][lane]

    def empty(self, position):
        empty(self.trackWidgets[position[0]][position[1]])

    def update(self):
        removeTokens(self.trackWidgets)
        displayRiders(self.trackWidgets, self.riders)
        self.frame.update()
        sleep(self.clock)


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


def displayRiders(boardWidgets, riders):
    for rider in riders:
        displayRider(boardWidgets, rider)


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
