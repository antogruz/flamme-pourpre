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

    def beforeTour(self, tour):
        self.displayers.append(ResultsWindow(self.window, tour, self.appearances))

    def beforeRace(self, track, teamsInRace, modes):
        self._reset()
        layout = RaceLayout(self.window)
        self.tokensDecorators, self.eventAnimator, self.roadAnimator = createDisplays(track, layout, self.clock, self.appearances)
        self.raceDisplayers = self.displayers + [self.tokensDecorators]
        self.tokensDecorators.addRoadDecorator(RidersDisplay(activeRidersOf(teamsInRace), self.tokensDecorators.trackDisplay, self.appearances))

    def placementObservers(self):
        return [PlacementRefresher(self.refresh)]

    def raceObservers(self, race):
        self.tokensDecorators.addRoadDecorator(RankingDisplay(race, self.tokensDecorators.trackDisplay, self.appearances))
        return [self.eventAnimator, self.roadAnimator]

    def onClimberObserver(self, observer):
        self.tokensDecorators.addRoadDecorator(MiniRacePointsDisplay(observer, "red", self.tokensDecorators.trackDisplay))

    def onSprintObserver(self, observer):
        self.tokensDecorators.addRoadDecorator(MiniRacePointsDisplay(observer, "green", self.tokensDecorators.trackDisplay))

    def refresh(self):
        for d in self.raceDisplayers:
            d.update()


class PlacementRefresher(RaceObserver):
    """Déclenche un refresh global après chaque rider placé. Permet de voir
    les riders apparaître un à un sans coupler RidersDisplay à l'event."""
    def __init__(self, refresh):
        self.refresh = refresh

    def onRiderPlaced(self, rider, square, lane):
        self.refresh()


def activeRidersOf(teamsInRace):
    """Renvoie un callable qui itère les riders encore en course à chaque appel."""
    return lambda: [r for team in teamsInRace for r in team.ridersInRace]


def createDisplays(track, layout, clock, appearances):
    factory = CanvasBoxFactory(layout.getTrackFrame())
    trackDisplay = TrackDisplay(factory, track)
    eventDisplay = EventDisplay(layout.getEventFrame(), appearances)
    eventAnimator = EventAnimator(eventDisplay)
    roadAnimator = RoadAnimator(layout.getTrackFrame(), trackDisplay, track, appearances, clock)
    tokensDecorators = TokensDecorators(layout.getTrackFrame(), trackDisplay)
    return tokensDecorators, eventAnimator, roadAnimator
