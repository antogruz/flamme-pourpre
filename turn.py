#!/usr/bin/env python3

def turn():
    for p in players:
        p.pickNextMoves()

    for r in orderedByPosition(riders):
        r.move(r.nextMove)

    slipstreaming(riders)
    exhaust(riders)


