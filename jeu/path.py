#!/usr/bin/env python3

from unittests import Tester, assert_equals
from rider import Rider
from track import Track
from obstacles import Obstacles
from riderMove import Rider as RiderToken

class PathTester(Tester):
    def __before__(self):
        self.track = Track([(5, "normal")])

    def testNoMoves(self):
        obstacles = Obstacles([])
        assert_equals([(0, 0)], findPath(obstacles, (0, 0), (0, 0)))

    def testMoveOne(self):
        obstacles = Obstacles([])
        assert_equals([(0, 0), (1, 0)], findPath(obstacles, (0, 0), (1, 0)))

    def testMoveStraight(self):
        obstacles = Obstacles([])
        assert_equals([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], findPath(obstacles, (0, 0), (4, 0)))

    def testObstacles(self):
        riders = [RiderToken(0, 0), RiderToken(1, 0), RiderToken(2, 1), RiderToken(3, 0), RiderToken(3, 1)]
        obstacles = Obstacles(riders)
        assert_equals([(0, 0), (1, 1), (2, 0), (3, 2), (4, 0)], findPath(obstacles, (0, 0), (4, 0)))


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
    PathTester().runTests()
