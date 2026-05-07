#! /usr/bin/env python3

from unittests import assert_equals, runTests
from jeu.riderInRace import RiderInRace
from jeu.drawOnePropulsor import DrawOnePropulsor
from jeu.riderMove import MovementRules
from jeu.track import Track
from jeu.race import Race, TeamInRace
from jeu.teamBuilder import TeamBuilder
from jeu.propulsion import SimpleTeamPropulsion
from jeu.riderBuilder import RiderBuilder


class EffortLong:
    def applyTo(self, personnage):
        personnage.energyRules = BetterFatigue(personnage.energyRules, 3)


class BetterFatigue:
    def __init__(self, base, fatigueValue):
        self.base = base
        self.fatigueValue = fatigueValue

    def energyFromCard(self, card):
        if card == "f":
            return self.fatigueValue
        return self.base.energyFromCard(card)


class EffortLongTest:
    def testEffortLong(self):
        track = Track([(5, "normal"), (3, "end")])
        rb = RiderBuilder()
        rb.buildPropulsor(DrawOnePropulsor(["f"]))
        personnage = rb.getResult()
        tb = TeamBuilder()
        tb.addRider(personnage)
        tb.buildPropulsion(SimpleTeamPropulsion())
        team = tb.getResult()

        personnage.gainTalent(EffortLong())

        teamInRace = TeamInRace(team)
        teamInRace.placeNextRider(0, 0)
        race = Race(track, [teamInRace])
        race.newTurn()
        assert_equals(3, teamInRace.ridersInRace[0].position()[0])


if __name__ == "__main__":
    runTests(EffortLongTest())
