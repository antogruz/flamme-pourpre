#!/usr/bin/env python3

# Cette classe respecte la procédure du jeu flamme rouge pour une course entière, jusqu'à ce que tous les coureurs soient arrivés.
# Elle donne le classement de la course. Ce n'est pas sa responsabilité de connaître les règles (de mouvement, d'aspiration, de fatigue...) mais elle connait la procédure.
# Elle sera amenée à changer si de nouvelles étapes sont décrites dans la procédure, par exemple la phase d'enchères du mode de jeu "échappée" ou l'activation de pouvoirs uniques avant de révéler les cartes, etc.

from obstacles import Obstacles
from slipstreaming import slipstreaming
from exhaust import exhaust
from raceSnapshot import RaceSnapshot

class Race():
    def __init__(self, track, teamsInRace):
        self.observers = []
        self.track = track
        self.teamsInRace = teamsInRace
        self.riders = [r for team in teamsInRace for r in team.ridersInRace]
        self.obstacles = Obstacles(self.riders)
        self.arrivals = []
        self.checkArrivals()
        for rider in self.riders:
            for observer in rider.personnage.raceObservers:
                self.addObserver(observer)
        for observer in self.observers:
            observer.onRaceStart(self.track)

    def addObserver(self, observer):
        self.observers.append(observer)

    def isOver(self):
        return not self.riders

    def newTurn(self):
        moves = {}
        for team in self.teamsInRace:
            moves.update(team.pickNextMoves())
        snapshot = RaceSnapshot(list(self.riders))
        energies = { r: energyOf(r, moves[r], snapshot) for r in self.riders }

        for r in playOrder(self.riders, snapshot):
            start = r.position()
            r.move(energies[r], self.track, self.obstacles)
            for observer in self.observers:
                observer.onRiderMove(r, start, r.position(), self.obstacles, moves[r])

        slipstreaming(self.riders, self.track, self.observers, self.obstacles)
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

def energyOf(rider, card, snapshot):
    base = rider.personnage.energyRules.energyFromCard(card)
    bonus = sum(rule.bonusFor(card, rider, snapshot) for rule in rider.personnage.bonusRules)
    return base + bonus

class RaceObserver:
    """Interface for observing race events.
    
    Implement this interface to receive notifications about race events
    such as rider movements, slipstreaming, exhaustion, and turn endings.
    """
    def onRaceStart(self, track):
        """Called when the race starts."""
        pass

    def onRiderMove(self, rider, start, end, obstacles, card):
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
        return self.ridersInRace[-1]

    def pickNextMoves(self):
        return self.team.propulsor.pickNextMoves(self.getActiveRiders())

    def getActiveRiders(self):
        return [r for r in self.ridersInRace if not r.arrived]

from unittests import runTests, assert_equals, assert_similars
from track import Track
from positions import headToTail, playOrder
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
            tb.addRider(createRider())
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
        champion = self.team.placeNextRider(4, 0)
        self.team.placeNextRider(0, 0)
        race = self.createRace()
        race.newTurn()
        assert_similars([champion], race.ranking())

    def testDontPlayForArrivedRiders(self):
        self.createTeam(1)
        rider = self.team.placeNextRider(5, 0)
        race = self.createRace()
        race.newTurn()
        assert_equals((5, 0), rider.position())

    def testRanking(self):
        self.createTeam(4)
        a = self.team.placeNextRider(5, 0)
        b = self.team.placeNextRider(4, 0)
        c = self.team.placeNextRider(3, 0)
        d = self.team.placeNextRider(0, 0)
        race = self.createRace()
        while not race.isOver():
            race.newTurn()
        assert_equals([a, b, c, d], race.ranking())

from riderBuilder import RiderBuilder
def createRider():
    rb = RiderBuilder()
    rb.buildPropulsor(SimplePropulsor(2))
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
