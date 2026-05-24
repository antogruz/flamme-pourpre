#!/usr/bin/env python3

# Façade UI Tk autour de RidersDirector pour les coureurs du joueur humain.
#
# Un seul TkRidersDirector gère les N coureurs d'une équipe : il reçoit la
# liste des N triplets (cardFrame, specialFrame, talentsFrame) et un index
# interne avance à chaque make. Le RidersDirector métier sous-jacent est
# lui aussi réutilisé : RiderBuilder est suffisamment "auto-réinitialisant"
# (chaque buildX écrase le précédent) pour qu'on puisse enchaîner les
# makeXxx sans fuite d'état entre coureurs.
#
# Pour chaque coureur construit :
#   1) délègue la construction au directeur métier (deck, propulsor, profile);
#   2) enregistre l'apparence (name + shade + color) dans Appearances;
#   3) ajoute au DisplayBinder les displays "per-rider" (cartes en main,
#      talents, set opportuniste).
#
# Les bots, qui n'ont pas de frame dédiée, passent par TeamsDirector
# directement (cf. main/teamsDirector.py).

from decorators.riderDisplay import rouleurShade, sprinteurShade, grimpeurShade, opportunisticShade
from beau.cardsDisplay import CardsDisplay
from beau.opportunisticDisplay import OpportunisticDisplay
from beau.decorators.talentsDisplay import TalentsDisplay


class TkRidersDirector:
    def __init__(self, base, displayBinder, appearances, layouts):
        """layouts : liste de triplets (cardFrame, specialFrame, talentsFrame),
        un par coureur à construire (dans l'ordre des makeXxx successifs)."""
        self.base = base
        self.displayBinder = displayBinder
        self.appearances = appearances
        self.layouts = layouts
        self.index = 0

    def makeRouleur(self, oracle, color):
        rider = self.base.makeRouleur(oracle)
        self._registerAppearance(rider, "Rouleur", rouleurShade, color)
        self._addStandardDisplays(rider)
        return rider

    def makeSprinteur(self, oracle, color):
        rider = self.base.makeSprinteur(oracle)
        self._registerAppearance(rider, "Sprinteur", sprinteurShade, color)
        self._addStandardDisplays(rider)
        return rider

    def makeGrimpeur(self, oracle, color):
        rider = self.base.makeGrimpeur(oracle)
        self._registerAppearance(rider, "Grimpeur", grimpeurShade, color)
        self._addStandardDisplays(rider)
        return rider

    def makeOpportunistic(self, oracle, color, sets = ["goldenrod", "magenta"]):
        rider = self.base.makeOpportunistic(oracle, sets)
        self._registerAppearance(rider, "Opportunistic", opportunisticShade, color)
        cardFrame, specialFrame, talentsFrame = self._nextLayout()
        self.displayBinder.add(CardsDisplay(cardFrame, rider, self.appearances))
        self.displayBinder.add(TalentsDisplay(talentsFrame, rider))
        self.displayBinder.add(OpportunisticDisplay(specialFrame, _sortedSets(rider, sets), rider.propulsor.cards))
        return rider

    def _registerAppearance(self, rider, name, shade, color):
        self.appearances.register(rider, name, shade, color)

    def _addStandardDisplays(self, rider):
        cardFrame, _, talentsFrame = self._nextLayout()
        self.displayBinder.add(CardsDisplay(cardFrame, rider, self.appearances))
        self.displayBinder.add(TalentsDisplay(talentsFrame, rider))

    def _nextLayout(self):
        layout = self.layouts[self.index]
        self.index += 1
        return layout


def _sortedSets(rider, sets):
    return [
        sorted([card for card in rider.propulsor.cards.deck if color in str(card)])
        for color in sets
    ]
