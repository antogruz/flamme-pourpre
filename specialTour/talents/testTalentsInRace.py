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
from poursuivant import Poursuivant
from echappe import Echappe
from seFaufiler import SeFaufiler

class TalentsInRaceTest():
    def __before__(self):
        self.track = Track([(30, "normal")])
        self.minions = []

    def createHero(self, cards, talent, position = (0, 0)):
        rb = RiderBuilder()
        rb.buildPropulsor(DrawOnePropulsor(cards, shuffle=noop))
        self.hero = rb.getResult()
        self.hero.gainTalent(talent)
        self.heroPosition = position

    def createDeckHero(self, deck, pickedIndex, talent, position = (0, 0)):
        rb = RiderBuilder()
        rb.buildOracle(ChoiceDoer(pickedIndex))
        rb.buildDeck(deck, shuffle=noop)
        self.hero = rb.getResult()
        self.hero.gainTalent(talent)
        self.heroPosition = position

    def addMinion(self, position, move = 2):
        rb = RiderBuilder()
        rb.buildPropulsor(DrawOnePropulsor([move] * 10))
        minion = rb.getResult()
        minion.position = position
        self.minions.append(minion)

    def createRace(self):
        tb = TeamBuilder()
        tb.addRider(self.hero)
        for rider in self.minions:
            tb.addRider(rider)
        tb.buildPropulsion(SimpleTeamPropulsion())
        self.team = TeamInRace(tb.getResult())
        self.mainRider = self.team.placeNextRider(self.heroPosition[0], self.heroPosition[1])
        for minion in self.minions:
            self.team.placeNextRider(minion.position[0], minion.position[1])
        self.race = Race(self.track, [self.team])


    def testEffortLong(self):
        self.createHero(["f"], EffortLong())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.mainRider.square)

    def testEconomieEnergieSkipsHand(self):
        self.createDeckHero([5], 1, EconomieEnergie())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.mainRider.square)

    def testEconomieEnergieSkipsOnEmptyDeck(self):
        self.createDeckHero([], 0, EconomieEnergie())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.mainRider.square)

    def testPoursuivantBonusWhenNotInLeadingGroup(self):
        self.createHero([2], Poursuivant())
        self.addMinion((10, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.mainRider.square)

    def testPoursuivantNoBonusWhenInLeadingGroup(self):
        self.createHero([2], Poursuivant())
        self.addMinion((1, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(2, self.mainRider.square)

    def testEchappeBonusWhenAloneInFront(self):
        self.createHero([2], Echappe(), (10, 0))
        self.addMinion((0, 0))
        self.addMinion((1, 0))
        self.addMinion((2, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(13, self.mainRider.square)

    def testEchappeNoBonusWhenLeadingGroupIsHalfOrMore(self):
        self.createHero([2], Echappe(), (10, 0))
        self.addMinion((9, 0))
        self.addMinion((0, 0))
        self.addMinion((1, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(12, self.mainRider.square)

    def testEffortLongAndPoursuivantStack(self):
        self.createHero(["f"], EffortLong())
        self.hero.gainTalent(Poursuivant())
        self.addMinion((10, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(4, self.mainRider.square)

    def testSeFaufilerSimple(self):
        self.createHero([3], SeFaufiler())
        self.addMinion((1, 0), 2)
        self.addMinion((1, 1), 2)
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.mainRider.square)

    def testSeFaufilerWithSeveralGroups(self):
        self.createHero([9], SeFaufiler())
        self.addMinion((7, 0), 2)
        self.addMinion((7, 1), 2)
        self.createRace()
        self.race.newTurn()
        assert_equals(8, self.mainRider.square)

class ChoiceDoer:
    def __init__(self, value):
        self.value = value

    def pick(self, *_):
        return self.value


if __name__ == "__main__":
    runTests(TalentsInRaceTest())
