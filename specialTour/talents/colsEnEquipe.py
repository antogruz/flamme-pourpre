from talent import Talent
from positions import tailToHead

class ColsEnEquipe(Talent):
    def applyTo(self, personnage):
        personnage.addGroupSlipstreamRule(TeamMountainSlipstream(personnage))

    def displayRule(self):
        return "Cols en équipe: Vous êtes aspiré en montagne et aspirez vos alliés en montagne (1 case)."


class TeamMountainSlipstream:
    def __init__(self, climber):
        self.climber = climber

    def apply(self, riders, track, observers, obstacles):
        affinity = [self.climber] + self.climber.teammates()
        credits = {p: 1 for p in affinity if p is not self.climber}
        climberPulled = [False]
        changed = True
        while changed:
            changed = False
            for rider in tailToHead(riders):
                if rider.personnage not in affinity:
                    continue
                if not self.hasCredit(rider, credits, climberPulled):
                    continue
                if not self.canBePulled(rider, riders, track, affinity):
                    continue
                origin = rider.position()
                rider.earnSquares(1, track, obstacles)
                if rider.position() == origin:
                    continue
                for observer in observers:
                    observer.onSlipstream([(rider, origin, rider.position())])
                changed = True
                self.spendCredit(rider, credits, climberPulled, affinity)

    def hasCredit(self, rider, credits, climberPulled):
        if rider.personnage is self.climber:
            return not climberPulled[0]
        return credits.get(rider.personnage, 0) > 0

    def spendCredit(self, rider, credits, climberPulled, affinity):
        if rider.personnage is self.climber:
            climberPulled[0] = True
            for personnage in affinity:
                if personnage is self.climber:
                    continue
                credits[personnage] = credits.get(personnage, 0) + 1
        else:
            credits[rider.personnage] -= 1

    def canBePulled(self, rider, riders, track, affinity):
        if not self.pathTouchesAscent(rider, track):
            return False
        if self.outsiderInFront(rider, riders, affinity):
            return False
        return self.aspiratorAtPlusTwo(rider, riders, affinity)

    def pathTouchesAscent(self, rider, track):
        for d in range(3):
            if track.getRoadType(rider.square + d) == "ascent":
                return True
        return False

    def outsiderInFront(self, rider, riders, affinity):
        for other in riders:
            if other is rider:
                continue
            if other.square != rider.square + 1:
                continue
            if other.personnage not in affinity:
                return True
        return False

    def aspiratorAtPlusTwo(self, rider, riders, affinity):
        isClimber = rider.personnage is self.climber
        for other in riders:
            if other.square != rider.square + 2:
                continue
            if isClimber:
                return True
            if other.personnage in affinity:
                return True
        return False
