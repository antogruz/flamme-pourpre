#!/usr/bin/env python3

from unittests import *
from cards import Cards
import random

def createOpportunisticCards(baseCards, sets):
    cards = Cards(createDeck(baseCards, sets), random.shuffle, shuffleOnlyBaseCards)
    cards.sets = sets
    return cards

def createDeck(baseCards, sets):
    return [ SpecialCard(value, "base") for value in baseCards ] * 2 + [ SpecialCard(value, specialSet) for value in baseCards for specialSet in sets ]

def shuffleOnlyBaseCards(cards):
    cards.deck = cards.deck + cards.discard
    for specialSet in cards.sets:
        if not specialSet in [ card.specialSet for card in cards.deck ]:
            transferSet(specialSet, cards.played, cards.deck)
    transferSet("base", cards.played, cards.deck)

def transferSet(set, source, destination):
    for card in source[:]:
        if card.specialSet == set:
            source.remove(card)
            destination.append(card)

class Card:
    def __init__(self, value):
        self.value = value

class SpecialCard:
    def __init__(self, value, specialSet):
        self.value = value
        self.specialSet = specialSet
        if specialSet != "base":
            self.color = specialSet

class OpportunisticTester():
    def testDeckAfterPlayingNormalCard(self):
        cards = createOpportunisticCards([2, 3], ["magenta"])
        forcePlayCard(cards, SpecialCard(2, "base"))
        cards.newRace()
        assert_similars([2, 2, 2, 3, 3, 3], [c.value for c in cards.deck])

    def testOnlyOneCardPlayedFromASet(self):
        cards = createOpportunisticCards([2, 3], ["magenta", "yellow"])
        forcePlayCard(cards, SpecialCard(2, "magenta"))
        cards.newRace()
        assert_similars([2, 2, 2, 3, 3, 3, 3], [c.value for c in cards.deck])

    def testAllCardsFromASetPlayed(self):
        cards = createOpportunisticCards([2, 3], ["magenta", "yellow"])
        forcePlayCard(cards, SpecialCard(2, "magenta"))
        forcePlayCard(cards, SpecialCard(3, "magenta"))
        cards.newRace()
        assert_similars([2, 2, 2, 2, 3, 3, 3, 3], [c.value for c in cards.deck])

def forcePlayCard(cards, cardToPlay):
    for card in cards.deck:
        if card.value == cardToPlay.value and card.specialSet == cardToPlay.specialSet:
            cards.deck.remove(card)
            cards.played.append(card)
            return


if __name__ == "__main__":
    runTests(OpportunisticTester())


