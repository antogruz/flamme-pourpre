#!/usr/bin/env python3

# Implémentation Tk de AnimationBinder.
#
# Reçoit en référence le TkDisplayBinder coordonné parce que les animators
# Tk (RoadAnimator, EventAnimator) sont créés là-bas (ils ont besoin du
# trackDisplay du layout) et parce que le PlacementRefresher déclenche le
# refresh des displays pull.

from race import RaceObserver
from animationBinder import AnimationBinder


class TkAnimationBinder(AnimationBinder):
    def __init__(self, displays):
        self.displays = displays

    def placementObservers(self):
        return [PlacementRefresher(self.displays.refresh)]

    def raceObservers(self, race):
        return [self.displays.eventAnimator, self.displays.roadAnimator]


class PlacementRefresher(RaceObserver):
    """Déclenche un refresh global après chaque rider placé. Permet de voir
    les riders apparaître un à un sans coupler RidersDisplay à l'event."""

    def __init__(self, refresh):
        self.refresh = refresh

    def onRiderPlaced(self, rider, square, lane):
        self.refresh()
