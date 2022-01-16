#!/usr/bin/env python3

from unittests import Tester
import tkinter as tk
from frames import Frames

class VisualTester(Tester):
    def __init__(self, frames):
        self.frames = frames

    def __before__(self):
        self.frame = self.frames.new()

    def testLayout(self):
        layout = RaceLayout(self.frame, 2)
        labels = ["User Frame", "Track Frame", "Deck1", "Deck2"]
        frames = [layout.getUserFrame(), layout.getTrackFrame()] + layout.getDecksFrames()
        for label, frame in zip(labels, frames):
            tk.Label(frame, text = label, highlightthickness = 1, highlightbackground = "black").pack()

class RaceLayout():
    def __init__(self, window, decksCount):
        framesFactory = Frames(window)
        self.user = framesFactory.new()
        self.track = framesFactory.new()
        self.decks = framesFactory.newLine(decksCount)

    def getUserFrame(self):
        return self.user

    def getTrackFrame(self):
        return self.track

    def getDecksFrames(self):
        return self.decks

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Race Layout")
    window.bind("<space>", lambda e: window.destroy())
    VisualTester(Frames(window)).runTests()
    window.mainloop()

