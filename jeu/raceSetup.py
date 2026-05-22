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

import random
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
