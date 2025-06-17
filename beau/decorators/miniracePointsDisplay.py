#!/usr/bin/env python3

from tokensDecorators import TokensDecorators
lanesCount = 2

class MiniRacePointsDisplay:
    def __init__(self, observer, color, trackDisplay):
        self.observer = observer
        self.color = color
        self.trackDisplay = trackDisplay

    def displayOnTrack(self):
        if not self.observer.prizeGiver.points:
            return
        for i in range(lanesCount):
            self.trackDisplay.setContent(self.observer.lastSquare + i, lanesCount, self.observer.prizeGiver.points[0], self.color)

from visualtests import *
from meilleurGrimpeurObserver import createClimberObserver
from track import Track
from trackDisplay import TrackDisplay
from tkinterSpecific.boxes import BoxFactory
class MiniRaceDisplayTester(VisualTester):
    def testBoth(self):
        track = Track([(5, "start"), (12, "normal"), (9, "ascent"), (12, "normal"), (5, "end")])
        factory = BoxFactory(self.frame)
        trackDisplay = TrackDisplay(factory, track)
        rd = TokensDecorators(self.frame, trackDisplay)
        rd.addRoadDecorator(MiniRacePointsDisplay(createClimberObserver(15, [1]), "green", trackDisplay))
        rd.addRoadDecorator(MiniRacePointsDisplay(createClimberObserver(25, [5]), "red", trackDisplay))
        rd.update()



if __name__ == "__main__":
    runVisualTestsInWindow(MiniRaceDisplayTester) 