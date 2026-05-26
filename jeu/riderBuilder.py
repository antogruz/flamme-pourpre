#! /usr/bin/env python3

import random
from cards import Cards, createCards
from deckPropulsor import DeckPropulsor
from dicePropulsor import DicePropulsor
from personnage import Personnage
from opportunistic import createOpportunisticCards
from energyRules import EnergyRules
from riderMove import MovementRules

class RiderBuilder:
    def __init__(self):
        self.oracle = None
        self.cards = None
        self.propulsor = None
        self.movementRules = MovementRules()
        self.energyRules = EnergyRules()

    def buildEnergyRules(self, energyRules):
        self.energyRules = energyRules

    def buildOracle(self, oracle):
        self.oracle = oracle

    def buildDeck(self, originalCards, shuffle = random.shuffle, endOfRaceDecksManagers = None):
        self.cards = Cards(createCards(originalCards), shuffle, endOfRaceDecksManagers)
        self.propulsor = DeckPropulsor(self.cards, self.oracle)

    def buildOpportunisticDeck(self, baseCards, sets = ["goldenrod", "magenta"], shuffle = random.shuffle, endOfRaceDecksManagers = None):
        self.cards = createOpportunisticCards(baseCards, sets, shuffle)
        if endOfRaceDecksManagers:
            self.cards.endOfRaceDecksManagers += endOfRaceDecksManagers
        self.propulsor = DeckPropulsor(self.cards, self.oracle)

    def buildDice(self, moves):
        self.propulsor = DicePropulsor(moves)

    def buildPropulsor(self, propulsor):
        self.propulsor = propulsor

    def buildMovementRules(self, movementRules):
        self.movementRules = movementRules

    def getResult(self):
        return Personnage(self.movementRules, self.propulsor, self.energyRules)
