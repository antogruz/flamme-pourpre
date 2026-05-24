#!/usr/bin/env python3

# Moteur de course agnostique de l'UI.
#
# EngineRunner orchestre la phase de setup (placement des riders),
# la création de la Race, l'ajout des observers (modes spéciaux),
# la boucle de tours, et la progression entre courses du SpecialTour.
#
# Il ne dépend pas de tkinter ni d'aucune autre techno d'affichage.
# Toute interaction UI passe par deux interfaces distinctes :
#   - displays : DisplayBinder (côté pull, refresh régulier)
#   - animations : AnimationBinder (côté push, RaceObservers d'animation)

from race import Race, TeamInRace
from raceSetup import setRidersOnStart, ensureEnoughStartSpots
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
    def __init__(self, displays, animations):
        self.displays = displays
        self.animations = animations

    def runTour(self, tour, tracksBuilders, bonusPerRace = 0):
        self.displays.bindTour(tour)
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

    def runRace(self, track, teams, logRanking = noLog, modes = SpecialModes()):
        teamsInRace = [TeamInRace(team) for team in teams]
        ridersCount = sum(len(t.ridersToPlace) for t in teamsInRace)
        track = ensureEnoughStartSpots(track, ridersCount)
        climberObservers = self._createClimberObservers(track, modes)
        sprintObservers = self._createSprintObservers(track, modes)

        self.displays.bindRace(track, teamsInRace, modes, climberObservers, sprintObservers)
        self.displays.refresh()

        setRidersOnStart(teamsInRace, track, self.animations.placementObservers())
        for team in teamsInRace:
            for rider in team.ridersInRace:
                rider.personnage.propulsor.newRace()

        race = Race(track, teamsInRace)
        for observer in self.animations.raceObservers(race):
            race.addObserver(observer)
        for observer in climberObservers + sprintObservers:
            race.addObserver(observer)

        self.displays.onRaceStarted(race)
        self.displays.refresh()

        while not race.isOver():
            race.newTurn()
            logRanking(race.ranking())
            self.displays.refresh()

    def _createClimberObservers(self, track, modes):
        if not modes.bestClimber:
            return []
        return [createClimberObserver(lastAscentSquare, points, modes.bestClimber)
                for (points, lastAscentSquare) in getPointsForClimbs(track)]

    def _createSprintObservers(self, track, modes):
        if not modes.intermediateSprint:
            return []
        return [createSprintObserver(lastSquare, points, modes.intermediateSprint)
                for (lastSquare, points) in getPointsForSprints(track)]
