#!/usr/bin/env python3

rouleurShade = "o±ỏ"
sprinteurShade = "o/ỏ"
grimpeurShade = "o|ỏ"
opportunisticShade = "o\\ỏ"

from tokensDecorators import TokensDecorators

class RidersDisplay:
    def __init__(self, riders, trackDisplay):
        self.riders = riders
        self.trackDisplay = trackDisplay

    def displayOnTrack(self):
        for r in self.riders:
            self.trackDisplay.setContent(r.position()[0], r.position()[1], r.shade, r.color)



from visualtests import *
from track import Track
from trackDisplay import TrackDisplayTkinter
class DisplayTester(VisualTester):
    def testTrack(self):
        track = Track([(1, "start"), (1, "normal"), (1, "ascent"), (1, "descent"), (1, "end")])
        TokensDecorators(self.frame, track)

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
        trackDisplay = TrackDisplayTkinter(self.frame, track)
        rd = TokensDecorators(self.frame, trackDisplay)
        rd.addRoadDecorator(RidersDisplay(riders, trackDisplay))
        rd.update()


class Rider:
    def __init__(self, shade, color, pos):
        self.shade = shade
        self.color = color
        self.pos = pos

    def position(self):
        return self.pos


if __name__ == "__main__":
    runVisualTestsInWindow(DisplayTester) 