#!/usr/bin/env python3

# Cette classe respecte la procédure du jeu flamme rouge pour une course entière, jusqu'à ce que tous les coureurs soient arrivés.
# Elle donne le classement de la course. Ce n'est pas sa responsabilité de connaître les règles (de mouvement, d'aspiration, de fatigue...) mais elle connait la procédure.
# Elle sera amenée à changer si de nouvelles étapes sont décrites dans la procédure, par exemple la phase d'enchères du mode de jeu "échappée" ou l'activation de pouvoirs uniques avant de révéler les cartes, etc.

from obstacles import Obstacles
from slipstreaming import slipstreaming
from exhaust import exhaust

class Race():
    def __init__(self, track, teamsInRace):
        self.observers = []
        self.track = track
        self.teamsInRace = teamsInRace
        self.riders = [r for team in teamsInRace for r in team.ridersInRace]
        self.obstacles = Obstacles(self.riders)
        self.arrivals = []
        self.checkArrivals()

    def addObserver(self, observer):
        self.observers.append(observer)

    def isOver(self):
        return not self.riders

    def newTurn(self):
        for team in self.teamsInRace:
            team.pickNextMoves()

        for r in headToTail(self.riders):
            start = r.position()
            r.move(r.nextMove, self.track, self.obstacles)
            for observer in self.observers:
                observer.onRiderMove(r, start, r.position(), self.obstacles)

        slipstreaming(self.riders, self.track, self.observers)
        self.checkArrivals()

        exhaust(headToTail(self.riders), self.observers)
        for observer in self.observers:
            observer.onTurnEnd()

    def ranking(self):
        return list(self.arrivals)

    def checkArrivals(self):
        for r in headToTail(self.riders):
            if arrived(r, self.track):
                self.riders.remove(r)
                self.arrivals.append(r)
                r.setArrived()

def arrived(rider, track):
    return track.getRoadType(rider.getSquare()) == "end"

class RaceObserver:
    """Interface for observing race events.
    
    Implement this interface to receive notifications about race events
    such as rider movements, slipstreaming, exhaustion, and turn endings.
    """

    def onRiderMove(self, rider, start, end, obstacles):
        """Called when a rider moves from start to end position."""
        pass
    
    def onSlipstream(self, riders):
        """Called when riders benefit from slipstream."""
        pass
    
    def onExhaustion(self, riders):
        """Called when riders get exhausted.  """
        pass
    
    def onTurnEnd(self):
        """Called at the end of each turn."""
        pass

class TeamInRace:
    def __init__(self, team):
        self.team = team
        self.ridersToPlace = list(team.riders)
        self.ridersInRace = []

    def placeNextRider(self, square, lane):
        if not self.ridersToPlace:
            return False
        self.ridersInRace.append(RiderInRace(self.ridersToPlace.pop(0), square, lane))
        return True

    def pickNextMoves(self):
        self.team.propulsor.pickNextMoves(self.getActiveRiders())

    def getActiveRiders(self):
        return [r for r in self.ridersInRace if not r.arrived]

from unittests import runTests, assert_equals, assert_similars
from track import Track
from positions import headToTail
from riderMove import MovementRules
from riderInRace import RiderInRace
from team import Team
from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion

class RaceTest():
    def __before__(self):
        self.track = Track([(5, "normal"), (3, "end")])

    def createTeam(self, ridersCount):
        tb = TeamBuilder()
        for i in range(ridersCount):
            tb.addRider(createRider(str(i)))
        tb.buildColor("green")
        tb.buildPropulsion(SimpleTeamPropulsion())
        self.team = TeamInRace(tb.getResult())

    def createRace(self):
        return Race(self.track, [self.team])

    def testCreateRace(self):
        self.createTeam(1)
        self.team.placeNextRider(0, 0)
        race = self.createRace()
        assert_equals(False, race.isOver())
        assert_similars([], race.ranking())

    def testRaceOver(self):
        self.createTeam(0)
        race = self.createRace()
        assert_equals(True, race.isOver())

    def testRaceIsOverIfAllRidersHavePassedLine(self):
        self.createTeam(1)
        self.team.placeNextRider(5, 0)
        race = self.createRace()
        assert_equals(True, race.isOver())

    def testRiderMovesAfterATurn(self):
        self.createTeam(1)
        self.team.placeNextRider(0, 0)
        race = self.createRace()
        race.newTurn()
        assert_equals(2, self.team.ridersInRace[0].position()[0])

    def testArrival(self):
        self.createTeam(2)
        self.team.placeNextRider(4, 0)
        self.team.placeNextRider(0, 0)
        race = self.createRace()
        race.newTurn()
        assert_similars(["0"], [r.persistent.name for r in race.ranking()])

    def testDontPlayForArrivedRiders(self):
        self.createTeam(1)
        self.team.placeNextRider(5, 0)
        race = self.createRace()
        race.newTurn()
        assert_equals((5, 0), self.team.ridersInRace[0].position())

    def testRanking(self):
        self.createTeam(4)
        self.team.placeNextRider(5, 0)
        self.team.placeNextRider(4, 0)
        self.team.placeNextRider(3, 0)
        self.team.placeNextRider(0, 0)
        race = self.createRace()
        while not race.isOver():
            race.newTurn()
        assert_equals(["0", "1", "2", "3"], [r.persistent.name for r in race.ranking()])

from riderBuilder import RiderBuilder
def createRider(name):
    rb = RiderBuilder()
    rb.buildTexts("o/o", name)
    rb.buildPropulsor(SimplePropulsor(2))
    rb.buildMovementRules(MovementRules())
    return rb.getResult()

class SimplePropulsor():
    def __init__(self, move):
        self.move = move

    def generateMove(self):
        return self.move
    
    def exhaust(self):
        pass


if __name__ == "__main__":
    runTests(RaceTest())
