#!/usr/bin/env python3

# Interface de choix utilisateur, indépendante de toute UI.
#
# Une UI implémente Menu pour permettre au moteur de poser une question
# à l'utilisateur (mode de jeu, nombre de courses, type de bots...). Les
# choix sont des valeurs arbitraires (str, int, callable, ...).
#
# Distincte d'Oracle : Oracle est consulté par le moteur DANS la course
# (choix d'une carte, etc.). Menu est consulté HORS course pour la
# configuration de la partie.


class Menu:
    def choose(self, choices, title = ""):
        """Demande à l'utilisateur de choisir une option dans choices.

        Retourne directement l'option choisie (pas son index)."""
        pass

    def chooseLabeled(self, labeledChoices, title = ""):
        """Variante : labeledChoices est une liste de tuples (label, value).
        L'utilisateur voit les labels, la value choisie est retournée."""
        pass
