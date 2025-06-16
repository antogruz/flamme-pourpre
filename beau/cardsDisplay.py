#!/usr/bin/env python3

import tkinter as tk
from frames import Frames, clear
from cards import Cards
from beautifulCard import *

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

    def update(self):
        self.displayCards(self.rider.cards.inDeck(), self.rider.cards.discard, self.rider.cards.played)
        self.frame.update()

    def displayCards(self, deckSize, discard, played):
        self.deck.config(text = str(deckSize))
        self.discard.config(text = len(discard))
        if discard:
            self.discard.pack()
        else:
            hide(self.discard)
        destroy(self.allCardsDiscarded)
        self.allCardsDiscarded = [smallCard(self.fullDiscardFrame, createBeautifulCard(str(card), self.color)) for card in discard]
        toDisplay = sorted([ createBeautifulCard(str(card), self.color) for card in played], key = getValue)
        displayPlayed(self.playedFrame, toDisplay)

def getValue(niceCard):
    return int(niceCard.text)


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

def destroy(labels):
    for label in labels:
        label.destroy()

def displayPlayed(window, niceCards):
    clear(window)
    last = -1
    row = 0
    col = -1
    for c in niceCards:
        if getValue(c) == last:
            row += 1
        else:
            row = 0
            col += 1
        last = getValue(c)
        smallCard(window, c).grid(row = row, column = col, padx = 1, pady = 1)

def deck(window, text):
    label = bigCard(window, BeautifulCard(text, "snow4"))
    label.config(relief = "raised", anchor = "se")
    return label

def bigCard(window, niceCard):
    label = cardLabel(window, niceCard)
    resize(label, 3)
    return label

def smallCard(window, niceCard):
    label = cardLabel(window, niceCard)
    resize(label, 1)
    return label

def cardLabel(window, niceCard):
    return tk.Label(window, text = niceCard.text, fg = niceCard.color, bg = niceCard.background, highlightthickness = 1, highlightbackground = "black")

def resize(label, n):
    label.config(width = n, height = n)

from visualtests import VisualTester, runVisualTestsInWindow
class CardsTester(VisualTester):
    def testEmpty(self):
        display = CardsDisplay(self.frame, Rider())
        display.displayCards(0, [], [])

    def testAfterFirstRound(self):
        display = CardsDisplay(self.frame, Rider())
        display.displayCards(7, [2, 4, 5, "7magenta"], [9, 3, 2, 3, "3goldenrod", 5, 3, 5])

from decorators.riderDisplay import rouleurShade
class Rider:
    def __init__(self):
        self.shade = rouleurShade
        self.name = "Rouleur"
        self.color = "green"

if __name__ == "__main__":
    runVisualTestsInWindow(CardsTester)


