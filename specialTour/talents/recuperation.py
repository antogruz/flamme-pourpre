from talent import Talent
from jeu.cards import removeExhausts
from jeu.race import RaceObserver

class Recuperation(Talent):
    def displayRule(self):
        return "Récupération: Quand vous jouez une carte 3 ou moins, enlevez une fatigue de votre défausse."

    def applyTo(self, personnage):
        personnage.addRaceObserver(RecuperationObserver(personnage))

class RecuperationObserver(RaceObserver):
    def __init__(self, personnage):
        self.personnage = personnage

    def onRiderMove(self, rider, start, end, obstacles, moves):
        if rider.personnage is not self.personnage:
            return
        if moves[0].energy() <= 3:
            removeExhausts(rider.personnage.propulsor.cards.discard, 1)
