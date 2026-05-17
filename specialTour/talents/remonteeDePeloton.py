from track import streamable
from talent import Talent

class RemonteeDePeloton(Talent):
    def applyTo(self, personnage):
        personnage.addSlipstreamRule(RemonteeDePelotonRule())

    def displayRule(self):
        return "Remontée de peloton: Prend l'aspiration même au sein d'un groupe. Le fait qu’il y ait un autre coureur juste devant vous n’empêche pas l’aspiration du coureur devant lui."

class RemonteeDePelotonRule:
    def squaresEarned(self, rider, riders, track):
        if isSquareInFrontFree(rider, riders, 1):
            return 0
        if isSquareInFrontFree(rider, riders, 2):
            return 0
        if not streamable(track.getRoadType(rider.square)):
            return 0
        if not streamable(track.getRoadType(rider.square + 1)):
            return 0
        if not streamable(track.getRoadType(rider.square + 2)):
            return 0
        return 1

def isSquareInFrontFree(rider, riders, distance):
    for other in riders:
        if other.square == rider.square + distance:
            return False
    return True