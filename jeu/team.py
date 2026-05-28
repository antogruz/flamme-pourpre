#! /usr/bin/env python3

class Team:
    def __init__(self, riders, propulsor, oracle, progression):
        self.riders = riders
        self.propulsor = propulsor
        self.oracle = oracle
        self.progression = progression
        for rider in riders:
            rider.team = self


class TeamProgression:
    """Interface for a team's progression between races.

    Default implementation does nothing (bot teams).
    """
    def progress(self):
        """Called after each race to apply progression."""
        pass