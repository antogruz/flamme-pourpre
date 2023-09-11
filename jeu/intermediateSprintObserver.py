#!/usr/bin/env python3

from miniraceObserver import MiniraceObserver
def createSprintObserver(sprintLastSpot, points):
    return MiniraceObserver(sprintLastSpot, SprintReward(points))

class SprintReward:
    def __init__(self, points):
        self.points = points

    def finished(self):
        return not self.points

    def reward(self, rider):
        rider.score += self.points.pop(0)


from track import Track
from trackAnalysis import getSections, countSquaresExcept
def getPointsForSprints(track):
    trackRealLength = countSquaresExcept(track, ["end"])
    farthestPossibleSprintLine = int((2 * trackRealLength) / 3)
    sections = getSections(track, ["normal", "descent"])
    sections = cutSectionsTo(sections, farthestPossibleSprintLine)
    sections = [ section for section in sections if length(section) >= 12 ]

    if not sections:
        return []

    return [(biggestSection(sections)[1] - 1, [1])]

def cutSectionsTo(sections, last):
    result = []
    for section in sections:
        if section[1] <= last:
            result.append(section)
        elif section[0] <= last:
            result.append((section[0], last))
    return result


def biggestSection(sections):
    return sorted(sections, key = length, reverse = True)[0]


def length(section):
    return section[1] - section[0] + 1


from unittests import runTests, assert_equals
class SprintsDetectorTest:
    def testNoSprintUnderTwelveSquares(self):
        track = Track([(11, "normal")])
        assert_equals([], getPointsForSprints(track))

    def testSprintBeforeAscent(self):
        track = Track([(12, "normal"), (1, "ascent"), (10, "normal")])
        assert_sprint_last_square(10, track)

    def testOnlyBiggestSection(self):
        track = Track([(12, "normal"), (1, "ascent"), (15, "normal"), (1, "ascent"), (12, "normal")])
        assert_sprint_last_square(26, track)

    def testDescent(self):
        track = Track([(12, "normal"), (1, "ascent"), (3, "normal"), (3, "descent"), (9, "normal"), (1, "ascent"), (12, "normal")])
        assert_sprint_last_square(26, track)

    def testNoSectionTooCloseOfTheEnd(self):
        track = Track([(12, "normal"), (1, "ascent"), (15, "normal"), (2, "ascent"), (5, "end")])
        assert_sprint_last_square(10, track)

    def testVeryBigSection(self):
        track = Track([(61, "normal"), (5, "end")])
        assert_sprint_last_square(39, track)

def assert_sprint_last_square(expected, track):
    assert_equals([(expected, [1])], getPointsForSprints(track))


if __name__ == "__main__":
    runTests(SprintsDetectorTest())



