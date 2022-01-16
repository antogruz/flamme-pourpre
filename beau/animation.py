#!/usr/bin/env python3

from frames import Frames
from unittests import Tester
from track import Track
from obstacles import Obstacles
from riderDisplay import rouleurShade
from display import RoadDisplay
from logger import Logger

class VisualTester(Tester):
    def __init__(self, frames):
        self.frames = frames

    def __before__(self):
        self.frame = self.frames.new()
        self.track = Track([(10, "normal")])
        self.logger = Logger()
        self.display = RoadDisplay(self.frame, self.track)
        self.animation = Animation(self.display)


    def animate(self):
        self.animation.animate(self.logger.getMoves(), self.logger.getGroups(), self.logger.getExhausted())

    def testMove(self):
        rider = Rider(rouleurShade, "green")
        self.logger.logMove(rider, (0, 0), (3, 1), Obstacles([]))
        self.display.displayRiders([rider])
        self.animate()

    def testGroup(self):
        a = Rider(rouleurShade, "green", (0, 0))
        b = Rider(rouleurShade, "blue", (2, 0))
        self.display.displayRiders([a, b])
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
        self.display.displayRiders([a, b])
        self.animate()


class Rider:
    def __init__(self, shade, color, position = (0, 0)):
        self.shade = shade
        self.color = color
        self.pos = position

    def position(self):
        return self.pos

from time import sleep
class Animation:
    def __init__(self, display, clock = 0.3):
        self.display = display
        self.clock = clock

    def animate(self, moves, groups, exhausted):
        for (rider, path) in moves:
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
    window = tk.Tk()
    VisualTester(Frames(window)).runTests()
