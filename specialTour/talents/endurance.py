from race import RaceObserver
from talent import Talent
from jeu.cards import removeExhausts

class Endurance(Talent, RaceObserver):
    def __init__(self):
        self.fatiguesCount = 0

    def displayRule(self):
        return "Endurance à la fatigue: Quête. Jouer des cartes fatigue. Entre 2 courses, enlevez du deck autant de carte fatigue que le total des cartes fatigue jouées"

    def stats(self):
        return ["Fatigues jouées: " + str(self.fatiguesCount)]

    def applyTo(self, personnage):
        personnage.propulsor.cards.endOfRaceDecksManagers.append(self)
        personnage.addRaceObserver(self)
        self.personnage = personnage

    def modifyCards(self, cards):
        removeExhausts(cards.deck, self.fatiguesCount)

    def onRiderMove(self, rider, start, end, obstacles, moves):
        if rider.personnage is not self.personnage:
            return
        for move in moves:
            if move.label() == "f":
                self.fatiguesCount += 1

