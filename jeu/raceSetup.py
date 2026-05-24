#!/usr/bin/env python3

# Phase de placement initial des coureurs sur la zone de départ.
#
# Règle : on tire une équipe au sort, elle place un coureur
# sur l'emplacement le plus en avant disponible (toutes lanes d'une case
# remplies avant de reculer). On re-tire à chaque coureur posé jusqu'à
# ce que tous soient placés.
#
# Les RaceObserver passés en paramètre reçoivent onRiderPlaced(rider, square, lane)
# après chaque placement, ce qui permet aux UI d'animer la phase de setup.
#
# Si la zone "start" du track n'a pas assez de places pour tous les
# coureurs, ensureEnoughStartSpots(track, ridersCount) doit être appelé
# en amont pour préfixer la track avec des cases "start" supplémentaires.

import random
from track import Track
from trackAnalysis import getSections


def setRidersOnStart(teamsInRace, track, observers = None):
    observers = observers or []
    spots = startSpots(track)
    teamsToPlace = [t for t in teamsInRace if t.ridersToPlace]
    while teamsToPlace and spots:
        team = random.choice(teamsToPlace)
        square, lane = spots.pop(0)
        rider = team.placeChosenRider(square, lane)
        if rider:
            for observer in observers:
                observer.onRiderPlaced(rider, square, lane)
        if not team.ridersToPlace:
            teamsToPlace.remove(team)


def startSpots(track):
    sections = getSections(track, ["start"])
    if not sections:
        return []
    first, last = sections[0]
    spots = []
    for square in range(last, first - 1, -1):
        for lane in range(track.getLaneCount(square)):
            spots.append((square, lane))
    return spots


def ensureEnoughStartSpots(track, ridersCount):
    """Retourne une track avec au moins ridersCount places de départ.

    Si la zone "start" du track est déjà assez grande, retourne le track
    tel quel. Sinon, préfixe le track avec juste assez de cases "start"
    (au même nombre de lanes que la première case start existante) pour
    accueillir tous les coureurs.
    """
    spots = startSpots(track)
    if len(spots) >= ridersCount:
        return track
    lanes = track.getLaneCount(0)
    missing = ridersCount - len(spots)
    extraSquares = (missing + lanes - 1) // lanes
    return _prependStartSquares(track, extraSquares, lanes)


def _prependStartSquares(track, count, lanes):
    extended = Track([])
    extended.squares = [("start", lanes)] * count + list(track.squares)
    return extended


from unittests import assert_equals, runTests


class StartSpotsTest:
    def __before__(self):
        self.track = Track([(3, "start", 2), (5, "normal", 2)])

    def testEnoughSpots(self):
        extended = ensureEnoughStartSpots(self.track, 6)
        assert_equals(self.track.squares, extended.squares)

    def testFewerRidersThanSpots(self):
        extended = ensureEnoughStartSpots(self.track, 2)
        assert_equals(self.track.squares, extended.squares)

    def testOneMoreRider(self):
        extended = ensureEnoughStartSpots(self.track, 7)
        first, last = getSections(extended, ["start"])[0]
        assert_equals(0, first)
        assert_equals(3, last)
        assert_equals(4 * 2, len(startSpots(extended)))
        assert_equals("start", extended.getRoadType(0))
        assert_equals("normal", extended.getRoadType(4))

    def testFullExtraSquareNeeded(self):
        extended = ensureEnoughStartSpots(self.track, 8)
        assert_equals(8, len(startSpots(extended)))

    def testNeedSeveralExtraSquares(self):
        extended = ensureEnoughStartSpots(self.track, 11)
        assert_equals(12, len(startSpots(extended)))

    def testOriginalTrackUnchanged(self):
        ensureEnoughStartSpots(self.track, 20)
        assert_equals(8, len(self.track.squares))

    def testExtensionUsesLanesOfFirstStartSquare(self):
        track = Track([(2, "start", 3), (5, "normal", 2)])
        extended = ensureEnoughStartSpots(track, 10)
        assert_equals(3, extended.getLaneCount(0))


if __name__ == "__main__":
    runTests(StartSpotsTest())
