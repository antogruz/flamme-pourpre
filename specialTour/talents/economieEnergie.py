#! /usr/bin/env python3

from talent import Talent
from cards import Card

class EconomieEnergie(Talent):
    def applyTo(self, personnage):
        personnage.propulsor.addExtraChoice(SkipProvider())

    def displayRule(self):
        return "Économie d'énergie: Vous pouvez ne pas jouer de carte et faire 3."


class SkipProvider(Card):
    """Permanent extra that lets the player skip the hand and move 3 squares."""
    def label(self):
        return "(3)"

    def energy(self):
        return 3

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def onPlay(self, cards):
        cards.discardHand()
        return self

    def doesEndTurn(self):
        return True
