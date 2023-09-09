#!/usr/bin/env python3

from tracks import *

def getPointsForClimbs(track):
    mountains = findMountainsSections(track)
    allClimbs = [ (getClimbPoints(last + 1 - first), last) for (first, last) in mountains ]
    return [ climb for climb in allClimbs if climb[0]]

def findMountainsSections(track):
    sections = []
    i = 0
    while True:
        sectionStart = findNextMountain(track, i)
        if sectionStart == -1:
            return sections
        sectionEnd = findLastMountain(track, sectionStart)
        sections.append((sectionStart, sectionEnd))
        i = sectionEnd + 1

def findNextMountain(track, i):
    while track.getRoadType(i) not in ["ascent", "out"]:
        i += 1
    if track.getRoadType(i) == "out":
        return -1
    return i

def findLastMountain(track, i):
    while track.getRoadType(i) == "ascent":
        i += 1
    return i - 1


def getClimbPoints(length):
    if length <= 4:
        return []
    if length <= 6:
        return [1]
    if length <= 8:
        return [2, 1]
    if length <= 10:
        return [5, 3, 2, 1]
    return [10, 8, 6, 4, 2, 1]

from unittests import assert_equals, runTests, assert_similars
class ClimbsDetectionTest():
    def testClassicissima(self):
        track = classicissima()
        assert_similars([([5, 3, 2, 1], 23), ([1], 44)], getPointsForClimbs(track))



if __name__ == "__main__":
    runTests(ClimbsDetectionTest())
