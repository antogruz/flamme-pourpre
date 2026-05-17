#! /usr/bin/env python3

class Team:
    def __init__(self, riders, propulsor, oracle, progression):
        self.riders = riders
        self.propulsor = propulsor
        self.oracle = oracle
        self.progression = progression


class TeamProgression:
    """Interface for a team's progression between races.

    Default implementation does nothing (bot teams).
    """
    def progress(self):
        """Called after each race to apply progression."""
        pass


class DefaultOracle:
    """Trivial oracle for teams that don't need user input.

    Always picks the first option. Suitable for bots whose propulsion
    doesn't query the oracle (e.g. DicePropulsor, DrawOnePropulsor).
    """
    def pick(self, *_):
        return 0

    def pickRider(self, *_):
        return 0

    def pickWithRiders(self, *_):
        return 0