#!/usr/bin/env python3

# Builder Tk qui construit un Personnage et l'enregistre dans le registre
# Appearances avec son nom, sa shade et sa couleur.
# Utilisé pour les riders qui doivent être affichés (track, classement…)
# sans avoir de widget propre.

from jeu.riderBuilder import RiderBuilder


class RiderBuilderWithAppearance(RiderBuilder):
    def __init__(self, appearances):
        super().__init__()
        self.appearances = appearances
        self._name = None
        self._shade = None
        self._color = None

    def buildAppearance(self, name, shade, color):
        self._name = name
        self._shade = shade
        self._color = color

    def getResult(self):
        rider = super().getResult()
        self.appearances.register(rider, self._name, self._shade, self._color)
        return rider
