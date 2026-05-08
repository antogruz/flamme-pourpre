from unittests import assert_equals, runTests
from jeu.cards import noop
from jeu.riderBuilder import RiderBuilder
from jeu.track import Track
from jeu.race import Race, TeamInRace
from jeu.teamBuilder import TeamBuilder
from jeu.propulsion import SimpleTeamPropulsion
from endurance import Endurance

class TestTalentsEndOfRace:
    def testEnduranceRemovesFatiguesFromDeck(self):
        personnage = createPersonnage(2, ["f"])
        race = prepareRace(2, personnage, Endurance())
        race.newTurn()
        personnage.propulsor.newRace()

        assert_equals(0, personnage.propulsor.cards.deck.count("f"))

    def testEnduranceRemovesOneFatigueFromDeck(self):
        personnage = createPersonnage(3, ["f"])
        race = prepareRace(2, personnage, Endurance())
        race.newTurn()
        personnage.propulsor.newRace()

        assert_equals(1, personnage.propulsor.cards.deck.count("f"))

    def testEnduranceWithoutPlayingFatigues(self):
        personnage = createPersonnage(2, [2])
        race = prepareRace(2, personnage, Endurance())
        race.newTurn()
        personnage.propulsor.newRace()

        assert_equals(2, personnage.propulsor.cards.deck.count("f"))
    
    def testEnduranceCumulatesBetweenRaces(self):
        personnage = createPersonnage(5, ["f", "f"])
        race = prepareRace(2, personnage, Endurance())
        race.newTurn()
        personnage.propulsor.newRace()
        otherRace = prepareRace(2, personnage, None)
        otherRace.newTurn()
        personnage.propulsor.newRace()

        assert_equals(0, personnage.propulsor.cards.deck.count("f"))

    def testEnduranceRemovesTooManyFatiguesFromDeck(self):
        personnage = createPersonnage(1, ["f"])
        race = prepareRace(2, personnage, Endurance())
        race.newTurn()
        personnage.propulsor.newRace()
        assert_equals(0, personnage.propulsor.cards.deck.count("f"))

def createPersonnage(fatiguesCount, cardsToPlay):
    rb = RiderBuilder()
    rb.buildOracle(CardsPicker(cardsToPlay))
    rb.buildDeck([1, 2] + ["f"] * fatiguesCount, shuffle=noop)
    return rb.getResult()

def prepareRace(trackSize, personnage, talent):
    track = Track([(trackSize, "normal"), (10, "end")])
    tb = TeamBuilder()
    tb.addRider(personnage)
    tb.buildPropulsion(SimpleTeamPropulsion())
    team = tb.getResult()

    if talent:
        personnage.gainTalent(talent)

    teamInRace = TeamInRace(team)
    teamInRace.placeNextRider(0, 0)
    race = Race(track, [teamInRace])
    return race

class CardsPicker:
    def __init__(self, cardsToPlay):
        self.cardsToPlay = cardsToPlay

    def pick(self, possibilities, *_):
        choice = self.cardsToPlay.pop(0)
        return possibilities.index(choice)

if __name__ == "__main__":
    runTests(TestTalentsEndOfRace())