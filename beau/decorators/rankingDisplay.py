#!/usr/bin/env python3

from tokensDecorators import TokensDecorators
from decorators.riderDisplay import rouleurShade, sprinteurShade, Rider

class RankingDisplay:
    def __init__(self, race, trackDisplay, appearances):
        self.race = race
        self.lastTrackSquare = race.track.lastSquare()
        self.trackDisplay = trackDisplay
        self.appearances = appearances

    def displayOnTrack(self):
        for i, rider in enumerate(self.race.ranking()):
            appearance = self.appearances.of(rider)
            self.trackDisplay.setContent(self.lastTrackSquare - i, 2, appearance.shade, appearance.color)


from visualtests import *
from track import Track
from trackDisplay import TrackDisplay
from tkinterSpecific.canvasBoxFactory import CanvasBoxFactory
from appearances import Appearances
class RankingDisplayTester(VisualTester):
    def testRanking(self):
        track = Track([(10, "normal")])
        appearances = Appearances()
        riders = []
        for shade, color, pos in [
                (rouleurShade, "green", (0, 0)),
                (rouleurShade, "black", (0, 1)),
                (rouleurShade, "red", (2, 0)),
                (rouleurShade, "blue", (9, 1)),
                (sprinteurShade, "green", (3, 1)),
                (sprinteurShade, "black", (4, 0)),
                (sprinteurShade, "red", (6, 2)),
                (sprinteurShade, "blue", (8, 0))
            ]:
            rider = Rider(pos)
            appearances.register(rider, "Coureur", shade, color)
            riders.append(rider)
        factory = CanvasBoxFactory(self.frame)
        trackDisplay = TrackDisplay(factory, track)
        rd = TokensDecorators(self.frame, trackDisplay)
        rd.addRoadDecorator(RankingDisplay(FakeRace(track, riders), trackDisplay, appearances))
        rd.update()

class FakeRace:
    def __init__(self, track, riders):
        self.riders = riders
        self.track = track

    def ranking(self):
        return self.riders

if __name__ == "__main__":
    runVisualTestsInWindow(RankingDisplayTester) 