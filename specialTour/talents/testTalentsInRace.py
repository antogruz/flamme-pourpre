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
from imblocableClimber import ImblocableClimber
from accelerationEnCol import AccelerationEnCol
from boost import Boost


def labels(cards):
    return [c.label() for c in cards]

def energies(cards):
    return [c.energy() for c in cards]


class TalentsInRaceTest():
    def __before__(self):
        self.track = Track([(30, "normal")])
        self.preparedTeams = [[], []]
        self.teamsInRace = []

    def createHero(self, cards, talent, position = (0, 0)):
        rb = RiderBuilder()
        rb.buildPropulsor(DrawOnePropulsor(cards, shuffle=noop))
        self.hero = rb.getResult()
        self.hero.gainTalent(talent)
        self.hero.position = position
        self.preparedTeams[0].append(self.hero)

    def createDeckHero(self, deck, pickedIndex, talent, position = (0, 0)):
        rb = RiderBuilder()
        self.oracle = ChoiceDoer(pickedIndex)
        rb.buildOracle(self.oracle)
        rb.buildDeck(deck, shuffle=noop)
        self.hero = rb.getResult()
        self.hero.gainTalent(talent)
        self.hero.position = position
        self.preparedTeams[0].append(self.hero)

    def getMainRider(self):
        return self.teamsInRace[0].ridersInRace[0]

    def addMinion(self, position, move = 2, team = 0):
        self.addPersonnage(self.preparedTeams[team], position, move)

    def addPersonnage(self, list, position, move = 2):
        rb = RiderBuilder()
        rb.buildPropulsor(DrawOnePropulsor([move] * 10))
        personnage = rb.getResult()
        personnage.position = position
        list.append(personnage)

    def createRace(self):
        for team in self.preparedTeams:
            tb = TeamBuilder()
            for rider in team:
                tb.addRider(rider)
            tb.buildPropulsion(SimpleTeamPropulsion())
            teamInRace = TeamInRace(tb.getResult())
            self.teamsInRace.append(teamInRace)
            for rider in team:
                teamInRace.placeNextRider(rider.position[0], rider.position[1])
        self.race = Race(self.track, self.teamsInRace)

    def testEffortLong(self):
        self.createHero(["f"], EffortLong())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.getMainRider().square)

    def testEconomieEnergieSkipsHand(self):
        self.createDeckHero([5], 1, EconomieEnergie())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.getMainRider().square)

    def testEconomieEnergieSkipsOnEmptyDeck(self):
        self.createDeckHero([], 0, EconomieEnergie())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.getMainRider().square)

    def testPoursuivantBonusWhenNotInLeadingGroup(self):
        self.createHero([2], Poursuivant())
        self.addMinion((10, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.getMainRider().square)

    def testPoursuivantNoBonusWhenInLeadingGroup(self):
        self.createHero([2], Poursuivant())
        self.addMinion((1, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(2, self.getMainRider().square)

    def testEchappeBonusWhenAloneInFront(self):
        self.createHero([2], Echappe(), (10, 0))
        self.addMinion((0, 0))
        self.addMinion((1, 0))
        self.addMinion((2, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(13, self.getMainRider().square)

    def testEchappeNoBonusWhenLeadingGroupIsHalfOrMore(self):
        self.createHero([2], Echappe(), (10, 0))
        self.addMinion((9, 0))
        self.addMinion((0, 0))
        self.addMinion((1, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(12, self.getMainRider().square)

    def testEffortLongAndPoursuivantStack(self):
        self.createHero(["f"], EffortLong())
        self.hero.gainTalent(Poursuivant())
        self.addMinion((10, 0))
        self.createRace()
        self.race.newTurn()
        assert_equals(4, self.getMainRider().square)

    def testSeFaufilerSimple(self):
        self.createHero([3], SeFaufiler())
        self.addMinion((1, 0), 2)
        self.addMinion((1, 1), 2)
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.getMainRider().square)

    def testSeFaufilerWithSeveralGroups(self):
        self.createHero([9], SeFaufiler())
        self.addMinion((7, 0), 2)
        self.addMinion((7, 1), 2)
        self.createRace()
        self.race.newTurn()
        assert_equals(8, self.getMainRider().square)

    def testSprintFinalWith3CardsLeft(self):
        self.createDeckHero([3, 3, 3], 1, SprintFinal())
        self.createRace()
        self.race.newTurn()
        assert_equals(5, self.getMainRider().square)

    def testSprintFinalWith4CardsLeft(self):
        self.createDeckHero([3, 3, 3, 3], 1, SprintFinal())
        self.createRace()
        self.race.newTurn()
        assert_equals(4, self.getMainRider().square)

    def testSprintFinalWith8CardsLeft(self):
        self.createDeckHero([3, 3, 3, 3, 3, 3, 3, 3], 1, SprintFinal())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.getMainRider().square)

    def testSuperSprintIncreasesNines(self):
        self.createHero([9], SuperSprint())
        self.createRace()
        self.race.newTurn()
        assert_equals(11, self.getMainRider().square)

    def testSuperSprintDoesNotIncreaseOtherCards(self):
        self.createHero([3], SuperSprint())
        self.createRace()
        self.race.newTurn()
        assert_equals(3, self.getMainRider().square)

    def prepareRecuperationActive(self, roadType, cards):
        self.track = Track([(30, roadType)])
        self.createDeckHero(cards, 0, RecuperationActive())
        self.createRace()
        self.race.newTurn()

    def testRecuperationActiveIncreasesACard(self):
        self.prepareRecuperationActive("refuel", [2, 3])
        assert_contains(4, energies(self.getMainRider().personnage.propulsor.cards.discard))

    def testRecuperationActiveDoesNothingOnStandardRoad(self):
        self.prepareRecuperationActive("normal", [2, 3])
        assert_contains(3, energies(self.getMainRider().personnage.propulsor.cards.discard))

    def testRecuperationActiveDoesNothingIfRiderGoesTooFast(self):
        self.prepareRecuperationActive("refuel", [7, 3])
        assert_contains(3, energies(self.getMainRider().personnage.propulsor.cards.discard))

    def testRecuperationActiveOnDescent(self):
        self.prepareRecuperationActive("descent", [4, 4])
        assert_contains(5, energies(self.getMainRider().personnage.propulsor.cards.discard))

    def testRecuperationActiveAllowsPlayerToChooseWhichCardToIncrement(self):
        self.track = Track([(30, "refuel")])
        self.createDeckHero([2, 3, 4, 5], 1, RecuperationActive())
        self.createRace()
        self.race.newTurn()
        assert_similars(["2", "5", "5", "f"], labels(self.getMainRider().personnage.propulsor.cards.discard))
        assert_similars(["2", "4", "5"], self.oracle.choices[1])

    def testRecuperationActiveOnlyAllowToIncrementCardsJustDiscarded(self):
        self.track = Track([(30, "refuel")])
        self.createDeckHero([2, 2, 2, 2, 2, 3, 4, 5], 1, RecuperationActive())
        self.createRace()
        self.race.newTurn()
        self.race.newTurn()
        assert_similars(["2", "4", "5"], self.oracle.choices[3])

    def testRecuperationActiveCannotIncrementExhaustCards(self):
        self.prepareRecuperationActive("refuel", [2, "f", "f"])
        assert_similars(["f", "f", "f"], labels(self.getMainRider().personnage.propulsor.cards.discard))

    def testCardsAreResetAfterRace(self):
        self.prepareRecuperationActive("refuel", [2, 3])
        self.getMainRider().personnage.propulsor.newRace()
        assert_contains(3, energies(self.getMainRider().personnage.propulsor.cards.deck))

    def testCardsAreNotResetAgainAfterEachRace(self):
        self.prepareRecuperationActive("refuel", [2, 3, 4])
        self.getMainRider().personnage.propulsor.newRace()
        self.getMainRider().personnage.propulsor.newRace()
        assert_contains(4, energies(self.getMainRider().personnage.propulsor.cards.deck))

    def testRecuperationActiveOnBiggerHandSize(self):
        self.track = Track([(30, "refuel")])
        self.createDeckHero([2, 3, 4, 5, 6], 1, RecuperationActive())
        self.hero.propulsor.cards.handSize = 5
        self.createRace()
        self.race.newTurn()
        assert_similars(["2", "4", "5", "6"], self.oracle.choices[1])

    def testRecuperationActiveCanResetPlayedCards(self):
        self.prepareRecuperationActive("refuel", [2, 3])
        self.race.newTurn()
        self.getMainRider().personnage.propulsor.newRace()
        assert_contains(3, energies(self.getMainRider().personnage.propulsor.cards.deck))

    def testImblocableClimber(self):
        self.track = Track([(30, "ascent")])
        self.createHero([5], ImblocableClimber())
        self.addMinion((3, 0))
        self.addMinion((3, 1))
        self.createRace()
        self.race.newTurn()
        assert_equals(5, self.getMainRider().square)

    def testImblocableClimberOnNormalRoad(self):
        self.track = Track([(30, "normal")])
        self.createHero([5], ImblocableClimber())
        self.addMinion((3, 0))
        self.addMinion((3, 1))
        self.createRace()
        self.race.newTurn()
        assert_equals(4, self.getMainRider().square)

    def testImblocableClimberBlocksOtherRiders(self):
        self.track = Track([(30, "ascent")])
        self.createHero([5], ImblocableClimber())
        self.addMinion((3, 0), team = 1)
        self.addMinion((3, 1), team = 1)
        self.createRace()
        self.race.newTurn()
        assert_equals(5, self.getMainRider().square)
        assert_equals(4, self.teamsInRace[1].ridersInRace[0].square)
        assert_equals(4, self.teamsInRace[1].ridersInRace[1].square)

    def testImblocableClimberLetAlliesPass(self):
        self.track = Track([(30, "ascent")])
        self.createHero([5], ImblocableClimber())
        self.addMinion((3, 0), team = 0)
        self.createRace()
        self.race.newTurn()
        assert_equals(5, self.getMainRider().square)
        assert_equals(5, self.teamsInRace[0].ridersInRace[1].square)

    def testImblocableBlocksInTheSameCaseAsItGetsPriority(self):
        self.track = Track([(4, "ascent"), (4, "descent")])
        self.createHero([5], ImblocableClimber())
        self.addMinion((3, 0), team = 1)
        self.createRace()
        self.race.newTurn()
        assert_equals(5, self.getMainRider().square)
        assert_equals(4, self.teamsInRace[1].ridersInRace[0].square)

    def testAccelerationEnCol(self):
        self.track = Track([(30, "ascent")])
        self.createDeckHero([6] * 20, 4, AccelerationEnCol())
        self.createRace()
        self.race.newTurn()
        assert_equals(6, self.getMainRider().square)
        self.race.newTurn()
        assert_equals(11, self.getMainRider().square)
        self.getMainRider().personnage.propulsor.newRace()
        self.race.newTurn()
        assert_equals(17, self.getMainRider().square)

    def testBoost(self):
        self.createDeckHero([5] * 20, 4, Boost(bonus=2, uses=1))
        self.createRace()
        self.race.newTurn()
        assert_equals(7, self.getMainRider().square)
        self.race.newTurn()
        assert_equals(12, self.getMainRider().square)
        self.getMainRider().personnage.propulsor.newRace()
        self.race.newTurn()
        assert_equals(19, self.getMainRider().square)

    def testBoostOnFatigueCard(self):
        self.createDeckHero(["f"] * 20, 4, Boost(bonus=2, uses=1))
        self.createRace()
        self.race.newTurn()
        assert_equals(4, self.getMainRider().square)


class ChoiceDoer:
    def __init__(self, value):
        self.value = value
        self.choices = []

    def pick(self, possibilities, *_):
        self.choices.append(possibilities)
        return self.value

if __name__ == "__main__":
    runTests(TalentsInRaceTest())
