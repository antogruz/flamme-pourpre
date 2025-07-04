#!/usr/bin/env python3

rouleurShade = "o±ỏ"
sprinteurShade = "o/ỏ"
grimpeurShade = "o|ỏ"
opportunisticShade = "o\\ỏ"

from tokensDecorators import TokensDecorators

class RidersDisplay:
    def __init__(self, riders, trackDisplay):
        self.riders = list(riders)
        self.trackDisplay = trackDisplay

    def displayOnTrack(self):
        for r in self.riders:
            if not r.arrived:
                self.trackDisplay.setContent(r.position()[0], r.position()[1], r.shade, r.color)



from visualtests import *
from track import Track
from trackDisplay import TrackDisplay
from tkinterSpecific.boxes import BoxFactory
class DisplayTester(VisualTester):
    def testRiders(self):
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
        factory = BoxFactory(self.frame)
        trackDisplay = TrackDisplay(factory, track)
        rd = TokensDecorators(self.frame, trackDisplay)
        rd.addRoadDecorator(RidersDisplay(riders, trackDisplay))
        rd.update()


class Rider:
    def __init__(self, shade, color, pos):
        self.shade = shade
        self.color = color
        self.pos = pos
        self.arrived = False

    def position(self):
        return self.pos


if __name__ == "__main__":
    runVisualTestsInWindow(DisplayTester) 