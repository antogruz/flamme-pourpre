#! /usr/bin/env python3

from talent import Talent


class Poursuivant(Talent):
    def applyTo(self, personnage):
        personnage.addBonusRule(NotInLeadingGroupBonus())

    def displayRule(self):
        return "Poursuivant: Si vous n'êtes pas dans le groupe de tête, ajoutez 1 à votre carte jouée."


class NotInLeadingGroupBonus:
    def bonusFor(self, moves, rider, snapshot):
        if rider not in snapshot.leadingGroup().riders:
            return 1
        return 0
