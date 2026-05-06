#!/usr/bin/env python3

# Registre central de l'apparence des riders pour le display.
# jeu/ ne dépend pas de cette classe : les Personnage / RiderInRace
# n'ont pas de name/shade/color, c'est ici qu'on les retrouve.
# Peuplé à la construction des riders, lu par les displays.

class Appearance:
    def __init__(self, name, shade, color):
        self.name = name
        self.shade = shade
        self.color = color

class Appearances:
    def __init__(self):
        self._map = {}

    def register(self, personnage, name, shade, color):
        self._map[personnage] = Appearance(name, shade, color)

    def of(self, rider):
        # Tolère un Personnage (clé directe) ou un RiderInRace (.personnage).
        return self._map[getattr(rider, "personnage", rider)]
