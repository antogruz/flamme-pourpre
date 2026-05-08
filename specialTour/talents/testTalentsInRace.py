#!/usr/bin/env python3

from unittests import assert_equals, runTests
from jeu.cards import noop
from jeu.drawOnePropulsor import DrawOnePropulsor
from jeu.riderBuilder import RiderBuilder
from jeu.track import Track
from jeu.race import Race, TeamInRace
from jeu.teamBuilder import TeamBuilder
from jeu.propulsion import SimpleTeamPropulsion

from effortLong import EffortLong
from economieEnergie import EconomieEnergie


class TalentsInRaceTest:
    def testEffortLong(self):
        rb = RiderBuilder()
        rb.buildPropulsor(DrawOnePropulsor(["f"]))
        rider = self.runOneTurn(rb.getResult(), EffortLong())
        assert_equals(3, rider.position()[0])

    def testEconomieEnergieSkipsHand(self):
        rider = self.runOneTurn(self.makeDeckRider(deck=[5], pickedIndex=1), EconomieEnergie())
        assert_equals(3, rider.position()[0])

    def testEconomieEnergieSkipsOnEmptyDeck(self):
        rider = self.runOneTurn(self.makeDeckRider(deck=[], pickedIndex=0), EconomieEnergie())
        assert_equals(3, rider.position()[0])

    def makeDeckRider(self, deck, pickedIndex):
        rb = RiderBuilder()
        rb.buildOracle(ChoiceDoer(pickedIndex))
        rb.buildDeck(deck, shuffle=noop)
        return rb.getResult()

    def runOneTurn(self, personnage, talent, track = None):
        track = track or Track([(5, "normal"), (3, "end")])
        tb = TeamBuilder()
        tb.addRider(personnage)
        tb.buildPropulsion(SimpleTeamPropulsion())
        team = tb.getResult()

        personnage.gainTalent(talent)

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
    runTests(TalentsInRaceTest())
