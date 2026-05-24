#!/usr/bin/env python3

# Interface du "côté push" de la UI.
#
# Une UI implémente AnimationBinder pour fournir les RaceObservers qui vont
# animer les événements transient (mouvements, slipstream, exhaust, carte
# jouée, placement). Pas de display statique ici : voir DisplayBinder.


class AnimationBinder:
    def placementObservers(self):
        """Observers attachés à setRidersOnStart (phase de placement).

        Typiquement un observer qui déclenche un refresh du DisplayBinder
        après chaque coureur placé, pour donner un effet d'apparition.
        """
        return []

    def raceObservers(self, race):
        """Observers attachés à la Race après sa construction.

        Typiquement les animators de mouvement, de carte jouée, etc.
        """
        return []
