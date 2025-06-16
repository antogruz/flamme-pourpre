#!/usr/bin/env python3

from visualtests import VisualTester
from unittests import runTests
from track import Track
from obstacles import Obstacles
from riderDisplay import rouleurShade, sprinteurShade, RidersDisplay
from display import TokensDecorators
from trackDisplay import TrackDisplayTkinter
from eventDisplay import EventDisplay
from logger import Logger, CardDecorator

class AnimateMovesTester(VisualTester):
    def __before__(self):
        VisualTester.__before__(self)
        frames = self.frames.newLine(2)
        track = Track([(10, "normal")])
        self.logger = Logger()
        self.cardDecorator = CardDecorator()
        self.trackDisplay = TrackDisplayTkinter(frames[0], track)
        self.tokensDecorators = TokensDecorators(frames[0], self.trackDisplay)
        eventDisplay = EventDisplay(frames[1])
        self.animation = Animation([EventAnimator(eventDisplay), RoadAnimator(frames[0], self.trackDisplay)])

    def displayRiders(self, riders):
        self.tokensDecorators.addRoadDecorator(RidersDisplay(riders))
        self.tokensDecorators.update()

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
        self.trackDisplay = TrackDisplayTkinter(frame, track)
        self.tokensDecorators = TokensDecorators(frame, self.trackDisplay)
        self.animation = Animation([RoadAnimator(frame, self.trackDisplay)])

    def displayRiders(self, riders):
        self.tokensDecorators.addRoadDecorator(RidersDisplay(riders))
        self.tokensDecorators.update()

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
    def __init__(self, frame, trackDisplay, clock = 0.3):
        self.frame = frame
        self.display = trackDisplay
        self.clock = clock

    def animateMove(self, rider, card, path):
        for i in range(len(path) - 1):
            sleep(self.clock)
            self.move(rider, path[i], path[i + 1])
            self.frame.update()

    def animateGroup(self, group):
        for (rider, end) in group:
            start = (end[0] - 1, end[1])
            self.move(rider, start, end)
        self.frame.update()

    def animateExhaust(self, exhausted):
        for color in ["yellow", "red", "default"]:
            for rider in exhausted:
                square, lane = rider.position()
                self.display.setBackground(square, lane, color)
            self.frame.update()
            sleep(self.clock)

    def move(self, rider, start, end):
        self.display.clear(start[0], start[1])
        self.display.setContent(end[0], end[1], rider.shade, rider.color)



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
