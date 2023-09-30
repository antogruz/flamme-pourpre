#!/usr/bin/env python3

from display import SquareDisplay

class MiniRacePointsDisplay:
    def __init__(self, observer, color):
        self.observer = observer
        self.color = color

    def displayOnTrack(self):
        if not self.observer.prizeGiver.points:
            return []
        return [ SquareDisplay(self.observer.lastSquare + i, 2, self.color, self.observer.prizeGiver.points[0]) for i in range(2) ]

from visualtests import *
from display import RoadDisplay
from meilleurGrimpeurObserver import createClimberObserver
from track import Track
class MiniRaceDisplayTester(VisualTester):
    def testBoth(self):
        track = Track([(5, "start"), (12, "normal"), (9, "ascent"), (12, "normal"), (5, "end")])
        rd = RoadDisplay(self.frame, track)
        rd.addRoadDecorator(MiniRacePointsDisplay(createClimberObserver(15, [1]), "green"))
        rd.addRoadDecorator(MiniRacePointsDisplay(createClimberObserver(25, [5]), "red"))
        rd.update()



if __name__ == "__main__":
    runVisualTestsInWindow(MiniRaceDisplayTester)

