#!/usr/bin/env python3

from unittests import assert_equals


def tests():
    riderAtStart()
    riderMove()
    twoRiders()


def riderAtStart():
    race = Race()
    id = race.addRider(0, 0)
    assert_equals((0, 0), race.position(id))


def riderMove():
    race = Race()
    id = race.addRider(0, 0)
    race.move(id, 1)
    assert_equals((1, 0), race.position(id))


def twoRiders():
    race = Race()
    id1 = race.addRider(0, 0)
    id2 = race.addRider(0, 1)
    race.move(id2, 1)
    assert_equals((0, 0), race.position(id1))


class Race():
    def __init__(self):
        self.ridersCount = 0
        self.squares = []

    def addRider(self, square, lane):
        id = self.ridersCount
        self.squares.append(square)
        self.ridersCount += 1
        return id

    def position(self, rider):
        return (self.squares[rider], 0)

    def move(self, rider, n):
        self.squares[rider] += 1



tests()

