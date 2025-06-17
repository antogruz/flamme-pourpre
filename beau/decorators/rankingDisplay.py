#!/usr/bin/env python3

from tokensDecorators import TokensDecorators
from decorators.riderDisplay import rouleurShade, sprinteurShade, Rider

class RankingDisplay:
    def __init__(self, race, trackDisplay):
        self.race = race
        self.lastTrackSquare = race.track.lastSquare()
        self.trackDisplay = trackDisplay

    def displayOnTrack(self):
        for i, rider in enumerate(self.race.ranking()):
            self.trackDisplay.setContent(self.lastTrackSquare - i, 2, rider.shade, rider.color)


from visualtests import *
from track import Track
from trackDisplay import TrackDisplay
from tkinterSpecific.canvasBoxFactory import CanvasBoxFactory
class RankingDisplayTester(VisualTester):
    def testRanking(self):
        track = Track([(10, "normal")])
        riders = [
                Rider(rouleurShade, "green", (0, 0)),
                Rider(rouleurShade, "black", (0, 1)),
                Rider(rouleurShade, "red", (2, 0)),
                Rider(rouleurShade, "blue", (9, 1)),
                Rider(sprinteurShade, "green", (3, 1)),
                Rider(sprinteurShade, "black", (4, 0)),
                Rider(sprinteurShade, "red", (6, 2)),
                Rider(sprinteurShade, "blue", (8, 0))
            ]
        factory = CanvasBoxFactory(self.frame)
        trackDisplay = TrackDisplay(factory, track)
        rd = TokensDecorators(self.frame, trackDisplay)
        rd.addRoadDecorator(RankingDisplay(FakeRace(track, riders), trackDisplay))
        rd.update()

class FakeRace:
    def __init__(self, track, riders):
        self.riders = riders
        self.track = track

    def ranking(self):
        return self.riders

if __name__ == "__main__":
    runVisualTestsInWindow(RankingDisplayTester) 