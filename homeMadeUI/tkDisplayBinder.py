#!/usr/bin/env python3

# Implémentation Tk de DisplayBinder.
#
# Stateful : entre deux courses d'un même tour, conserve les displays durables
# (cards/talents/opportunistic per rider + results) ajoutés via add() ou bindTour.
# Pour chaque course, reconstruit le layout dans bindRace ; le tk.Frame de la
# précédente course est implicitement détruit par recréation du layout.
#
# Expose en attributs eventAnimator/roadAnimator pour que le TkAnimationBinder
# coordonné puisse les retourner comme observers de Race (couplage assumé
# entre les deux côtés Tk : le DisplayBinder possède le layout, l'AnimationBinder
# s'en sert).

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
from displayBinder import DisplayBinder


class TkDisplayBinder(DisplayBinder):
    def __init__(self, window, clock, appearances):
        self.window = window
        self.clock = clock
        self.appearances = appearances
        self.displayers = []
        self._reset()

    def add(self, display):
        """Ajoute un display durable rafraîchi à chaque refresh()."""
        self.displayers.append(display)

    def _reset(self):
        self.tokensDecorators = None
        self.eventAnimator = None
        self.roadAnimator = None
        self.raceDisplayers = []

    def bindTour(self, tour):
        self.add(ResultsWindow(self.window, tour, self.appearances))

    def bindRace(self, track, teamsInRace, modes,
                 climberObservers = (), sprintObservers = ()):
        self._reset()
        layout = RaceLayout(self.window)
        self.tokensDecorators, self.eventAnimator, self.roadAnimator = _createDisplays(track, layout, self.clock, self.appearances)
        self.raceDisplayers = self.displayers + [self.tokensDecorators]
        self.tokensDecorators.addRoadDecorator(RidersDisplay(activeRidersOf(teamsInRace), self.tokensDecorators.trackDisplay, self.appearances))
        for obs in climberObservers:
            self.tokensDecorators.addRoadDecorator(MiniRacePointsDisplay(obs, "red", self.tokensDecorators.trackDisplay))
        for obs in sprintObservers:
            self.tokensDecorators.addRoadDecorator(MiniRacePointsDisplay(obs, "green", self.tokensDecorators.trackDisplay))

    def onRaceStarted(self, race):
        self.tokensDecorators.addRoadDecorator(RankingDisplay(race, self.tokensDecorators.trackDisplay, self.appearances))

    def refresh(self):
        for d in self.raceDisplayers:
            d.update()


def activeRidersOf(teamsInRace):
    """Callable qui itère les riders encore en course à chaque appel."""
    return lambda: [r for team in teamsInRace for r in team.ridersInRace]


def _createDisplays(track, layout, clock, appearances):
    factory = CanvasBoxFactory(layout.getTrackFrame())
    trackDisplay = TrackDisplay(factory, track)
    eventDisplay = EventDisplay(layout.getEventFrame(), appearances)
    eventAnimator = EventAnimator(eventDisplay)
    roadAnimator = RoadAnimator(layout.getTrackFrame(), trackDisplay, track, appearances, clock)
    tokensDecorators = TokensDecorators(layout.getTrackFrame(), trackDisplay)
    return tokensDecorators, eventAnimator, roadAnimator
