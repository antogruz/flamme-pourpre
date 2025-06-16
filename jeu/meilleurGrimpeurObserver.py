#!/usr/bin/env python3

from unittests import runTests, assert_equals, assert_similars

finDeCol = 6
class OneRiderTest:
    def __before__(self):
        self.observer = createClimberObserver(finDeCol, [1, 1])
        self.rider = Rider()

    def logMoveAndEndTurn(self, start, end):
        self.rider.pos = (end, 0)
        self.observer.onRiderMove(self.rider, (start, 0), (end, 0))
        self.observer.onTurnEnd()

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

    def testRiderMovesTwice(self):
        self.logMoveAndEndTurn(3, finDeCol + 1)
        self.logMoveAndEndTurn(finDeCol + 1, finDeCol + 2)
        assert_equals(1, self.rider.climberPoints)


class SeveralRidersTest:
    def __before__(self):
        self.observer = createClimberObserver(finDeCol, [2, 1])

    def logAndMove(self, rider, start, end):
        rider.pos = end
        self.observer.onRiderMove(rider, start, end)

    def testThreeRiders(self):
        riders = [ Rider() for i in range(3) ]
        for i, r in enumerate(riders):
            self.logAndMove(r, (0, 0), (finDeCol + 1 + i, 0))
        self.observer.onTurnEnd()
        assert_equals(0, riders[0].climberPoints)
        assert_equals(1, riders[1].climberPoints)
        assert_equals(2, riders[2].climberPoints)

class Rider:
    def __init__(self):
        self.climberPoints = 0
        self.pos = (0, 0)

    def position(self):
        return self.pos


from miniraceObserver import MiniraceObserver
def createClimberObserver(mountainLastSpot, points):
    return MiniraceObserver(mountainLastSpot, ClimberReward(points))


class ClimberReward:
    def __init__(self, points):
        self.points = points

    def finished(self):
        return not self.points

    def reward(self, rider):
        rider.climberPoints += self.points.pop(0)


if __name__ == "__main__":
    runTests(OneRiderTest())
    runTests(SeveralRidersTest())
