#!/usr/bin/env python3

# Interface Oracle : moyen pour le moteur de demander un choix à l'extérieur.
# Implémentée par les UIs (TkUserChoice, etc.), ou par DefaultOracle pour
# les équipes qui n'ont pas besoin de choisir (bots avec propulsion automatique).
#
# Toutes les méthodes retournent un index (int) dans la liste proposée.


class Oracle:
    """Interface pour obtenir un choix d'un agent externe (humain ou IA)."""

    def pick(self, choices, instruction = ""):
        """Choisit parmi une liste d'options arbitraires. Retourne l'index."""
        pass

    def pickWithRiders(self, choices, instruction = ""):
        """Choisit parmi une liste de (rider, texte). Retourne l'index."""
        pass


class DefaultOracle(Oracle):
    """Oracle trivial qui choisit toujours la première option.

    Convient aux bots dont la propulsion n'interroge pas l'oracle
    (DicePropulsor, DrawOnePropulsor, etc.).
    """
    def pick(self, *_):
        return 0

    def pickWithRiders(self, *_):
        return 0
