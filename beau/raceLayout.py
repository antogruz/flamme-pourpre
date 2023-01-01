#!/usr/bin/env python3

from visualtests import *
import tkinter as tk
from frames import Frames

class RaceTester(VisualTester):
    def testLayout(self):
        layout = RaceLayout(self.frame, 2)
        labels = ["User Frame", "Track Frame", "Event Frame", "Deck1", "Deck2"]
        frames = [layout.getUserFrame(), layout.getTrackFrame(), layout.getEventFrame()] + layout.getDecksFrames()
        for label, frame in zip(labels, frames):
            tk.Label(frame, text = label, highlightthickness = 1, highlightbackground = "black").pack()

class RaceLayout():
    def __init__(self, window, decksCount):
        framesFactory = Frames(window)
        self.user = framesFactory.new()
        self.track, self.event = framesFactory.newLine(2)
        self.decks = framesFactory.newLine(decksCount)

    def getUserFrame(self):
        return self.user

    def getTrackFrame(self):
        return self.track

    def getDecksFrames(self):
        return self.decks

    def getEventFrame(self):
        return self.event

if __name__ == "__main__":
    runVisualTestsInWindow(RaceTester)

