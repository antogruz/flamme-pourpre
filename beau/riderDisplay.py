#!/usr/bin/env python3

rouleurShade = "o±ỏ"
sprinteurShade = "o/ỏ"
grimpeurShade = "o|ỏ"
opportunisticShade = "o\\ỏ"

from display import SquareDisplay, TokensDecorators

class RidersDisplay:
    def __init__(self, riders):
        self.riders = riders

    def displayOnTrack(self):
        return [ SquareDisplay(r.position()[0], r.position()[1], r.color, r.shade) for r in self.riders ]



from visualtests import *
from track import Track
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
        rd = TokensDecorators(self.frame, track)
        rd.addRoadDecorator(RidersDisplay(riders))
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
