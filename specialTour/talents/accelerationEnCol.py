from talent import Talent
from deckPropulsor import CombiningChoice


class AccelerationEnCol(Talent):
    def applyTo(self, personnage):
        uncapped = UncappedAscentRules(personnage.movementRules)
        personnage.movementRules = uncapped
        personnage.propulsor.addExtraChoice(AccelerationChoice(uncapped))

    def displayRule(self):
        return ("Accélération en col : une fois par course, jouez une carte de "
                "votre main en ignorant la limite de 5 cases en montagne.")


class AccelerationChoice(CombiningChoice):
    def __init__(self, uncapped):
        self.uncapped = uncapped
        self.remainingUses = 1

    def label(self):
        return "Accélération en col"

    def isAvailable(self):
        return self.remainingUses > 0

    def combine(self, value, propulsor):
        self.uncapped.bypass = True
        self.remainingUses -= 1
        return value

    def newRace(self):
        self.remainingUses = 1


class UncappedAscentRules:
    def __init__(self, base):
        self.base = base
        self.bypass = False

    def computeNewPosition(self, startingPosition, energy, track, obstacles):
        if self.bypass:
            self.bypass = False
            track = FlattenedAscentTrack(track)
        return self.base.computeNewPosition(startingPosition, energy, track, obstacles)

    def findAvailableSlot(self, obstacles, startingPosition, distance, track):
        return self.base.findAvailableSlot(obstacles, startingPosition, distance, track)


class FlattenedAscentTrack:
    def __init__(self, base):
        self.base = base

    def getRoadType(self, square):
        road = self.base.getRoadType(square)
        return "normal" if road == "ascent" else road

    def getLaneCount(self, square):
        return self.base.getLaneCount(square)

    def previousPosition(self, square, lane):
        return self.base.previousPosition(square, lane)
