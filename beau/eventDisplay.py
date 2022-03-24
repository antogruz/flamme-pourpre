#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
from riderDisplay import rouleurShade, sprinteurShade
import tkinter as tk
from frames import Frames
from cardsDisplay import bigCard, smallCard

class EventTester(VisualTester):
    def testEvent(self):
        blue, red = Rider("Rouleur", rouleurShade, "blue"), Rider("Sprinteur", sprinteurShade, "red")
        display = EventDisplay(self.frame)
        display.displayEvent(blue, "f")
        display.displayEvent(red, "9")

class EventDisplay:
    def __init__(self, window):
        self.window = window
        subFrames = Frames(window)
        names = subFrames.newLine(2)
        cards = subFrames.newLine(2)
        for frame in names + cards:
            frame.config(width = 80, height = 50)
        self.currentRider = tk.Label(names[0])
        self.previousRider = tk.Label(names[1])
        self.currentCard = bigCard(cards[0], "")
        self.previousCard = smallCard(cards[1], "")
        for label in [self.currentRider, self.previousRider, self.currentCard, self.previousCard]:
            label.place(relx=.5, rely=.5, anchor="c")
            #label.pack(side="left")

        self.current = None

    def displayEvent(self, rider, card):
        if self.current:
            self.updatePrevious(self.current[0], self.current[1])
        self.updateCurrent(rider, card)
        self.current = (rider, card)

    def updatePrevious(self, rider, card):
        self.previousRider.config(text = rider.shade, fg = rider.color)
        self.previousCard.config(text = card, fg = rider.color)

    def updateCurrent(self, rider, card):
        self.currentRider.config(text = rider.name + " " + rider.shade, fg = rider.color)
        self.currentCard.config(text = card, fg = rider.color)

class Rider:
    def __init__(self, name, shade, color):
        self.name = name
        self.shade = shade
        self.color = color

if __name__ == "__main__":
    runVisualTestsInWindow(EventTester)
