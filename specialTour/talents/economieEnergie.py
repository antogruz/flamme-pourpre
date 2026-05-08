#! /usr/bin/env python3

from unittests import assert_equals, runTests
from jeu.cards import noop
from jeu.track import Track
from jeu.race import Race, TeamInRace
from jeu.teamBuilder import TeamBuilder
from jeu.propulsion import SimpleTeamPropulsion
from jeu.riderBuilder import RiderBuilder
from jeu.riderMove import MovementRules
from jeu.deckPropulsor import DeckPropulsor


class EconomieEnergie:
    def applyTo(self, personnage):
        personnage.energyRules = BetterEmpty(personnage.energyRules, 3)
        personnage.propulsor = SkippableDeckPropulsor(
            personnage.propulsor.cards,
            personnage.propulsor.oracle,
        )


class BetterEmpty:
    def __init__(self, base, emptyValue):
        self.base = base
        self.emptyValue = emptyValue

    def energyFromCard(self, card):
        if card == "":
            return self.emptyValue
        return self.base.energyFromCard(card)


class SkippableDeckPropulsor(DeckPropulsor):
    def choicesFrom(self, cards):
        return list(cards) + [""]

    def applyCard(self, card):
        if card == "":
            self.cards.discardHand()
        else:
            self.cards.play(card)


class EconomieEnergieTest:
    def testSkipsHand(self):
        rider = self.runOneTurn(deck=[5], pickedIndex=1)
        assert_equals(3, rider.position()[0])

    def testSkipsOnEmptyDeck(self):
        rider = self.runOneTurn(deck=[], pickedIndex=0)
        assert_equals(3, rider.position()[0])

    def runOneTurn(self, deck, pickedIndex):
        track = Track([(5, "normal"), (3, "end")])
        rb = RiderBuilder()
        rb.buildOracle(ChoiceDoer(pickedIndex))
        rb.buildDeck(deck, shuffle=noop)
        rb.buildMovementRules(MovementRules())
        personnage = rb.getResult()
        tb = TeamBuilder()
        tb.addRider(personnage)
        tb.buildPropulsion(SimpleTeamPropulsion())
        team = tb.getResult()

        personnage.gainTalent(EconomieEnergie())

        teamInRace = TeamInRace(team)
        teamInRace.placeNextRider(0, 0)
        race = Race(track, [teamInRace])
        race.newTurn()
        return teamInRace.ridersInRace[0]


class ChoiceDoer:
    def __init__(self, value):
        self.value = value

    def pick(self, *_):
        return self.value


if __name__ == "__main__":
    runTests(EconomieEnergieTest())
