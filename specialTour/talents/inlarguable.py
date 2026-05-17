from track import streamable
from groups import computeGroups
from talent import Talent

class Inlarguable(Talent):
    def applyTo(self, personnage):
        personnage.addSlipstreamRule(InlarguableRule())

    def displayRule(self):
        return "Inlarguable: Bénéficie de l'aspiration même à 2 cases d'écart du coureur de devant. Ne fonctionne pas contre une échappée."

class InlarguableRule:
    def squaresEarned(self, rider, riders, track):
        if not isSquareInFrontFree(rider, riders, 1):
            return 0
        if not isSquareInFrontFree(rider, riders, 2):
            return 0
        if isSquareInFrontFree(rider, riders, 3):
            return 0
        for d in range(4):
            if not streamable(track.getRoadType(rider.square + d)):
                return 0
        if aspiratorIsInEscape(rider, riders):
            return 0
        return 2

def isSquareInFrontFree(rider, riders, distance):
    for other in riders:
        if other.square == rider.square + distance:
            return False
    return True

def aspiratorIsInEscape(rider, riders):
    leadingGroup = computeGroups(riders)[-1]
    if len(leadingGroup.riders) * 2 >= len(riders):
        return False
    for other in leadingGroup.riders:
        if other.square == rider.square + 3:
            return True
    return False
