#!/usr/bin/env python3

from unittests import *
from cards import Cards
import random

def createOpportunisticCards(baseCards, specialColors):
    baseDeck, specialSets = createDeck(baseCards, specialColors)
    deck = baseDeck
    for specialSet in specialSets:
        deck += specialSet

    return Cards(deck, random.shuffle, [OpportunisticSetManager(cardsSet) for cardsSet in specialSets])

def createDeck(baseCards, specialColors):
    return baseCards * 2, [ [ str(value) + color for value in baseCards] for color in specialColors ]

class OpportunisticSetManager:
    def __init__(self, specialCards):
        self.specialCards = specialCards

    def modifyCards(self, cards):
        for card in self.specialCards:
            if card in cards.played:
                cards.played.remove(card)
        if self.noCardIn(cards.deck):
            cards.deck += self.specialCards

    def noCardIn(self, deck):
        for card in self.specialCards:
            if card in deck:
                return False
        return True


class OpportunisticTester():
    def testDeckAfterPlayingNormalCard(self):
        cards = createOpportunisticCards([2, 3], ["magenta"])
        playFromDeck(cards, 2)
        cards.newRace()
        assert_similars([2, 2, "2magenta", 3, 3, "3magenta"], cards.deck)

    def testOnlyOneCardPlayedFromASet(self):
        cards = createOpportunisticCards([2, 3], ["magenta", "yellow"])
        playFromDeck(cards, "2magenta")
        cards.newRace()
        assert_similars([2, 2, "2yellow", 3, 3, "3magenta", "3yellow"], cards.deck)

    def testAllCardsFromASetPlayed(self):
        cards = createOpportunisticCards([2, 3], ["magenta", "yellow"])
        originalDeck = cards.deck[:]
        playFromDeck(cards, "2magenta")
        playFromDeck(cards, "3magenta")
        cards.newRace()
        assert_similars(originalDeck, cards.deck)

def playFromDeck(cards, cardToPlay):
    cards.deck.remove(cardToPlay)
    cards.played.append(cardToPlay)

if __name__ == "__main__":
    runTests(OpportunisticTester())


