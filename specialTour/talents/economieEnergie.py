#! /usr/bin/env python3

from talent import Talent
from cards import TerminatingChoice
from deckPropulsor import EmptyCard

class EconomieEnergie(Talent):
    def applyTo(self, personnage):
        personnage.energyRules = BetterEmpty(personnage.energyRules, 3)
        personnage.propulsor.addExtraChoice(SkipProvider())

    def displayRule(self):
        return "Économie d'énergie: Vous pouvez ne pas jouer de carte et faire 3."


class BetterEmpty:
    def __init__(self, base, emptyValue):
        self.base = base
        self.emptyValue = emptyValue

    def energyFromMove(self, move):
        if move.label() == "":
            return self.emptyValue
        return self.base.energyFromMove(move)


class SkipProvider(TerminatingChoice):
    def label(self):
        return "(3)"

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def onPlay(self, cards):
        cards.discardHand()
        return EmptyCard()
