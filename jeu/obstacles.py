#!/usr/bin/env python3

class Obstacles:
    def __init__(self, obstacles):
        self.obstacles = obstacles

    def isFree(self, slot):
        for o in self.obstacles:
            if o.position() == slot:
                return False
        return True

