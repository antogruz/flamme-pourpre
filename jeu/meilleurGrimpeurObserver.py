#!/usr/bin/env python3

from miniraceObserver import MiniraceObserver
def createClimberObserver(mountainLastSpot, points, awardClimberPoints):
    return MiniraceObserver(mountainLastSpot, ClimberReward(points, awardClimberPoints))


class ClimberReward:
    def __init__(self, points, awardClimberPoints):
        self.points = points
        self.awardClimberPoints = awardClimberPoints

    def finished(self):
        return not self.points

    def reward(self, rider):
        self.awardClimberPoints(rider, self.points.pop(0))


from unittests import runTests, assert_equals, assert_similars

finDeCol = 6
class OneRiderTest:
    def __before__(self):
        self.awarded = {}
        self.observer = createClimberObserver(finDeCol, [1, 1], self.award)
        self.rider = RiderInRace()

    def award(self, personnage, points):
        self.awarded[personnage] = self.awarded.get(personnage, 0) + points

    def points(self, rider):
        return self.awarded.get(rider.personnage, 0)

    def logMoveAndEndTurn(self, start, end):
        self.rider.pos = (end, 0)
        self.observer.onRiderMove(self.rider, (start, 0), (end, 0))
        self.observer.onTurnEnd()

    def testRiderCrossEndOfClimb(self):
        self.logMoveAndEndTurn(3, finDeCol + 1)
        assert_equals(1, self.points(self.rider))

    def testRiderDontCrossEndOfClimb(self):
        self.logMoveAndEndTurn(3, finDeCol)
        assert_equals(0, self.points(self.rider))

    def testRiderAfterEndOfClimb(self):
        self.logMoveAndEndTurn(finDeCol + 1, finDeCol + 2)
        assert_equals(0, self.points(self.rider))

    def testRiderCumulatePoints(self):
        self.awarded[self.rider.personnage] = 3
        self.logMoveAndEndTurn(3, finDeCol + 1)
        assert_equals(4, self.points(self.rider))

    def testRiderMovesTwice(self):
        self.logMoveAndEndTurn(3, finDeCol + 1)
        self.logMoveAndEndTurn(finDeCol + 1, finDeCol + 2)
        assert_equals(1, self.points(self.rider))


class SeveralRidersTest:
    def __before__(self):
        self.awarded = {}
        self.observer = createClimberObserver(finDeCol, [2, 1], self.award)

    def award(self, personnage, points):
        self.awarded[personnage] = self.awarded.get(personnage, 0) + points

    def points(self, rider):
        return self.awarded.get(rider.personnage, 0)

    def logAndMove(self, rider, start, end):
        rider.pos = end
        self.observer.onRiderMove(rider, start, end)

    def testThreeRiders(self):
        riders = [ RiderInRace() for i in range(3) ]
        for i, r in enumerate(riders):
            self.logAndMove(r, (0, 0), (finDeCol + 1 + i, 0))
        self.observer.onTurnEnd()
        assert_equals(0, self.points(riders[0]))
        assert_equals(1, self.points(riders[1]))
        assert_equals(2, self.points(riders[2]))

class RiderInRace:
    def __init__(self):
        self.personnage = Rider()
        self.pos = (0, 0)

    def position(self):
        return self.pos

class Rider:
    pass

if __name__ == "__main__":
    runTests(OneRiderTest())
    runTests(SeveralRidersTest())
