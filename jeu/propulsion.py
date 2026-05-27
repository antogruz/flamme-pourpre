#!/usr/bin/env python3

class SequentialPropulsion():
    def __init__(self, oracle):
        self.oracle = oracle

    def pickNextMoves(self, riders):
        moves = {}
        ridersToPick = list(riders)
        while (ridersToPick):
            rider = self.pickRider(ridersToPick)
            moves[rider] = rider.personnage.propulsor.generateMoves()
        return moves

    def pickRider(self, riders):
        choice = self.oracle.pickWithRiders([(r, "") for r in riders], "Pick a rider")
        if choice < 0 or choice >= len(riders):
            choice = 0
        return riders.pop(choice)

class SimpleTeamPropulsion():
    def pickNextMoves(self, riders):
        return {r: r.personnage.propulsor.generateMoves() for r in riders}
