#!/usr/bin/env python3

# Étend une track en insérant `bonusSquares` cases "normal" à l'index `offset`.
# Utilisé par le mode SpecialTour pour allonger les courses au fil de la progression
# du joueur. L'offset correspond au nombre de cases occupées par les coureurs
# au départ : les cases bonus sont donc insérées juste après les coureurs.

from track import Track
from trackAnalysis import getSections
from unittests import assert_equals, runTests

def extendTrack(track, bonusSquares):
    sections = getSections(track, ["start"])
    return extendTrackAtOffset(track, bonusSquares, sections[0][1] + 1)

def extendTrackAtOffset(track, bonusSquares, offset):
    if bonusSquares == 0:
        return track
    lanes = track.getLaneCount(offset - 1)
    extra = [("normal", lanes)] * bonusSquares
    extended = Track([])
    extended.squares = list(track.squares[:offset]) + extra + list(track.squares[offset:])
    return extended


class ExtendTrackTest:
    def __before__(self):
        self.before = Track([(5, "start", 4), (5, "ascent", 8)])

    def testZeroExtensionReturnsSameContent(self):
        extended = extendTrack(self.before, 0)
        assert_equals(self.before.squares, extended.squares)

    def testInsertion(self):
        extended = extendTrack(self.before, 3)
        assert_equals("start", extended.getRoadType(4))
        assert_equals("normal", extended.getRoadType(5))
        assert_equals("ascent", extended.getRoadType(8))
        assert_equals(13, len(extended.squares))

    def testInsertedSquaresHaveLanesOfPreviousSquare(self):
        extended = extendTrack(self.before, 4)
        assert_equals(4, extended.getLaneCount(4))
        assert_equals(4, extended.getLaneCount(5))
        assert_equals(8, extended.getLaneCount(9))

    def testOriginalTrackIsUnchanged(self):
        extendTrack(self.before, 3)
        assert_equals(10, len(self.before.squares))


if __name__ == "__main__":
    runTests(ExtendTrackTest())
