#!/usr/bin/env python3

from meilleurGrimpeurObserver import ClimberObserver
from display import SquareDisplay

class ClimberPointsDisplay:
    def __init__(self, climberObserver):
        self.co = climberObserver

    def displayOnTrack(self):
        if not self.co.points:
            return []
        return [SquareDisplay(self.co.mountainLastSpot, 2, "red", self.co.points[0])]


