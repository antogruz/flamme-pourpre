#!/usr/bin/env python3

from riderDisplay import *
from rider import *
import random
from cards import Cards, ExhaustRecovery
from opportunisticDisplay import OpportunisticDisplay


class SimpleDeckRiderFactory:
    def __init__(self, deck):
        self.deck = deck

    def createRider(self, endOfRaceDecksManagers):
        return Rider(Cards(self.deck, random.shuffle, endOfRaceDecksManagers))

    def createSpecialDisplay(self, frame):
        return NothingDisplay()

class NothingDisplay:
    def update(self, *_):
        pass

class OpportunisticRiderFactory:
    def __init__(self, baseCards):
        self.baseCards = baseCards
        self.sets = ["goldenrod", "magenta"]
        self.cards = createOpportunisticCards(self.baseCards, self.sets)

    def createRider(self, endOfRaceDecksManagers):
        self.cards.endOfRaceDecksManagers += endOfRaceDecksManagers
        return Rider(self.cards)

    def createSpecialDisplay(self, frame):
        return OpportunisticDisplay(frame, [sorted([ card for card in self.cards.deck if color in str(card)]) for color in self.sets], self.cards)



class Specialist:
    def __init__(self, name, factory, shade):
        self.name = name
        self.shade = shade
        self.factory = factory

    def createRider(self, endOfRaceDecksManagers):
        rider = self.factory.createRider(endOfRaceDecksManagers)
        rider.name = self.name
        rider.shade = self.shade
        return rider

    def createSpecialDisplay(self, frame):
        return self.factory.createSpecialDisplay(frame)

def rouleurSpecialist():
    return Specialist("Rouleur", SimpleDeckRiderFactory(rouleurDeck()), rouleurShade)

def sprinteurSpecialist():
    return Specialist("Sprinteur", SimpleDeckRiderFactory(sprinteurDeck()), sprinteurShade)

def grimpeurSpecialist():
    return Specialist("Grimpeur", SimpleDeckRiderFactory(grimpeurDeck()), grimpeurShade)

def opportunisticSpecialist():
    return Specialist("Opportuniste", OpportunisticRiderFactory([2, 3, 4, 5, 9]), opportunisticShade)

def rouleurDeck():
    return threeTimes([3, 4, 5, 6, 7])

def sprinteurDeck():
    return threeTimes([2, 3, 4, 5, 9])

def grimpeurDeck():
    return [3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7, 7]

def threeTimes(five):
    return [ card for card in five for i in range(3) ]


# Idée de formation des riders
#
#def createRider(deck, shade, color, name):
#    rider = Rider(Cards(deck, random.shuffle))
#    giveDisplay(rider, shade, color, name)
#    giveMovement(rider)
#
#def giveDisplay(rider, shade, color, name):
#    rider.shade = shade
#    rider.color = color
#    rider.name = name
#
#def giveMovement(rider):
#    rider.riderMove = riderMove.Rider(0, 0)

