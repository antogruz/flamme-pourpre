#!/usr/bin/env python3

# Implémentation Tk de UIBackend. Encapsule la construction des layouts,
# displays et observers d'animation pour une course pilotée par EngineRunner.
#
# Stateful : entre deux courses d'un même tour, conserve les `displayers`
# initiaux + le ResultsWindow ajouté à beforeTour. Pour chaque course,
# reconstruit le layout dans beforeRace et le détruit implicitement au
# beforeRace suivant (le tk.Frame est recréé).

from race import RaceObserver
from tokensDecorators import TokensDecorators
from trackDisplay import TrackDisplay
from tkinterSpecific.canvasBoxFactory import CanvasBoxFactory
from animation import EventAnimator, RoadAnimator
from raceLayout import RaceLayout
from eventDisplay import EventDisplay
from beau.resultsWindow import ResultsWindow
from decorators.miniracePointsDisplay import MiniRacePointsDisplay
from decorators.riderDisplay import RidersDisplay
from decorators.rankingDisplay import RankingDisplay
from uiBackend import UIBackend


class TkUIBackend(UIBackend):
    def __init__(self, window, clock, displayers, appearances):
        self.window = window
        self.clock = clock
        self.displayers = list(displayers)
        self.appearances = appearances
        self._reset()

    def _reset(self):
        self.tokensDecorators = None
        self.eventAnimator = None
        self.roadAnimator = None
        self.raceDisplayers = []
        self.placedRiders = []
        self.ridersDisplay = None

    def beforeTour(self, tour):
        self.displayers.append(ResultsWindow(self.window, tour, self.appearances))

    def beforeRace(self, track, teamsInRace, modes):
        self._reset()
        layout = RaceLayout(self.window)
        self.tokensDecorators, self.eventAnimator, self.roadAnimator = createDisplays(track, layout, self.clock, self.appearances)
        self.raceDisplayers = self.displayers + [self.tokensDecorators]
        self.ridersDisplay = RidersDisplay(self.placedRiders, self.tokensDecorators.trackDisplay, self.appearances)
        self.tokensDecorators.addRoadDecorator(self.ridersDisplay)

    def placementObservers(self):
        return [PlacementWatcher(self.placedRiders, self.refresh)]

    def raceObservers(self, race):
        self.tokensDecorators.addRoadDecorator(RankingDisplay(race, self.tokensDecorators.trackDisplay, self.appearances))
        return [self.eventAnimator, self.roadAnimator, self.ridersDisplay]

    def onClimberObserver(self, observer):
        self.tokensDecorators.addRoadDecorator(MiniRacePointsDisplay(observer, "red", self.tokensDecorators.trackDisplay))

    def onSprintObserver(self, observer):
        self.tokensDecorators.addRoadDecorator(MiniRacePointsDisplay(observer, "green", self.tokensDecorators.trackDisplay))

    def refresh(self):
        for d in self.raceDisplayers:
            d.update()


class PlacementWatcher(RaceObserver):
    def __init__(self, placedRiders, refresh):
        self.placedRiders = placedRiders
        self.refresh = refresh

    def onRiderPlaced(self, rider, square, lane):
        self.placedRiders.append(rider)
        self.refresh()


def createDisplays(track, layout, clock, appearances):
    factory = CanvasBoxFactory(layout.getTrackFrame())
    trackDisplay = TrackDisplay(factory, track)
    eventDisplay = EventDisplay(layout.getEventFrame(), appearances)
    eventAnimator = EventAnimator(eventDisplay)
    roadAnimator = RoadAnimator(layout.getTrackFrame(), trackDisplay, track, appearances, clock)
    tokensDecorators = TokensDecorators(layout.getTrackFrame(), trackDisplay)
    return tokensDecorators, eventAnimator, roadAnimator
