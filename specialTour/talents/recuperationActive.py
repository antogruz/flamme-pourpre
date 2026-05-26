from jeu.race import RaceObserver
from jeu.talent import Talent
from jeu.cards import SimpleCard

class RecuperationActive(Talent, RaceObserver):
    def displayRule(self):
        return "Récupération active: si on avance du minimum en ravitaillement ou en descente, on peut augmenter de 1 une carte de sa main. (pour la course en cours)"

    def applyTo(self, personnage):
        personnage.addRaceObserver(self)
        personnage.propulsor.cards.endOfRaceDecksManagers.append(self)
        self.personnage = personnage
        self.history = []

    def onRaceStart(self, track):
        self.track = track

    def onRiderMove(self, rider, start, end, obstacles, move):
        if rider.personnage is not self.personnage:
            return
        if self.track.getRoadType(start[0]) == "refuel":
            if end[0] - start[0] <= 4:
                self.incrementCard(rider.personnage.propulsor)
        if self.track.getRoadType(start[0]) == "descent":
            if end[0] - start[0] <= 5:
                self.incrementCard(rider.personnage.propulsor)

    def incrementCard(self, propulsor):
        eligibleCards = [c for c in propulsor.cards.lastDiscarded if c.label() != "f"]
        if not eligibleCards:
            return
        choice = propulsor.oracle.pick([c.label() for c in eligibleCards], "Choose a card to increment")
        card = eligibleCards[choice]
        incremented = SimpleCard(card.energy() + 1)
        replaceCard(propulsor.cards.discard, card, incremented)
        self.history.append((card, incremented))

    def modifyCards(self, cards):
        for card, incrementedCard in self.history:
            for list in [cards.played, cards.deck]:
                if incrementedCard in list:
                    list.remove(incrementedCard)
                    list.append(card)
                    break
        self.history = []

def replaceCard(list, before, after):
    list.remove(before)
    list.append(after)