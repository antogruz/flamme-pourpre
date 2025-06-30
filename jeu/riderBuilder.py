#! /usr/bin/env python3

import random
from cards import Cards
from deckPropulsor import DeckPropulsor
from dicePropulsor import DicePropulsor
from newRider import NewRider
from opportunistic import createOpportunisticCards

class RiderBuilder:
    def __init__(self):
        self.shade = None
        self.name = None
        self.oracle = None
        self.cards = None
        self.propulsor = None
        self.movementRules = None
        self.color = None

    def buildTexts(self, shade, name):
        self.shade = shade
        self.name = name

    def buildOracle(self, oracle):
        self.oracle = oracle

    def buildDeck(self, originalCards, shuffle = random.shuffle, endOfRaceDecksManagers = []):
        self.cards = Cards(originalCards, shuffle, endOfRaceDecksManagers)
        self.propulsor = DeckPropulsor(self.cards, self.oracle)

    def buildOpportunisticDeck(self, baseCards, sets = ["goldenrod", "magenta"], shuffle = random.shuffle, endOfRaceDecksManagers = []):
        self.cards = createOpportunisticCards(baseCards, sets, shuffle)
        self.cards.endOfRaceDecksManagers += endOfRaceDecksManagers
        self.propulsor = DeckPropulsor(self.cards, self.oracle)

    def buildDice(self, moves):
        self.propulsor = DicePropulsor(moves)

    def buildPropulsor(self, propulsor):
        self.propulsor = propulsor

    def buildMovementRules(self, movementRules):
        self.movementRules = movementRules

    def getResult(self):
        rider = NewRider(self.name, self.movementRules, self.propulsor)
        rider.shade = self.shade
        rider.color = self.color
        rider.time = 0
        return rider

    