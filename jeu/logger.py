#!/usr/bin/env python3

from path import findPath

class Logger():
    def __init__(self):
        self.moves = []
        self.groups = []
        self.exhausted = []

    def logMove(self, rider, card, start, end, obstacles):
        path = findPath(obstacles, start, end)
        self.moves.append((rider, card, path))

    def logGroup(self, riders):
        self.groups.append([(rider, rider.position()) for rider in riders])

    def logExhaust(self, rider):
        self.exhausted.append(rider)

    def getMoves(self):
        return self.moves

    def getGroups(self):
        return self.groups

    def getExhausted(self):
        return self.exhausted


