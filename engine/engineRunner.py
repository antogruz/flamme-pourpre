#!/usr/bin/env python3

# Moteur de course agnostique de l'UI.
#
# EngineRunner orchestre la phase de setup (placement des riders),
# la création de la Race, l'ajout des observers (modes spéciaux),
# la boucle de tours, et la progression entre courses du SpecialTour.
#
# Il ne dépend pas de tkinter ni d'aucune autre techno d'affichage.
# Toute interaction avec l'UI passe par l'objet `ui` (cf. uiBackend.UIBackend).

from race import Race, TeamInRace
from raceSetup import setRidersOnStart
from specialTour.extendTrack import extendTrack
from meilleurGrimpeurObserver import createClimberObserver
from intermediateSprintObserver import createSprintObserver, getPointsForSprints
from cols import getPointsForClimbs


def noLog(ranking):
    pass


class SpecialModes:
    def __init__(self, bestClimber = None, intermediateSprint = None):
        self.bestClimber = bestClimber
        self.intermediateSprint = intermediateSprint


class EngineRunner:
    def __init__(self, ui):
        self.ui = ui

    def runTour(self, tour, tracksBuilders, bonusPerRace = 0):
        self.ui.beforeTour(tour)
        bonusSquares = 0
        for trackBuilder in tracksBuilders:
            track = extendTrack(trackBuilder(len(tour.teams)), bonusSquares)
            tour.newRace()
            self.runRace(track, tour.teams, tour.checkNewArrivals,
                         SpecialModes(bestClimber = tour.addClimberPoints,
                                      intermediateSprint = tour.addPoints))
            for team in tour.teams:
                team.progression.progress()
            bonusSquares += bonusPerRace
        self.ui.afterTour(tour)

    def runRace(self, track, teams, logRanking = noLog, modes = SpecialModes()):
        teamsInRace = [TeamInRace(team) for team in teams]
        self.ui.beforeRace(track, teamsInRace, modes)
        self.ui.refresh()

        setRidersOnStart(teamsInRace, track, self.ui.placementObservers())
        for team in teamsInRace:
            for rider in team.ridersInRace:
                rider.personnage.propulsor.newRace()

        race = Race(track, teamsInRace)
        for observer in self.ui.raceObservers(race):
            race.addObserver(observer)
        self.attachMiniRaces(race, track, modes)
        self.ui.refresh()

        while not race.isOver():
            race.newTurn()
            logRanking(race.ranking())
            self.ui.refresh()

        self.ui.afterRace(race)

    def attachMiniRaces(self, race, track, modes):
        if modes.bestClimber:
            for observer in createClimbsObservers(track, modes.bestClimber):
                race.addObserver(observer)
                self.ui.onClimberObserver(observer)
        if modes.intermediateSprint:
            for observer in createSprintsObservers(track, modes.intermediateSprint):
                race.addObserver(observer)
                self.ui.onSprintObserver(observer)


def createClimbsObservers(track, awardClimberPoints):
    return [createClimberObserver(lastAscentSquare, points, awardClimberPoints)
            for (points, lastAscentSquare) in getPointsForClimbs(track)]


def createSprintsObservers(track, awardPoints):
    return [createSprintObserver(lastSquare, points, awardPoints)
            for (lastSquare, points) in getPointsForSprints(track)]
