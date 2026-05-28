from talent import Talent
from jeu.exhaust import ExhaustionRule
from jeu.race import RaceObserver


class ColsEnSolo(Talent):
    def displayRule(self):
        return "Cols en solo: Vous ne prenez pas de fatigue si une partie de votre déplacement est en montagne."

    def applyTo(self, personnage):
        rule = ColsEnSoloRule(personnage)
        personnage.addExhaustionRule(rule)
        personnage.addRaceObserver(rule)


class ColsEnSoloRule(ExhaustionRule, RaceObserver):
    def __init__(self, personnage):
        self.personnage = personnage
        self.track = None
        self.crossedAscent = False

    def onRaceStart(self, track):
        self.track = track
        self.crossedAscent = False

    def onRiderMove(self, rider, start, end, obstacles, moves):
        if rider.personnage is not self.personnage:
            return
        if self.pathTouchesAscent(start[0], end[0]):
            self.crossedAscent = True

    def onTurnEnd(self):
        self.crossedAscent = False

    def exempts(self, rider):
        return rider.personnage is self.personnage and self.crossedAscent

    def pathTouchesAscent(self, startSquare, endSquare):
        for square in range(startSquare, endSquare + 1):
            if self.track.getRoadType(square) == "ascent":
                return True
        return False
