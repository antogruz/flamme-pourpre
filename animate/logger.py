#!/usr/bin/env python3

from unittests import runTests, assert_equals, assert_similars
from obstacles import Obstacles
# Cette classe choisit les informations qui doivent être retenues quand un coureur joue une carte et se déplace, un groupe est aspiré, ou les coureurs sont fatigués.
# Le logger change si quelqu'un a besoin de connaître une information interne sur les évènements qui se sont produits pendant un tour de jeu (phase de résolution), et qui ne sont plus disponibles à la fin du tour (chemin précis parcouru par un coureur, carte qu'il a jouée à ce tour...).

class LoggerTest:
    def testCardPlayed(self):
        logger = Logger()
        rider = Rider()
        CardDecorator().cardPlayed(rider, 3)
        logger.logMove(rider, (0, 0), (1, 0), Obstacles([]))
        assert_equals(3, logger.getMoves()[0][1])

class Rider:
    pass
from path import findPath

class Logger:
    def __init__(self):
        self.moves = []
        self.groups = []
        self.exhausted = []

    def logMove(self, rider, start, end, obstacles):
        path = findPath(obstacles, start, end)
        try:
            card = rider.logCardPlayed
        except:
            card = ""
        self.moves.append((rider, card, path))

    def logGroup(self, riders):
        self.groups.append([(rider, rider.position()) for rider in riders])

    def logExhaust(self, rider):
        self.exhausted.append(rider)

    def getMoves(self):
        return self.moves

    def getGroups(self):
        return self.groups

    def getExhausted(self):
        return self.exhausted

    def endTurn(self):
        pass

class CardDecorator:
    def cardPlayed(self, rider, card):
        rider.logCardPlayed = card

if __name__ == "__main__":
    runTests(LoggerTest())
