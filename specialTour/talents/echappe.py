#! /usr/bin/env python3


class Echappe:
    def applyTo(self, personnage):
        personnage.addBonusRule(InSmallLeadingGroupBonus())

    def displayRule(self):
        return "Échappé: Si vous êtes dans un groupe de tête de moins de la moitié des coureurs, ajoutez 1 à votre carte jouée."


class InSmallLeadingGroupBonus:
    def bonusFor(self, card, rider, snapshot):
        leadingGroup = snapshot.leadingGroup()
        if rider not in leadingGroup.riders:
            return 0
        if len(leadingGroup.riders) * 2 < len(snapshot.allRiders):
            return 1
        return 0
