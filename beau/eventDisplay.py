#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
from decorators.riderDisplay import rouleurShade, opportunisticShade
import tkinter as tk
from frames import Frames
from cardsDisplay import bigCard, smallCard, thereIsColorIn, extractColor
from beautifulCard import createBeautifulCard, BeautifulCard

class EventTester(VisualTester):
    def testEvent(self):
        blue, red = Rider("Rouleur", rouleurShade, "blue"), Rider("Opportuniste", opportunisticShade, "red")
        display = EventDisplay(self.frame)
        display.displayEvent(blue, "f")
        display.displayEvent(red, "9magenta")

class EventDisplay:
    def __init__(self, window):
        self.window = window
        subFrames = Frames(window)
        names = subFrames.newLine(2)
        cards = subFrames.newLine(2)
        for frame in names + cards:
            frame.config(width = 140, height = 60)
        self.currentRider = tk.Label(names[0])
        self.previousRider = tk.Label(names[1])
        self.currentCard = bigCard(cards[0], BeautifulCard(""))
        self.previousCard = smallCard(cards[1], BeautifulCard(""))
        for label in [self.currentRider, self.previousRider, self.currentCard, self.previousCard]:
            label.place(relx=.5, rely=.5, anchor="c")

        self.current = None

    def displayEvent(self, rider, card):
        if self.current:
            self.updatePrevious(self.current[0], self.current[1])
        self.updateCurrent(rider, card)
        self.current = (rider, card)

    def updatePrevious(self, rider, card):
        self.previousRider.config(text = rider.shade, fg = rider.color)
        updateCardLabel(self.previousCard, card, rider.color)

    def updateCurrent(self, rider, card):
        self.currentRider.config(text = rider.name + " " + rider.shade, fg = rider.color)
        updateCardLabel(self.currentCard, card, rider.color)


def updateCardLabel(label, card, defaultColor):
    niceCard = createBeautifulCard(card, defaultColor)
    label.config(text = niceCard.text, fg = niceCard.color, bg = niceCard.background)

class Rider:
    def __init__(self, name, shade, color):
        self.name = name
        self.shade = shade
        self.color = color

if __name__ == "__main__":
    runVisualTestsInWindow(EventTester)
