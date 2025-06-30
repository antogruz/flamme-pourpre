#! /usr/bin/env python3

class Team:
    def __init__(self, color, riders, propulsor, oracle):
        self.color = color
        self.riders = riders
        self.propulsor = propulsor
        self.oracle = oracle

    def score(self):
        return sum([r.score for r in self.riders])