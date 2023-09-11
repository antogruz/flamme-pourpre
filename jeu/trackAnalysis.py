#!/usr/bin/env python3

from unittests import *
from track import Track


def getSections(track, types):
    return SectionsGetter(track, types).getSections()

class SectionsGetter:
    def __init__(self, track, types):
        self.track = track
        self.types = types
        self.cursor = 0
        self.sections = []

    def getSections(self):
        while self.getNextSection():
            pass
        return self.sections

    def getNextSection(self):
        sectionFirst = self.findNextSectionStart()
        if sectionFirst == -1:
            return False
        sectionLast = self.findEndOfSection()
        self.sections.append((sectionFirst, sectionLast))
        return True

    def findNextSectionStart(self):
        while self.track.getRoadType(self.cursor) not in self.types + ["out"]:
            self.cursor += 1
        if self.track.getRoadType(self.cursor) == "out":
            return -1
        return self.cursor

    def findEndOfSection(self):
        while self.track.getRoadType(self.cursor) in self.types:
            self.cursor += 1
        return self.cursor - 1

def countSquaresExcept(track, types):
    count = 0
    for roadType in getAllTypes(track):
        if roadType not in types:
            count += 1
    return count

def getAllTypes(track):
    return [ track.getRoadType(i) for i in range(len(track.squares)) ]

class AnalysisTester:
    def testNoSection(self):
        track = Track([(3, "normal")])
        assert_similars([], getSections(track, []))

    def testOneSection(self):
        track = Track([(3, "normal"), (4, "ascent")])
        assert_similars([(3, 6)], getSections(track, ["ascent"]))

if __name__ == "__main__":
    runTests(AnalysisTester())
