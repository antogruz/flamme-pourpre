#!/usr/bin/env python3

import random
from unittests import *
from cards import Cards, SimpleCard

def createOpportunisticCards(baseCards, specialColors, shuffle = random.shuffle):
    baseDeck, specialSets = createDeck(baseCards, specialColors)
    deck = list(baseDeck)
    for specialSet in specialSets:
        deck += specialSet

    return Cards(deck, shuffle, [OpportunisticSetManager(cardsSet) for cardsSet in specialSets])

def createDeck(baseCards, specialColors):
    base = [SimpleCard(v) for v in baseCards] * 2
    specials = [[OpportunisticCard(v, color) for v in baseCards] for color in specialColors]
    return base, specials


class OpportunisticCard(SimpleCard):
    def __init__(self, number, color):
        super().__init__(number)
        self.color = color

    def label(self):
        return f"{self.number}{self.color}"



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
        playFromDeck(cards, "2")
        cards.newRace()
        assert_similars(["2", "2", "2magenta", "3", "3", "3magenta"], labels(cards.deck))

    def testOnlyOneCardPlayedFromASet(self):
        cards = createOpportunisticCards([2, 3], ["magenta", "yellow"])
        playFromDeck(cards, "2magenta")
        cards.newRace()
        assert_similars(["2", "2", "2yellow", "3", "3", "3magenta", "3yellow"], labels(cards.deck))

    def testAllCardsFromASetPlayed(self):
        cards = createOpportunisticCards([2, 3], ["magenta", "yellow"])
        originalLabels = labels(cards.deck)
        playFromDeck(cards, "2magenta")
        playFromDeck(cards, "3magenta")
        cards.newRace()
        assert_similars(originalLabels, labels(cards.deck))

def labels(cards):
    return [c.label() for c in cards]

def playFromDeck(cards, label):
    picked = [c for c in cards.deck if c.label() == label][0]
    cards.deck.remove(picked)
    cards.played.append(picked)

if __name__ == "__main__":
    runTests(OpportunisticTester())
