#! /usr/bin/env python3

class Personnage():
    def __init__(self, movementRules, propulsor, energyRules):
        self.movementRules = movementRules
        self.propulsor = propulsor
        self.energyRules = energyRules
        self.talents = []
        self.raceObservers = []

    def gainTalent(self, talent):
        self.talents.append(talent)
        talent.applyTo(self)

    def addRaceObserver(self, observer):
        self.raceObservers.append(observer)
