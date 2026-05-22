#!/usr/bin/env python3

# Interface ducktype des UI consommées par EngineRunner.
#
# Toutes les méthodes ont une implémentation no-op par défaut, donc une UI
# n'a besoin de surcharger que ce qui l'intéresse. NoopUIBackend permet
# de faire tourner une course en headless (tests, IA, automatisation).

class UIBackend:
    """Hooks de cycle de vie consommés par EngineRunner.

    Sequence d'appels pour un tour :
      beforeTour(tour)
      pour chaque course :
        beforeRace(track, teamsInRace, modes)
        refresh()
        [setRidersOnStart utilise placementObservers()]
        [Race construite]
        [raceObservers(race) ajoutés à la Race]
        [observers mini-races ajoutés via onClimberObserver/onSprintObserver]
        refresh()
        pour chaque tour de jeu :
          refresh()
        afterRace(race)
      afterTour(tour)
    """

    def beforeTour(self, tour):
        """Appelé une seule fois au début d'un tour multi-courses."""
        pass

    def afterTour(self, tour):
        """Appelé une seule fois en fin de tour."""
        pass

    def beforeRace(self, track, teamsInRace, modes):
        """Avant le placement initial. L'UI peut créer fenêtres, displays, decorators."""
        pass

    def placementObservers(self):
        """Observers ajoutés à setRidersOnStart pour réagir à chaque coureur posé."""
        return []

    def raceObservers(self, race):
        """Observers ajoutés à la Race après sa construction."""
        return []

    def onClimberObserver(self, observer):
        """Notifié pour chaque observer de mini-course de meilleur grimpeur."""
        pass

    def onSprintObserver(self, observer):
        """Notifié pour chaque observer de mini-course de sprint intermédiaire."""
        pass

    def refresh(self):
        """Rafraîchit les displays entre deux phases du moteur."""
        pass

    def afterRace(self, race):
        """Appelé une fois la course terminée."""
        pass


class NoopUIBackend(UIBackend):
    """Aucun affichage. Utile pour les tests headless et l'automatisation."""
    pass
