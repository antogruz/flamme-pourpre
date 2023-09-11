#!/usr/bin/env python3

from positions import headToTail

class MiniraceObserver:
    def __init__(self, lastSquare, prizeGiver):
        self.lastSquare = lastSquare
        self.prizeGiver = prizeGiver
        self.ridersThatCrossedThisTurn = []

    def logMove(self, rider, start, end, *_):
        if self.prizeGiver.finished():
            return
        if start[0] <= self.lastSquare and end[0] > self.lastSquare:
            self.saveRider(rider)

    def saveRider(self, rider):
        self.ridersThatCrossedThisTurn.append(rider)

    def endTurn(self):
        for rider in headToTail(self.ridersThatCrossedThisTurn):
            if self.prizeGiver.finished():
                break
            self.prizeGiver.reward(rider)
        self.ridersThatCrossedThisTurn = []

    def logGroup(*_):
        #TODO group can cross a point by slipstream
        pass

    def logExhaust(*_):
        pass



