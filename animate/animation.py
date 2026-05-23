#!/usr/bin/env python3

from time import sleep
from race import RaceObserver
from path import findPath

class RoadAnimator(RaceObserver):
    def __init__(self, frame, trackDisplay, track, appearances, clock = 0.3):
        self.frame = frame
        self.display = trackDisplay
        self.clock = clock
        self.track = track
        self.appearances = appearances

    def onRiderMove(self, rider, start, end, obstacles, card):
        path = findPath(self.track, obstacles, start, end)
        for i in range(len(path) - 1):
            sleep(self.clock)
            self.move(rider, path[i], path[i + 1])
            self.frame.update()

    def onSlipstream(self, moves):
        sleep(self.clock * 2)
        for rider, start, end in moves:
            if start == end:
                continue
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
        appearance = self.appearances.of(rider)
        self.display.clear(start[0], start[1])
        self.display.setContent(end[0], end[1], appearance.shade, appearance.color)



class EventAnimator(RaceObserver):
    def __init__(self, display):
        self.display = display

    def onRiderMove(self, rider, start, end, obstacles, card):
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
from jeu.track import Track
from obstacles import Obstacles
from decorators.riderDisplay import rouleurShade, sprinteurShade, RidersDisplay
from tokensDecorators import TokensDecorators
from trackDisplay import TrackDisplay
from eventDisplay import EventDisplay
from appearances import Appearances

class AnimateMovesTester(VisualTester):
    def __before__(self):
        VisualTester.__before__(self)
        frames = self.frames.newLine(2)
        track = Track([(10, "normal")])
        factory = BoxFactory(frames[0])
        self.trackDisplay = TrackDisplay(factory, track)
        self.tokensDecorators = TokensDecorators(frames[0], self.trackDisplay)
        self.appearances = Appearances()
        eventDisplay = EventDisplay(frames[1], self.appearances)
        self.animators = [EventAnimator(eventDisplay), RoadAnimator(frames[0], self.trackDisplay, track, self.appearances)]

    def displayRiders(self, riders):
        self.tokensDecorators.addRoadDecorator(RidersDisplay(lambda: riders, self.trackDisplay, self.appearances))
        self.tokensDecorators.update()

    def makeRider(self, shade, color, pos=(0, 0)):
        rider = Rider(pos)
        self.appearances.register(rider, "Coureur", shade, color)
        return rider

    def testMove(self):
        rouleur = self.makeRider(rouleurShade, "green")
        sprinteur = self.makeRider(sprinteurShade, "red", (1, 0))
        self.displayRiders([rouleur, sprinteur])
        for animator in self.animators:
            animator.onRiderMove(sprinteur, (1, 0), (3, 0), Obstacles([]), "f")
        for animator in self.animators:
            animator.onRiderMove(rouleur, (0, 0), (3, 1), Obstacles([]), 3)
        sleep(0.5)

class AnimateRoadTester(VisualTester):
    def __before__(self):
        VisualTester.__before__(self)
        frame = self.frames.new()
        track = Track([(10, "normal")])
        factory = BoxFactory(frame)
        self.trackDisplay = TrackDisplay(factory, track)
        self.tokensDecorators = TokensDecorators(frame, self.trackDisplay)
        self.appearances = Appearances()
        self.roadAnimator = RoadAnimator(frame, self.trackDisplay, track, self.appearances)

    def displayRiders(self, riders):
        self.tokensDecorators.addRoadDecorator(RidersDisplay(lambda: riders, self.trackDisplay, self.appearances))
        self.tokensDecorators.update()

    def makeRider(self, shade, color, pos=(0, 0)):
        rider = Rider(pos)
        self.appearances.register(rider, "Coureur", shade, color)
        return rider

    def testGroup(self):
        a = self.makeRider(rouleurShade, "green", (0, 0))
        b = self.makeRider(rouleurShade, "blue", (2, 0))
        self.displayRiders([a, b])
        a.pos = (1, 0)
        self.roadAnimator.onSlipstream([(a, (0, 0), (1, 0))])
        a.pos = (2, 0)
        b.pos = (3, 0)
        self.roadAnimator.onSlipstream([(b, (2, 0), (3, 0)), (a, (1, 0), (2, 0))])

    def testExhaust(self):
        a = self.makeRider(rouleurShade, "black")
        b = self.makeRider(rouleurShade, "blue", (0, 1))
        self.displayRiders([a, b])
        self.roadAnimator.onExhaustion([a, b])


class Rider:
    def __init__(self, position):
        self.pos = position

    def position(self):
        return self.pos

from frames import clear
import tkinter as tk
if __name__ == "__main__":
    window = tk.Tk()
    runTests(AnimateRoadTester(window))
    clear(window)
    runTests(AnimateMovesTester(window))
