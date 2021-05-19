#!/usr/bin/env python3

from unittests import Tester
import tkinter as tk
from frames import Frames
from cards import Cards

class VisualTester(Tester):
    def __init__(self, frames):
        self.frames = frames

    def __before__(self):
        self.frame = self.frames.new()

    def testEmpty(self):
        displayCards(self.frame, Rider(), 0, [], [])

    def testAfterFirstRound(self):
        displayCards(self.frame, Rider(), 7, [2, 4, 5], [9, 3, 2, 3, 5, 3, 5])

from display import rouleurShade
class Rider:
    def __init__(self):
        self.shade = rouleurShade
        self.name = "Rouleur"
        self.color = "green"

def displayCards(frame, rider, deckSize, discard, played):
    subFrames = Frames(frame)
    displayRider(subFrames.new(), rider)
    framesLine = subFrames.newLine(3)
    displayDeck(framesLine[0], deckSize)
    displayDiscard(framesLine[1], discard, rider.color)
    displayPlayed(framesLine[2], sorted(played))


def displayRider(window, rider):
    tk.Label(window, text = rider.name + " " + rider.shade, fg = rider.color).pack()

def displayDeck(window, cardsCount):
    bigCard(window, cardsCount, "black", "raised").pack()

def displayDiscard(window, cards, color):
    if cards:
        bigCard(window, str(cards[-1]), color, "raised").pack()


def displayPlayed(window, cards):
    last = -1
    row = 0
    col = -1
    for c in cards:
        if c == last:
            row += 1
        else:
            row = 0
            col += 1
        last = c
        smallCard(window, str(c)).grid(row = row, column = col, padx = 1, pady = 1)

def bigCard(window, text, color = "black", relief = "flat"):
    label = cardLabel(window, text, color, relief)
    resize(label, 3)
    return label

def smallCard(window, text, color = "black", relief = "flat"):
    label = cardLabel(window, text, color, relief)
    resize(label, 1)
    return label

def cardLabel(window, text, color, relief):
    return tk.Label(window, text = text, fg = color,  highlightthickness = 1, highlightbackground = "black", relief = relief)

def resize(label, n):
    label.config(width = n, height = n)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Visual tests")
    window.bind("<space>", lambda e: window.destroy())
    VisualTester(Frames(window)).runTests()
    window.mainloop()


