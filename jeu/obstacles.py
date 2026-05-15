#!/usr/bin/env python3

class Obstacles:
    def __init__(self, obstacles):
        self.obstacles = obstacles

    def isFree(self, slot):
        return all(o.isFree(slot) for o in self.obstacles)


class DefaultRiderObstacle:
    def __init__(self, rider):
        self.rider = rider

    def isFree(self, position):
        return self.rider.position() != position


def obstaclesFromRiders(riders):
    return Obstacles([DefaultRiderObstacle(r) for r in riders])

class ObstacleFactory:
    """Interface for producing extra obstacles attached to a rider.

    Implement this to expose obstacles (mountain blocking, walls, hazard zones, etc.)
    that other riders should see when computing their movement.
    Race assembles these obstacles, opt-out for teammates of the rider that owns them.
    """
    def createFor(self, rider, track):
        """Build and return the obstacle that represents `rider` on the given `track`."""
        pass