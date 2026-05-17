from positions import absolutePosition
from jeu.obstacles import ObstacleFactory
from jeu.positions import PlayOrderRule
from jeu.talent import Talent

class ImblocableClimber(Talent):
    def applyTo(self, personnage):
        mountainBehaviour = MountainBehaviour()
        personnage.addPlayOrderRule(mountainBehaviour)
        personnage.addObstacleFactory(mountainBehaviour)

    def displayRule(self):
        return "Grimpeur Imblocable: En montagne, jouez avant tous les coureurs. Seuls vos équipiers peuvent se placer sur les autres couloirs de votre case."

class MountainBehaviour(PlayOrderRule, ObstacleFactory):
    def __init__(self):
        self.willCrossAscent = False

    def keyFor(self, rider, snapshot):
        end = rider.personnage.movementRules.computeNewPosition(rider.position(), snapshot.energyOf(rider), snapshot.track, snapshot.obstaclesFor(rider))
        self.willCrossAscent = anyAscentBetween(snapshot.track, rider.position()[0], end[0])
        if self.willCrossAscent:
            return (-1, -absolutePosition(rider))
        return (0, -absolutePosition(rider))

    def isFree(self, position):
        if not self.willCrossAscent:
            return True
        return position[0] != self.rider.getSquare()

    def createFor(self, rider, track):
        self.rider = rider
        return self

def anyAscentBetween(track, start, end):
    for s in range(start, end + 1):
        if track.getRoadType(s) == "ascent":
            return True
    return False
