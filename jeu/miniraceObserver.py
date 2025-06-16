#!/usr/bin/env python3

from positions import headToTail
from race import RaceObserver

class MiniraceObserver(RaceObserver):
    def __init__(self, lastSquare, prizeGiver):
        self.lastSquare = lastSquare
        self.prizeGiver = prizeGiver
        self.ridersThatCrossedThisTurn = []

    def onRiderMove(self, rider, start, end, *_):
        if self.prizeGiver.finished():
            return
        if start[0] <= self.lastSquare and end[0] > self.lastSquare:
            self.saveRider(rider)

    def saveRider(self, rider):
        self.ridersThatCrossedThisTurn.append(rider)

    def onTurnEnd(self):
        for rider in headToTail(self.ridersThatCrossedThisTurn):
            if self.prizeGiver.finished():
                break
            self.prizeGiver.reward(rider)
        self.ridersThatCrossedThisTurn = []

    def onSlipstream(*_):
        #TODO group can cross a point by slipstream
        pass

    def onExhaustion(*_):
        pass



