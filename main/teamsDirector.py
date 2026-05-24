#!/usr/bin/env python3

# Construit les équipes de bots. Chaque rider est créé via RidersDirector
# (métier) puis son apparence (name + shade + color) est enregistrée dans
# Appearances pour que les displays partagés (track, classement) puissent
# l'afficher. Les bots n'ont pas de displays per-rider (pas de cartes en
# main affichées, etc.), donc on ne passe pas par TkRidersDirector.

from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion
from ridersDirector import RidersDirector
from oracle import DefaultOracle
from decorators.riderDisplay import rouleurShade, sprinteurShade


class TeamsDirector:
    def __init__(self, appearances):
        self.appearances = appearances

    def makeStandardBots(self, color):
        return self._makeTeam(color, [
            ("Rouleur", rouleurShade, lambda d: d.makeRouleur(DefaultOracle())),
            ("Sprinteur", sprinteurShade, lambda d: d.makeSprinteur(DefaultOracle())),
        ])

    def makeDiceBots(self, color):
        return self._makeTeam(color, [
            ("Rouleur", rouleurShade, lambda d: d.makeDiceRider()),
            ("Sprinteur", sprinteurShade, lambda d: d.makeDiceSprinteur()),
        ])

    def makeMuscleTeam(self, color):
        return self._makeTeam(color, [
            ("Rouleur", rouleurShade, lambda d: d.makeMuscleRouleur()),
            ("Sprinteur", sprinteurShade, lambda d: d.makeMuscleSprinteur()),
        ])

    def _makeTeam(self, color, riderSpecs):
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        director = RidersDirector()
        for name, shade, make in riderSpecs:
            rider = make(director)
            self.appearances.register(rider, name, shade, color)
            tb.addRider(rider)
        return tb.getResult()
