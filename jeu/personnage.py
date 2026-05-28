#! /usr/bin/env python3

class Personnage():
    def __init__(self, movementRules, propulsor, energyRules):
        self.movementRules = movementRules
        self.propulsor = propulsor
        self.energyRules = energyRules
        self.bonusRules = []
        self.slipstreamRules = []
        self.groupSlipstreamRules = []
        self.playOrderRules = []
        self.exhaustionRules = []
        self.obstacleFactories = []
        self.talents = []
        self.raceObservers = []
        self.profile = None
        self.team = None

    def gainTalent(self, talent):
        self.talents.append(talent)
        talent.applyTo(self)

    def teammates(self):
        if not self.team:
            return []
        return [r for r in self.team.riders if r is not self]

    def addRaceObserver(self, observer):
        self.raceObservers.append(observer)

    def addBonusRule(self, rule):
        self.bonusRules.append(rule)

    def addSlipstreamRule(self, rule):
        self.slipstreamRules.append(rule)

    def addGroupSlipstreamRule(self, rule):
        self.groupSlipstreamRules.append(rule)

    def addPlayOrderRule(self, rule):
        self.playOrderRules.append(rule)

    def addExhaustionRule(self, rule):
        self.exhaustionRules.append(rule)

    def addObstacleFactory(self, factory):
        self.obstacleFactories.append(factory)
