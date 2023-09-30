#!/usr/bin/env python3

from visualtests import *
import tkinter as tk
from frames import Frames

class RaceTester(VisualTester):
    def testLayout(self):
        layout = RaceLayout(self.frame)
        labels = ["Track Frame", "Event Frame", "Deck1", "Deck2"]
        frames = [layout.getTrackFrame(), layout.getEventFrame()]
        for label, frame in zip(labels, frames):
            tk.Label(frame, text = label, highlightthickness = 1, highlightbackground = "black").pack()

class RaceLayout():
    def __init__(self, window):
        framesFactory = Frames(window)
        self.track, self.event = framesFactory.newLine(2)

    def getTrackFrame(self):
        return self.track

    def getEventFrame(self):
        return self.event

if __name__ == "__main__":
    runVisualTestsInWindow(RaceTester)

