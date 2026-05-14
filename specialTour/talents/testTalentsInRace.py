#!/usr/bin/env python3

from unittests import assert_equals, assert_contains, assert_similars, runTests
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
from sprintFinal import SprintFinal
from superSprint import SuperSprint
from recuperationActive import RecuperationActive

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
        self.oracle = ChoiceDoer(pickedIndex)
        rb.buildOracle(self.oracle)
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

    def testSprintFinalWith3CardsLeft(self):
        self.createDeckHero([3, 3, 3], 1, SprintFinal())
        self.createRace()
        self.race.newTurn()
        assert_equals(5, self.mainRider.square)

    def testSprintFinalWith4CardsLeft(self):
        self.createDeckHero([3, 3, 3, 3], 1, SprintFinal())
        self.createRace()
        self.race.newTurn()
        assert_equals(4, self.mainRider.square)

    def testSprintFinalWith8CardsLeft(self):
        self.createDeckHero([3, 3, 3, 3, 3, 3, 3, 3], 1, SprintFinal())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.mainRider.square)

    def testSuperSprintIncreasesNines(self):
        self.createHero([9], SuperSprint())
        self.createRace()
        self.race.newTurn()
        assert_equals(11, self.mainRider.square)

    def testSuperSprintDoesNotIncreaseOtherCards(self):
        self.createHero([3], SuperSprint())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.mainRider.square)

    def prepareRecuperationActive(self, roadType, cards):
        self.track = Track([(30, roadType)])
        self.createDeckHero(cards, 0, RecuperationActive())
        self.createRace()
        self.race.newTurn()

    def testRecuperationActiveIncreasesACard(self):
        self.prepareRecuperationActive("refuel", [2, 3])
        assert_contains(4, self.mainRider.personnage.propulsor.cards.discard)

    def testRecuperationActiveDoesNothingOnStandardRoad(self):
        self.prepareRecuperationActive("normal", [2, 3])
        assert_contains(3, self.mainRider.personnage.propulsor.cards.discard)

    def testRecuperationActiveDoesNothingIfRiderGoesTooFast(self):
        self.prepareRecuperationActive("refuel", [7, 3])
        assert_contains(3, self.mainRider.personnage.propulsor.cards.discard)

    def testRecuperationActiveOnDescent(self):
        self.prepareRecuperationActive("descent", [4, 4])
        assert_contains(5, self.mainRider.personnage.propulsor.cards.discard)

    def testRecuperationActiveAllowsPlayerToChooseWhichCardToIncrement(self):
        self.track = Track([(30, "refuel")])
        self.createDeckHero([2, 3, 4, 5], 1, RecuperationActive())
        self.createRace()
        self.race.newTurn()
        assert_similars([2, 5, 5, "f"], self.mainRider.personnage.propulsor.cards.discard)
        assert_similars([2, 4, 5], self.oracle.choices[1])

    def testRecuperationActiveOnlyAllowToIncrementCardsJustDiscarded(self):
        self.track = Track([(30, "refuel")])
        self.createDeckHero([2, 2, 2, 2, 2, 3, 4, 5], 1, RecuperationActive())
        self.createRace()
        self.race.newTurn()
        self.race.newTurn()
        assert_similars([2, 4, 5], self.oracle.choices[3])

    def testRecuperationActiveCannotIncrementExhaustCards(self):
        self.prepareRecuperationActive("refuel", [2, "f", "f"])
        assert_similars(["f", "f", "f"], self.mainRider.personnage.propulsor.cards.discard)

    def testCardsAreResetAfterRace(self):
        self.prepareRecuperationActive("refuel", [2, 3])
        self.mainRider.personnage.propulsor.newRace()
        assert_contains(3, self.mainRider.personnage.propulsor.cards.deck)

    def testCardsAreNotResetAgainAfterEachRace(self):
        self.prepareRecuperationActive("refuel", [2, 3, 4])
        self.mainRider.personnage.propulsor.newRace()
        self.createRace()
        self.mainRider.personnage.propulsor.newRace()
        self.createRace()
        assert_contains(4, self.mainRider.personnage.propulsor.cards.deck)

    def testRecuperationActiveOnBiggerHandSize(self):
        self.track = Track([(30, "refuel")])
        self.createDeckHero([2, 3, 4, 5, 6], 1, RecuperationActive())
        self.hero.propulsor.cards.handSize = 5
        self.createRace()
        self.race.newTurn()
        assert_similars([2, 4, 5, 6], self.oracle.choices[1])


class ChoiceDoer:
    def __init__(self, value):
        self.value = value
        self.choices = []

    def pick(self, possibilities, *_):
        self.choices.append(possibilities)
        return self.value

if __name__ == "__main__":
    runTests(TalentsInRaceTest())
