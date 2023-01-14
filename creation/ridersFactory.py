#!/usr/bin/env python3

from riderDisplay import *
from rider import *
import random
from cards import reshuffleAll, halfRecovery, fullRecovery

def createHumanRider(specialist):
    return createRider(specialist, reshuffleAll)

def createBotRider(specialist):
    return createRider(specialist, halfRecovery)

class Specialist:
    def __init__(self, name, deck, shade):
        self.name = name
        self.deck = deck
        self.shade = shade

def createRider(specialist, cardsBetweenRaces):
    rider = Rider(specialist.name, Cards(specialist.deck, random.shuffle, cardsBetweenRaces), None)
    rider.shade = specialist.shade
    return rider

def rouleurSpecialist():
    return Specialist("Rouleur", rouleurDeck(), rouleurShade)

def sprinteurSpecialist():
    return Specialist("Sprinteur", sprinteurDeck(), sprinteurShade)

def rouleurDeck():
    return threeTimes([3, 4, 5, 6, 7])

def sprinteurDeck():
    return threeTimes([2, 3, 4, 5, 9])

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

