#!/usr/bin/env python3

# Interface du "côté pull" de la UI.
#
# Une UI implémente DisplayBinder pour construire ses displays statiques
# (cards, talents, ranking, etc.) qui re-lisent l'état métier à chaque
# refresh. Pas d'animation ici : voir AnimationBinder pour le côté push.
#
# Cycle d'appels par EngineRunner pour un tour :
#   bindTour(tour)
#   pour chaque course :
#     bindRace(track, teamsInRace, modes, climberObservers, sprintObservers)
#     refresh()
#     [placement des riders, refresh entre chaque via AnimationBinder]
#     onRaceStarted(race)
#     refresh()
#     pour chaque tour de jeu :
#       refresh()


class DisplayBinder:
    def bindTour(self, tour):
        """Appelé une fois au début d'un tour multi-courses."""
        pass

    def bindRace(self, track, teamsInRace, modes,
                 climberObservers = (), sprintObservers = ()):
        """Appelé avant le placement initial des riders. La UI dispose de
        tout le contexte de course (track, équipes, observers de mini-jeux)
        pour préparer ses displays per-course. RidersDisplay/MiniRacePoints
        peuvent être affichés dès maintenant : les riders apparaîtront pendant
        le placement (lus en pull), les points de mini-jeu sont déjà visibles."""
        pass

    def onRaceStarted(self, race):
        """Appelé une fois la Race construite (après placement). La UI peut
        finaliser les displays qui dépendent de la Race (ranking, etc.)."""
        pass

    def refresh(self):
        """À appeler par l'engine après chaque mutation visible."""
        pass
