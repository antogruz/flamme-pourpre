#! /usr/bin/env python3

import random
from cards import SimpleCard, FatigueCard
from deckPropulsor import EmptyCard

class DrawOnePropulsor:
    def __init__(self, cards, shuffle = random.shuffle):
        self.cards = [asMove(c) for c in cards]
        self.shuffle = shuffle
        self.newRace()

    def generateMoves(self):
        if self.index >= len(self.cards):
            return [EmptyCard()]
        move = self.cards[self.index]
        self.index += 1
        return [move]

    def newRace(self):
        self.index = 0
        self.shuffle(self.cards)

    def exhaust(self):
        pass


def asMove(raw):
    if hasattr(raw, "energy"):
        return raw
    if raw == "f":
        return FatigueCard()
    return SimpleCard(int(raw))
