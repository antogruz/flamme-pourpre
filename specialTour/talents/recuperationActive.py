from jeu.race import RaceObserver

class RecuperationActive(RaceObserver):
    def applyTo(self, personnage):
        personnage.addRaceObserver(self)
        personnage.propulsor.cards.endOfRaceDecksManagers.append(self)
        self.personnage = personnage
        self.history = []

    def onRaceStart(self, track):
        self.track = track

    def onRiderMove(self, rider, start, end, obstacles, card):
        if rider.personnage is not self.personnage:
            return
        if self.track.getRoadType(start[0]) == "refuel":
            if end[0] - start[0] <= 4:
                self.incrementCard(rider.personnage.propulsor)
        if self.track.getRoadType(start[0]) == "descent":
            if end[0] - start[0] <= 5:
                self.incrementCard(rider.personnage.propulsor)

    def incrementCard(self, propulsor):
        eligibleCards = [c for c in propulsor.cards.lastDiscarded if c != "f"]
        if not eligibleCards:
            return
        choice = propulsor.oracle.pick(eligibleCards, "Choose a card to increment")
        card = eligibleCards[choice]
        replaceCard(propulsor.cards.discard, card, card + 1)
        self.history.append((card, card + 1))

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