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
        rider.nextMove = rider.persistent.propulsor.generateMove()
        rider.logCardPlayed = rider.nextMove

    def pickRider(self, riders):
        choice = self.pick([r.persistent.name for r in riders], "Pick a rider")
        return riders.pop(choice)

    def pick(self, list, instruction):
        choice = self.oracle.pick(list, instruction)
        if choice < 0 or choice >= len(list):
            return 0
        return choice

class SimpleTeamPropulsion():
    def pickNextMoves(self, riders):
        for r in riders:
            r.nextMove = r.persistent.propulsor.generateMove()
            r.logCardPlayed = r.nextMove
    