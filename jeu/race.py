#!/usr/bin/env python3

# Cette classe respecte la procédure du jeu flamme rouge pour une course entière, jusqu'à ce que tous les coureurs soient arrivés.
# Elle donne le classement de la course. Ce n'est pas sa responsabilité de connaître les règles (de mouvement, d'aspiration, de fatigue...) mais elle connait la procédure.
# Elle sera amenée à changer si de nouvelles étapes sont décrites dans la procédure, par exemple la phase d'enchères du mode de jeu "échappée" ou l'activation de pouvoirs uniques avant de révéler les cartes, etc.

from obstacles import Obstacles
from slipstreaming import slipstreaming
from exhaust import exhaust

class Race():
    def __init__(self, track, riders, players):
        self.observers = []
        self.track = track
        self.riders = riders
        self.obstacles = Obstacles(riders)
        self.players = players
        self.arrivals = []
        self.checkArrivals()

    def addObserver(self, observer):
        self.observers.append(observer)

    def isOver(self):
        return not self.riders

    def newTurn(self):
        for p in self.players:
            p.pickNextMoves()

        for r in headToTail(self.riders):
            start = r.position()
            r.move(self.track, self.obstacles)
            for observer in self.observers:
                observer.onRiderMove(r, start, r.position(), self.obstacles)

        slipstreaming(self.riders, self.track, self.observers)
        self.checkArrivals()

        exhaust(headToTail(self.riders), self.observers)
        for observer in self.observers:
            observer.onTurnEnd()

    def ranking(self):
        return self.arrivals

    def checkArrivals(self):
        for r in headToTail(self.riders):
            if arrived(r, self.track):
                self.riders.remove(r)
                self.arrivals.append(r)
                self.removeFromPlayers(r)

    def removeFromPlayers(self, rider):
        for p in self.players:
            if rider in p.riders:
                p.riders.remove(rider)


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

from unittests import runTests, assert_equals, assert_similars
from track import Track
from rider import Rider
from cards import Cards
from positions import headToTail
import riderMove

class RaceTest():
    def __before__(self):
        self.track = Track([(5, "normal"), (3, "end")])

    def createRace(self, riders):
        return Race(self.track, riders, [SimplePlayer(copy(riders), 2)])

    def testCreateRace(self):
        riders = [createRider(0, 0)]
        race = self.createRace(riders)
        assert_equals(False, race.isOver())
        assert_similars([], race.ranking())

    def testRaceOver(self):
        race = self.createRace([])
        assert_equals(True, race.isOver())

    def testRaceIsOverIfAllRidersHavePassedLine(self):
        race = self.createRace([createRider(5, 0)])
        assert_equals(True, race.isOver())

    def testRiderMovesAfterATurn(self):
        rider = createRider(0, 0)
        race = self.createRace([rider])
        race.newTurn()
        assert_equals(2, rider.position()[0])

    def testArrival(self):
        rider = createRider(4, 0)
        race = self.createRace([rider, createRider(0, 0)])
        race.newTurn()
        assert_similars([rider], race.ranking())

    def testDontPlayForArrivedRiders(self):
        rider = createRider(5, 0)
        race = self.createRace([rider])
        race.newTurn()
        assert_equals((5, 0), rider.position())

    def testRanking(self):
        first = createRider(5, 0)
        second = createRider(4, 0)
        third = createRider(3, 0)
        fourth = createRider(0, 0)
        race = self.createRace([fourth, second, third, first])
        while not race.isOver():
            race.newTurn()
        assert_equals([first, second, third, fourth], race.ranking())


def copy(list):
    return [l for l in list]

def createRider(square, lane):
    rider = Rider(Cards([]))
    rider.riderMove = riderMove.Rider(square, lane)
    return rider

class SimplePlayer():
    def __init__(self, riders, move):
        self.riders = riders
        self.move = move

    def pickNextMoves(self):
        for r in self.riders:
            r.nextMove = self.move


if __name__ == "__main__":
    runTests(RaceTest())
