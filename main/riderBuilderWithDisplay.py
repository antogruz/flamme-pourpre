#!/usr/bin/env python3

from jeu.riderBuilder import RiderBuilder
from beau.cardsDisplay import CardsDisplay
from beau.opportunisticDisplay import OpportunisticDisplay
import random

class RiderBuilderWithDisplay:
    """
    Builder qui implémente la même interface que RiderBuilder 
    mais enregistre aussi les displays dans un registry fourni.
    """
    
    def __init__(self, displayRegistry, cardFrame, specialFrame):
        self.riderBuilder = RiderBuilder()
        self.displayRegistry = displayRegistry
        self.cardFrame = cardFrame
        self.specialFrame = specialFrame
        self.displayFactories = []

    def buildTexts(self, shade, name):
        self.riderBuilder.buildTexts(shade, name)
        
    def buildOracle(self, oracle):
        self.riderBuilder.buildOracle(oracle)
        
    def buildDeck(self, originalCards, shuffle = random.shuffle, endOfRaceDecksManagers = []):
        self.riderBuilder.buildDeck(originalCards, shuffle, endOfRaceDecksManagers)
        self.displayFactories.append(CardsDisplayFactory(self.cardFrame))

        
    def buildOpportunisticDeck(self, baseCards, sets=["goldenrod", "magenta"], shuffle = random.shuffle, endOfRaceDecksManagers = []):
        self.riderBuilder.buildOpportunisticDeck(baseCards, sets, shuffle, endOfRaceDecksManagers)
        self.displayFactories.append(CardsDisplayFactory(self.cardFrame))
        self.displayFactories.append(OpportunisticDisplayFactory(self.specialFrame, sets))

        
    def buildDice(self, moves):
        self.riderBuilder.buildDice(moves)
        
    def buildPropulsor(self, propulsor):
        self.riderBuilder.buildPropulsor(propulsor)
        
    def buildMovementRules(self, movementRules):
        self.riderBuilder.buildMovementRules(movementRules)
        
    def getResult(self):
        rider = self.riderBuilder.getResult()
        for displayFactory in self.displayFactories:
            display = displayFactory.create(rider)
            self.displayRegistry.register(display)
        return rider

class CardsDisplayFactory:
    def __init__(self, cardFrame):
        self.cardFrame = cardFrame

    def create(self, rider):
        return CardsDisplay(self.cardFrame, rider)

class OpportunisticDisplayFactory:
    def __init__(self, specialFrame, sets):
        self.specialFrame = specialFrame
        self.sets = sets

    def create(self, rider):
        sorted_sets = [ sorted([card for card in rider.propulsor.cards.deck if color in str(card)]) 
                for color in self.sets
            ]
        return OpportunisticDisplay(self.specialFrame, sorted_sets, rider.propulsor.cards)