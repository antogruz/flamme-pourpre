#!/usr/bin/env python3

from unittests import Tester, assert_equals
from riderMove import Rider
from track import Track
from obstacles import Obstacles

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
        riders = [rider, Rider(1, 0), Rider(2, 1), Rider(3, 0), Rider(3, 1)]
        obstacles = Obstacles(riders)
        rider.move(4, self.track, obstacles)
        self.assert_positions([(0, 0), (1, 1), (2, 0), (3, 2), (4, 0)])

    def assert_positions(self, positions):
        assert_equals(positions, self.display.getPositions())


def createAnimated(square, lane, display):
    return AnimatedRider(Rider(square, lane), display)


class Display():
    def animate(self, rider, path):
        self.positions = path

    def getPositions(self):
        return self.positions

class AnimatedRider():
    def __init__(self, riderMove, display):
        self.riderMove = riderMove
        self.display = display

    def move(self, distance, track, obstacles):
        start = self.position()
        self.riderMove.move(distance, track, obstacles)
        path = findPath(obstacles, start, self.position())
        self.display.animate(self, path)

    def position(self):
        return self.riderMove.position()

    def getSquare(self):
        return self.riderMove.getSquare()

    def getSlipstream(self, track):
        return self.riderMove.getSlipstream(track)


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
