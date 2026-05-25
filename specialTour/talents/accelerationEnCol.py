from jeu.talent import Talent
from jeu.deckPropulsor import ExtraChoice

class AccelerationEnCol(Talent):
    def applyTo(self, personnage):
        uncapped = UncappedAscentRules(personnage.movementRules)
        personnage.movementRules = uncapped
        personnage.propulsor.addExtraChoice(
            AccelerationChoice(personnage.propulsor, uncapped))

    def displayRule(self):
        return ("Accélération en col : une fois par course, jouez une carte de "
                "votre main en ignorant la limite de 5 cases en montagne.")


class AccelerationChoice(ExtraChoice):
    LABEL = "Accélération en col"

    def __init__(self, propulsor, uncapped):
        self.propulsor = propulsor
        self.uncapped = uncapped
        self.remainingUses = 1
        self.nextLabel = self.LABEL

    def label(self):
        result = self.nextLabel
        self.nextLabel = self.LABEL
        return result

    def isAvailable(self):
        return self.remainingUses > 0

    def newRace(self):
        self.remainingUses = 1

    def applyTo(self, propulsor):
        cards = list(propulsor.cards.hand)
        if not cards:
            return
        index = propulsor.oracle.pick(cards, "Choisissez la carte à jouer (Accélération en col)")
        if index < 0 or index >= len(cards):
            index = 0
        chosen = cards[index]
        propulsor.cards.play(chosen)
        self.uncapped.bypass = True
        self.nextLabel = chosen
        self.remainingUses -= 1


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
