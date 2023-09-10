#!/usr/bin/env python3

from meilleurGrimpeurObserver import ClimberObserver
from display import SquareDisplay

class ClimberPointsDisplay:
    def __init__(self, climberObserver):
        self.co = climberObserver

    def displayOnTrack(self):
        text = 0 if not self.co.points else self.co.points[0]
        return SquareDisplay(self.co.mountainLastSpot, 2, "red", text)


