#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
import tkinter as tk
from frames import Frames
from cards import Cards

class CardsTester(VisualTester):
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
    fullDiscard = subFrames.new()
    displayDeck(framesLine[0], deckSize)
    displayDiscard(framesLine[1], fullDiscard, discard, rider.color)
    displayPlayed(framesLine[2], sorted(played), rider.color)


def displayRider(window, rider):
    tk.Label(window, text = rider.name + " " + rider.shade, fg = rider.color).pack()

def displayDeck(window, cardsCount):
    deck(window, cardsCount).pack()

def displayDiscard(deckWindow, fullWindow, cards, color):
    if not cards:
        return
    discardDeck = deck(deckWindow, len(cards))
    discardDeck.pack()
    allCardsDiscarded = [smallCard(fullWindow, card, color) for card in cards]
    discardDeck.bind("<Button-1>", lambda e:toggleDiscard(allCardsDiscarded))

def toggleDiscard(cardLabels):
    for label in cardLabels:
        if label.winfo_ismapped():
            label.pack_forget()
        else:
            label.pack(side="left")


def displayPlayed(window, cards, color):
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


