from jeu.race import RaceObserver
from jeu.talent import Talent

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

    def onRiderMove(self, rider, start, end, obstacles, moves):
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
        self.history.append((card, card.energy()))
        card.setEnergy(card.energy() + 1)

    def modifyCards(self, cards):
        for card, originalEnergy in self.history:
            card.setEnergy(originalEnergy)
        self.history = []