#!/usr/bin/env python3

class SequentialPropulsion():
    def __init__(self, oracle):
        self.oracle = oracle

    def pickNextMoves(self, riders):
        ridersToPick = list(riders)
        while (ridersToPick):
            self.pickOneMove(ridersToPick)

    def pickOneMove(self, riders):
        rider = self.pickRider(riders)
        rider.nextMove = rider.personnage.propulsor.generateMove()
        rider.logCardPlayed = rider.nextMove

    def pickRider(self, riders):
        choice = self.oracle.pickRider(riders, "Pick a rider")
        if choice < 0 or choice >= len(riders):
            choice = 0
        return riders.pop(choice)

class SimpleTeamPropulsion():
    def pickNextMoves(self, riders):
        for r in riders:
            r.nextMove = r.personnage.propulsor.generateMove()
            r.logCardPlayed = r.nextMove
    