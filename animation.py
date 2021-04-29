#!/usr/bin/env python3

from unittests import Tester, assert_equals
from rider import Rider
from track import Track
from obstacles import Obstacles
from riderMove import Rider as RiderToken

class AnimatedTester(Tester):
    def __init__(self):
        self.track = Track([(5, "normal")])
        self.display = Display()

    def testNoMoves(self):
        obstacles = Obstacles([])
        rider = createAnimated(0, 0, self.display)
        rider.move(0, self.track, obstacles)
        self.assert_positions([(0, 0)])

    def testMoveOne(self):
        obstacles = Obstacles([])
        rider = createAnimated(0, 0, self.display)
        rider.move(1, self.track, obstacles)
        self.assert_positions([(0, 0), (1, 0)])

    def testMoveStraight(self):
        obstacles = Obstacles([])
        rider = createAnimated(0, 0, self.display)
        rider.move(4, self.track, obstacles)
        self.assert_positions([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)])

    def testObstacles(self):
        rider = createAnimated(0, 0, self.display)
        riders = [rider, RiderToken(1, 0), RiderToken(2, 1), RiderToken(3, 0), RiderToken(3, 1)]
        obstacles = Obstacles(riders)
        rider.move(4, self.track, obstacles)
        self.assert_positions([(0, 0), (1, 1), (2, 0), (3, 2), (4, 0)])

    def testExhaust(self):
        rider = createAnimated(0, 0, self.display)
        rider.exhaust()
        assert_equals(rider, self.display.exhausted)


    def assert_positions(self, positions):
        assert_equals(positions, self.display.getPositions())


from cards import Cards
def createAnimated(square, lane, display):
    return AnimatedRider("Tac", Cards([]), RiderToken(square, lane), display)

class Display():
    def animate(self, rider, path):
        self.positions = path

    def exhaust(self, rider):
        self.exhausted = rider

    def getPositions(self):
        return self.positions

class AnimatedRider(Rider):
    def __init__(self, name, cards, riderMove, display):
        Rider.__init__(self, name, cards, riderMove)
        self.display = display

    def move(self, distance, track, obstacles):
        start = self.position()
        Rider.move(self, distance, track, obstacles)
        path = findPath(obstacles, start, self.position())
        self.display.animate(self, path)

    def exhaust(self):
        self.display.exhaust(self)
        Rider.exhaust(self)


def findPath(obstacles, start, end):
    if start[0] == end[0]:
        return [end]

    next = findNextEmpty(obstacles, start, end)
    return [start] + findPath(obstacles, next, end)

def findNextEmpty(obstacles, start, end):
    nextSquare = start[0] + 1
    if nextSquare == end[0]:
        return end

    for lane in range(2):
        if obstacles.isFree((nextSquare, lane)):
            return nextSquare, lane

    return nextSquare, 2



if __name__ == "__main__":
    AnimatedTester().runTests()
