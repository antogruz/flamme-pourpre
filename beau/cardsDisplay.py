#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
import tkinter as tk
from frames import Frames, clear
from cards import Cards

class CardsTester(VisualTester):
    def testEmpty(self):
        display = CardsDisplay(self.frame, Rider())
        display.displayCards(0, [], [])

    def testAfterFirstRound(self):
        display = CardsDisplay(self.frame, Rider())
        display.displayCards(7, [2, 4, 5], [9, 3, 2, 3, 5, 3, 5])

from display import rouleurShade
class Rider:
    def __init__(self):
        self.shade = rouleurShade
        self.name = "Rouleur"
        self.color = "green"

class CardsDisplay:
    def __init__(self, frame, rider):
        self.frame = frame
        subFrames = Frames(frame)
        self.riderFrame = subFrames.new()
        self.deckFrame, self.discardFrame, self.playedFrame = subFrames.newLine(3)
        self.fullDiscardFrame = subFrames.new()
        self.rider = rider
        self.color = rider.color
        self.prepareWidgets()

    def prepareWidgets(self):
        displayRider(self.riderFrame, self.rider)
        self.deck = deck(self.deckFrame, "")
        self.deck.pack()
        self.discard = deck(self.discardFrame, "")
        self.allCardsDiscarded = []
        self.discard.bind("<Button-1>", lambda e:toggleDiscard(self.allCardsDiscarded))

    def displayCards(self, deckSize, discard, played):
        self.deck.config(text = deckSize)
        self.discard.config(text = len(discard))
        if discard:
            self.discard.pack()
        else:
            hide(self.discard)
        self.allCardsDiscarded = [smallCard(self.fullDiscardFrame, card, self.color) for card in discard]
        displayPlayed(self.playedFrame, sorted(played), self.color)



def displayRider(window, rider):
    tk.Label(window, text = rider.name + " " + rider.shade, fg = rider.color).pack()

def toggleDiscard(cardLabels):
    for label in cardLabels:
        if label.winfo_ismapped():
            hide(label)
        else:
            label.pack(side="left")

def hide(label):
    label.pack_forget()

def displayPlayed(window, cards, color):
    clear(window)
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
        smallCard(window, str(c), color).grid(row = row, column = col, padx = 1, pady = 1)

def deck(window, text):
    return bigCard(window, text, "snow4", "raised", "se")

def bigCard(window, text, color = "black", relief = "flat", anchor = "center"):
    label = cardLabel(window, text, color, relief, anchor)
    resize(label, 3)
    return label

def smallCard(window, text, color = "black", relief = "flat"):
    label = cardLabel(window, text, color, relief)
    resize(label, 1)
    return label

def cardLabel(window, text, color, relief, anchor = "center"):
    return tk.Label(window, text = text, fg = color,  highlightthickness = 1, highlightbackground = "black", relief = relief, anchor = anchor)

def resize(label, n):
    label.config(width = n, height = n)

if __name__ == "__main__":
    runVisualTestsInWindow(CardsTester)


