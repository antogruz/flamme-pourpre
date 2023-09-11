#!/usr/bin/env python3

from display import SquareDisplay

class MiniRacePointsDisplay:
    def __init__(self, observer, color):
        self.observer = observer
        self.color = color

    def displayOnTrack(self):
        if not self.observer.prizeGiver.points:
            return []
        return [SquareDisplay(self.observer.lastSquare, 2, self.color, self.observer.prizeGiver.points[0])]

