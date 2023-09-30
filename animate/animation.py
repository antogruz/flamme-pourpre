#!/usr/bin/env python3

from visualtests import VisualTester
from unittests import runTests
from track import Track
from obstacles import Obstacles
from riderDisplay import rouleurShade, sprinteurShade
from display import RoadDisplay
from eventDisplay import EventDisplay
from logger import Logger, CardDecorator
from riderDisplay import RidersDisplay

class AnimateMovesTester(VisualTester):
    def __before__(self):
        VisualTester.__before__(self)
        frames = self.frames.newLine(2)
        track = Track([(10, "normal")])
        self.logger = Logger()
        self.cardDecorator = CardDecorator()
        self.roadDisplay = RoadDisplay(frames[0], track)
        eventDisplay = EventDisplay(frames[1])
        self.animation = Animation([EventAnimator(eventDisplay), RoadAnimator(self.roadDisplay)])

    def displayRiders(self, riders):
        self.roadDisplay.addRoadDecorator(RidersDisplay(riders))
        self.roadDisplay.update()

    def animate(self):
        self.animation.animate(self.logger.getMoves(), [], [])

    def testMove(self):
        rouleur = Rider(rouleurShade, "green")
        sprinteur = Rider(sprinteurShade, "red", (1, 0))
        self.cardDecorator.cardPlayed(sprinteur, "f")
        self.cardDecorator.cardPlayed(rouleur, 3)
        self.logger.logMove(sprinteur, (1, 0), (3, 0), Obstacles([]))
        self.logger.logMove(rouleur, (0, 0), (3, 1), Obstacles([]))
        self.displayRiders([rouleur, sprinteur])
        self.animate()

class AnimateRoadTester(VisualTester):
    def __before__(self):
        VisualTester.__before__(self)
        frame = self.frames.new()
        track = Track([(10, "normal")])
        self.logger = Logger()
        self.roadDisplay = RoadDisplay(frame, track)
        self.animation = Animation([RoadAnimator(self.roadDisplay)])

    def displayRiders(self, riders):
        self.roadDisplay.addRoadDecorator(RidersDisplay(riders))
        self.roadDisplay.update()

    def animate(self):
        self.animation.animate(self.logger.getMoves(), self.logger.getGroups(), self.logger.getExhausted())

    def testGroup(self):
        a = Rider(rouleurShade, "green", (0, 0))
        b = Rider(rouleurShade, "blue", (2, 0))
        self.displayRiders([a, b])
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
        self.displayRiders([a, b])
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
    def __init__(self, animators, clock = 0.3):
        self.animators = animators
        self.clock = clock

    def animate(self, moves, groups, exhausted):
        for (rider, card, path) in moves:
            for a in self.animators:
                a.animateMove(rider, card, path)

        sleep(self.clock * 2)
        for group in groups:
            sleep(self.clock * 2)
            for a in self.animators:
                a.animateGroup(group)

        sleep(self.clock * 2)
        for a in self.animators:
            a.animateExhaust(exhausted)


class RoadAnimator:
    def __init__(self, display, clock = 0.3):
        self.display = display
        self.clock = clock

    def animateMove(self, rider, card, path):
        for i in range(len(path) - 1):
            sleep(self.clock)
            self.display.move(rider, path[i], path[i + 1])
            self.display.frame.update()

    def animateGroup(self, group):
        for (rider, end) in group:
            start = (end[0] - 1, end[1])
            self.display.move(rider, start, end)
        self.display.frame.update()

    def animateExhaust(self, exhausted):
        for color in ["yellow", "red", "default"]:
            for rider in exhausted:
                self.display.setBackground(rider, color)
            self.display.frame.update()
            sleep(self.clock)

class EventAnimator:
    def __init__(self, display):
        self.display = display

    def animateMove(self, rider, card, path):
        self.display.displayEvent(rider, card)

    def animateGroup(self, group):
        pass

    def animateExhaust(self, exhausted):
        pass

from frames import clear
import tkinter as tk
if __name__ == "__main__":
    window = tk.Tk()
    runTests(AnimateRoadTester(window))
    clear(window)
    runTests(AnimateMovesTester(window))
