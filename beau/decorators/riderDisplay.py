#!/usr/bin/env python3

rouleurShade = "o±ỏ"
sprinteurShade = "o/ỏ"
grimpeurShade = "o|ỏ"
opportunisticShade = "o\\ỏ"

from tokensDecorators import TokensDecorators

class RidersDisplay:
    def __init__(self, getRiders, trackDisplay, appearances):
        self.getRiders = getRiders
        self.trackDisplay = trackDisplay
        self.appearances = appearances

    def displayOnTrack(self):
        for r in self.getRiders():
            appearance = self.appearances.of(r)
            self.trackDisplay.setContent(r.position()[0], r.position()[1], appearance.shade, appearance.color)



from visualtests import *
from track import Track
from trackDisplay import TrackDisplay
from tkinterSpecific.boxes import BoxFactory
from appearances import Appearances
class DisplayTester(VisualTester):
    def testRiders(self):
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
        factory = BoxFactory(self.frame)
        trackDisplay = TrackDisplay(factory, track)
        rd = TokensDecorators(self.frame, trackDisplay)
        rd.addRoadDecorator(RidersDisplay(lambda: riders, trackDisplay, appearances))
        rd.update()


class Rider:
    def __init__(self, pos):
        self.pos = pos

    def position(self):
        return self.pos


if __name__ == "__main__":
    runVisualTestsInWindow(DisplayTester) 