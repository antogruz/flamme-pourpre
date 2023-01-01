#!/usr/bin/env python3

from visualtests import VisualTester
from unittests import runTests
from track import Track
from obstacles import Obstacles
from riderDisplay import rouleurShade, sprinteurShade
from display import RoadDisplay
from eventDisplay import EventDisplay
from logger import Logger

# Je me dis que pour chaque évènement, on pourrait appeler tous les animateurs à la suite dans les différentes frames
class AnimateTester(VisualTester):
    def __before__(self):
        VisualTester.__before__(self)
        frames = self.frames.newLine(2)
        track = Track([(10, "normal")])
        self.logger = Logger()
        self.roadDisplay = RoadDisplay(frames[0], track)
        self.eventDisplay = EventDisplay(frames[1])
        self.animation = Animation(self.roadDisplay, self.eventDisplay)

    def animate(self):
        self.animation.animate(self.logger.getMoves(), self.logger.getGroups(), self.logger.getExhausted())

    def testMove(self):
        rouleur = Rider(rouleurShade, "green")
        sprinteur = Rider(sprinteurShade, "red", (1, 0))
        self.logger.logMove(sprinteur, "f", (1, 0), (3, 0), Obstacles([]))
        self.logger.logMove(rouleur, "3", (0, 0), (3, 1), Obstacles([]))
        self.roadDisplay.displayRiders([rouleur, sprinteur])
        self.animate()

    def testGroup(self):
        a = Rider(rouleurShade, "green", (0, 0))
        b = Rider(rouleurShade, "blue", (2, 0))
        self.roadDisplay.displayRiders([a, b])
        a.pos = (1, 0)
        self.logger.logGroup([a])
        a.pos = (2, 0)
        b.pos = (3, 0)
        self.logger.logGroup([b, a])
        self.animate()

    def testExhaust(self):
        a = Rider(rouleurShade, "black")
        b = Rider(rouleurShade, "blue", (0, 1))
        self.logger.logExhaust(a)
        self.logger.logExhaust(b)
        self.roadDisplay.displayRiders([a, b])
        self.animate()


class Rider:
    def __init__(self, shade, color, position = (0, 0)):
        self.shade = shade
        self.color = color
        self.pos = position
        self.name = "Coureur"

    def position(self):
        return self.pos

from time import sleep
class Animation:
    def __init__(self, roadDisplay, eventDisplay, clock = 0.3):
        self.display = roadDisplay
        self.eventDisplay = eventDisplay
        self.clock = clock

    def animate(self, moves, groups, exhausted):
        for (rider, card, path) in moves:
            self.eventDisplay.displayEvent(rider, card)
            self.animateMove(rider, path)

        sleep(self.clock * 2)
        for group in groups:
            sleep(self.clock * 2)
            self.animateGroup(group)

        for color in ["yellow", "red", "default"]:
            for rider in exhausted:
                self.display.setBackground(rider, color)
            self.display.update()
            sleep(self.clock)


    def animateMove(self, rider, path):
        for i in range(len(path) - 1):
            sleep(self.clock)
            self.display.move(rider, path[i], path[i + 1])
            self.display.update()

    def animateGroup(self, group):
        for (rider, end) in group:
            start = (end[0] - 1, end[1])
            self.display.move(rider, start, end)
        self.display.update()

import tkinter as tk
if __name__ == "__main__":
    runTests(AnimateTester(tk.Tk()))
