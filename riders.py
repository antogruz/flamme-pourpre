#!/usr/bin/env python3

class Riders:
    def __init__(self, riders):
        self.riders = riders

    def isFree(self, slot):
        for rider in self.riders:
            if rider.position() == slot:
                return False
        return True

