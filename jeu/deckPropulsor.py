#! /usr/bin/env python3

class DeckPropulsor:
    def __init__(self, cards, oracle):
        self.cards = cards
        self.oracle = oracle

    def generateMove(self):
        cards = self.cards.draw()
        if not cards:
            return 2
        card = self.pickCard(cards)
        self.cards.play(card)
        return getCardValue(card)
    
    def newRace(self):
        self.cards.newRace()
    
    def pickCard(self, cards):
        return cards[self.pick(cards, "Play a card")]
    
    def pick(self, list, instruction):
        choice = self.oracle.pick(list, instruction)
        if choice < 0 or choice >= len(list):
            return 0
        return choice

    def exhaust(self):
        self.cards.discard.append("f")


def getCardValue(card):
    if card == "f" or card == "":
        return 2
    return extractNumberFrom(card)

import re
def extractNumberFrom(card):
    return int(re.sub("[a-z]||[A-Z]", "", str(card)))

from unittests import *
from cards import Cards

class DeckPropulsorTest:
    def testPlayFirstCard(self):
        cards = Cards([9, 3, "f", 5])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        assert_equals(9, propulsor.generateMove())
        assert_equals(3, propulsor.generateMove())
        assert_equals(2, propulsor.generateMove())
        assert_equals(5, propulsor.generateMove())
        assert_equals(2, propulsor.generateMove())

class ChoiceDoer():
    def __init__(self, always):
        self.always = always

    def pick(self, possibilities, *_):
        return self.always

if __name__ == "__main__":
    runTests(DeckPropulsorTest())