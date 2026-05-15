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
