#!/usr/bin/env python3

# Vue figée de la course à un instant donné, partagée entre tous les coureurs.
# Une instance par tour, créée au début (avant tout mouvement) et passée aux règles
# qui ont besoin du contexte de course (BonusRules, EnergyRules contextuelles, etc.).
# Permet aux talents de connaître la situation d'un coureur (groupes, peloton de tête)
# sans coupler les talents à la classe Race.

from groups import computeGroups


class RaceSnapshot:
    def __init__(self, allRiders, track, obstacles):
        self.allRiders = allRiders
        self.track = track
        self.obstacles = obstacles
        self.groups = None
        self.energies = None

    def setEnergies(self, energies):
        self.energies = energies

    def energyOf(self, rider):
        return self.energies[rider]

    def getGroups(self):
        if self.groups is None:
            self.groups = computeGroups(self.allRiders)
        return self.groups

    def leadingGroup(self):
        return self.getGroups()[-1]

    def groupOf(self, rider):
        for group in self.getGroups():
            if rider in group.riders:
                return group
        return None
