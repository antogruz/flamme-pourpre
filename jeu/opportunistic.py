#!/usr/bin/env python3

from unittests import *
from rider import Rider
from cards import Cards
import random

def createOpportunistic(baseCards, sets):
    cards = Cards(createDeck(baseCards, sets), random.shuffle, shuffleOnlyBaseCards)
    cards.sets = sets
    rider = Rider("Opportunistic", cards, None)
    return rider

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
        rider = createOpportunistic([2, 3], ["magenta"])
        forcePlayCard(rider, SpecialCard(2, "base"))
        rider.cards.newRace()
        assert_similars([2, 2, 2, 3, 3, 3], [c.value for c in rider.cards.deck])

    def testOnlyOneCardPlayedFromASet(self):
        rider = createOpportunistic([2, 3], ["magenta", "yellow"])
        forcePlayCard(rider, SpecialCard(2, "magenta"))
        rider.cards.newRace()
        assert_similars([2, 2, 2, 3, 3, 3, 3], [c.value for c in rider.cards.deck])

    def testAllCardsFromASetPlayed(self):
        rider = createOpportunistic([2, 3], ["magenta", "yellow"])
        forcePlayCard(rider, SpecialCard(2, "magenta"))
        forcePlayCard(rider, SpecialCard(3, "magenta"))
        rider.cards.newRace()
        assert_similars([2, 2, 2, 2, 3, 3, 3, 3], [c.value for c in rider.cards.deck])

def forcePlayCard(rider, cardToPlay):
    for card in rider.cards.deck:
        if card.value == cardToPlay.value and card.specialSet == cardToPlay.specialSet:
            rider.cards.deck.remove(card)
            rider.cards.played.append(card)
            return


if __name__ == "__main__":
    runTests(OpportunisticTester())


