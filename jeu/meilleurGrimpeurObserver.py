#!/usr/bin/env python3

from unittests import runTests, assert_equals, assert_similars

finDeCol = 6
class OneRiderOneValueTest:
    def __before__(self):
        self.observer = ClimberObserver(finDeCol, [1])
        self.rider = Rider()

    def logMoveAndEndTurn(self, start, end):
        self.rider.pos = (end, 0)
        self.observer.logMove(self.rider, (start, 0), (end, 0))
        self.observer.endTurn()

    def testRiderCrossEndOfClimb(self):
        self.logMoveAndEndTurn(3, finDeCol + 1)
        assert_equals(1, self.rider.climberPoints)

    def testRiderDontCrossEndOfClimb(self):
        self.logMoveAndEndTurn(3, finDeCol)
        assert_equals(0, self.rider.climberPoints)

    def testRiderAfterEndOfClimb(self):
        self.logMoveAndEndTurn(finDeCol + 1, finDeCol + 2)
        assert_equals(0, self.rider.climberPoints)

    def testRiderCumulatePoints(self):
        self.rider.climberPoints = 3
        self.logMoveAndEndTurn(3, finDeCol + 1)
        assert_equals(4, self.rider.climberPoints)

class TwoRidersTest:
    def __before__(self):
        self.observer = ClimberObserver(finDeCol, [2, 1])

    def logAndMove(self, rider, start, end):
        rider.pos = end
        self.observer.logMove(rider, start, end)

    def testThreeRiders(self):
        riders = [ Rider() for i in range(3) ]
        for i, r in enumerate(riders):
            self.logAndMove(r, (0, 0), (finDeCol + 1 + i, 0))
        self.observer.endTurn()
        assert_equals(0, riders[0].climberPoints)
        assert_equals(1, riders[1].climberPoints)
        assert_equals(2, riders[2].climberPoints)


class Rider:
    def __init__(self):
        self.climberPoints = 0
        self.pos = (0, 0)

    def position(self):
        return self.pos


from positions import headToTail

class ClimberObserver:
    def __init__(self, mountainLastSpot, points):
        self.mountainLastSpot = mountainLastSpot
        self.points = points
        self.ridersThatClimbedThisTurn = []

    def logMove(self, rider, start, end):
        if not self.points:
            return
        if start[0] <= self.mountainLastSpot and end[0] > self.mountainLastSpot:
            self.saveRider(rider)

    def saveRider(self, rider):
        self.ridersThatClimbedThisTurn.append(rider)

    def endTurn(self):
        for rider in headToTail(self.ridersThatClimbedThisTurn):
            self.givePoints(rider)

    def givePoints(self, rider):
        if not self.points:
            return
        rider.climberPoints += self.points.pop(0)



if __name__ == "__main__":
    runTests(OneRiderOneValueTest())
    runTests(TwoRidersTest())
