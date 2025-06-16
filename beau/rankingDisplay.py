#!/usr/bin/env python3

from display import SquareDisplay, TokensDecorators

class RankingDisplay:
    def __init__(self, race):
        self.race = race
        self.lastTrackSquare = race.track.lastSquare()

    def displayOnTrack(self):
        return [ SquareDisplay(self.lastTrackSquare - i, 2, rider.color, rider.shade) for i, rider in enumerate(self.race.ranking()) ]


from visualtests import *
from track import Track
from riderDisplay import rouleurShade, sprinteurShade, Rider
from trackDisplay import TrackDisplayTkinter
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
        rd = TokensDecorators(self.frame, TrackDisplayTkinter(self.frame, track))
        rd.addRoadDecorator(RankingDisplay(FakeRace(track, riders)))
        rd.update()

class FakeRace:
    def __init__(self, track, riders):
        self.riders = riders
        self.track = track

    def ranking(self):
        return self.riders

if __name__ == "__main__":
    runVisualTestsInWindow(RankingDisplayTester)
