from jeu.talent import Talent
from jeu.riderMove import MovementRules

class DescenteDeCol(Talent):
    def applyTo(self, personnage):
        personnage.movementRules = DescenteDeColMovementRules(personnage.movementRules)

    def displayRule(self):
        return "Descente de col: Vous avancez de 6 minimum en descente, ou vous ajoutez 2 à votre carte."

class DescenteDeColMovementRules(MovementRules):
    def __init__(self, base):
        self.base = base

    def computeNewPosition(self, startingPosition, energy, track, obstacles):
        if track.getRoadType(startingPosition[0]) == "descent":
            energy = max(6, energy + 2)
        return self.base.computeNewPosition(startingPosition, energy, track, obstacles)

    def findAvailableSlot(self, obstacles, startingPosition, distance, track):
        return self.base.findAvailableSlot(obstacles, startingPosition, distance, track)
