from race import RaceObserver

class Endurance(RaceObserver):
    def __init__(self):
        self.fatiguesCount = 0

    def displayRule(self):
        return "Endurance à la fatigue: Quête. Jouer des cartes fatigue. Entre 2 courses, enlevez du deck autant de carte fatigue que le total des cartes fatigue jouées"

    def applyTo(self, personnage):
        personnage.propulsor.cards.endOfRaceDecksManagers.append(self)
        personnage.addRaceObserver(self)

    def modifyCards(self, cards):
        removeExhausts(cards.deck, self.fatiguesCount)
    
    def onRiderMove(self, rider, start, end, obstacles, card):
        if card == "f":
            self.fatiguesCount += 1

def removeExhausts(deck, count):
    for i in range(count):
        if "f" in deck:
            deck.remove("f")
