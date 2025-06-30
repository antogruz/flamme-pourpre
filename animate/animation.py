#!/usr/bin/env python3

from time import sleep
from race import RaceObserver
from path import findPath

class RoadAnimator(RaceObserver):
    def __init__(self, frame, trackDisplay, track, clock = 0.3):
        self.frame = frame
        self.display = trackDisplay
        self.clock = clock
        self.track = track

    def onRiderMove(self, rider, start, end, obstacles):
        path = findPath(self.track, obstacles, start, end)
        for i in range(len(path) - 1):
            sleep(self.clock)
            self.move(rider, path[i], path[i + 1])
            self.frame.update()

    def onSlipstream(self, group):
        sleep(self.clock * 2)
        for rider in group:
            end = rider.position()
            start = (end[0] - 1, end[1])
            self.move(rider, start, end)
        self.frame.update()

    def onExhaustion(self, exhausted):
        sleep(self.clock * 2)
        for color in ["yellow", "red", "default"]:
            for rider in exhausted:
                square, lane = rider.position()
                self.display.setBackground(square, lane, color)
            self.frame.update()
            sleep(self.clock)
    
    def onTurnEnd(self):
        pass

    def move(self, rider, start, end):
        self.display.clear(start[0], start[1])
        self.display.setContent(end[0], end[1], rider.shade, rider.color)



class EventAnimator(RaceObserver):
    def __init__(self, display):
        self.display = display

    def onRiderMove(self, rider, start, end, obstacles):
        try:
            card = rider.logCardPlayed
        except:
            card = ""
        self.display.displayEvent(rider, card)

    def animateGroup(self, group):
        pass

    def animateExhaust(self, exhausted):
        pass

    def onTurnEnd(self):
        pass

from tkinterSpecific.boxes import BoxFactory
from visualtests import VisualTester
from unittests import runTests
from track import Track
from obstacles import Obstacles
from decorators.riderDisplay import rouleurShade, sprinteurShade, RidersDisplay
from tokensDecorators import TokensDecorators
from trackDisplay import TrackDisplay
from eventDisplay import EventDisplay

class AnimateMovesTester(VisualTester):
    def __before__(self):
        VisualTester.__before__(self)
        frames = self.frames.newLine(2)
        track = Track([(10, "normal")])
        factory = BoxFactory(frames[0])
        self.trackDisplay = TrackDisplay(factory, track)
        self.tokensDecorators = TokensDecorators(frames[0], self.trackDisplay)
        eventDisplay = EventDisplay(frames[1])
        self.animators = [EventAnimator(eventDisplay), RoadAnimator(frames[0], self.trackDisplay, track)]

    def displayRiders(self, riders):
        self.tokensDecorators.addRoadDecorator(RidersDisplay(riders, self.trackDisplay))
        self.tokensDecorators.update()

    def testMove(self):
        rouleur = Rider(rouleurShade, "green")
        sprinteur = Rider(sprinteurShade, "red", (1, 0))
        sprinteur.logCardPlayed = "f"
        rouleur.logCardPlayed = 3
        self.displayRiders([rouleur, sprinteur])
        for animator in self.animators:
            animator.onRiderMove(sprinteur, (1, 0), (3, 0), Obstacles([]))
        for animator in self.animators:
            animator.onRiderMove(rouleur, (0, 0), (3, 1), Obstacles([]))
        sleep(0.5)

class AnimateRoadTester(VisualTester):
    def __before__(self):
        VisualTester.__before__(self)
        frame = self.frames.new()
        track = Track([(10, "normal")])
        factory = BoxFactory(frame)
        self.trackDisplay = TrackDisplay(factory, track)
        self.tokensDecorators = TokensDecorators(frame, self.trackDisplay)
        self.roadAnimator = RoadAnimator(frame, self.trackDisplay, track)

    def displayRiders(self, riders):
        self.tokensDecorators.addRoadDecorator(RidersDisplay(riders, self.trackDisplay))
        self.tokensDecorators.update()

    def testGroup(self):
        a = Rider(rouleurShade, "green", (0, 0))
        b = Rider(rouleurShade, "blue", (2, 0))
        self.displayRiders([a, b])
        a.pos = (1, 0)
        self.roadAnimator.onSlipstream([a])
        a.pos = (2, 0)
        b.pos = (3, 0)
        self.roadAnimator.onSlipstream([b, a])

    def testExhaust(self):
        a = Rider(rouleurShade, "black")
        b = Rider(rouleurShade, "blue", (0, 1))
        self.displayRiders([a, b])
        self.roadAnimator.onExhaustion([a, b])


class Rider:
    def __init__(self, shade, color, position = (0, 0)):
        self.shade = shade
        self.color = color
        self.pos = position
        self.name = "Coureur"
        self.arrived = False

    def position(self):
        return self.pos

from frames import clear
import tkinter as tk
if __name__ == "__main__":
    window = tk.Tk()
    runTests(AnimateRoadTester(window))
    clear(window)
    runTests(AnimateMovesTester(window))
