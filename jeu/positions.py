#!/usr/bin/env python3

def headToTail(riders):
    return sorted(riders, key = absolutePosition, reverse = True)

def tailToHead(riders):
    return sorted(riders, key = absolutePosition)

def absolutePosition(rider):
    square, lane = rider.position()
    return 10*square + 1 - lane

# Convention pour les PlayOrderRule:
# chaque rule retourne un tuple ; on prend min sur les rules d'un même rider ;
# on trie ascendant entre riders. Plus petit = joue plus tôt.
def playOrder(riders, snapshot):
    return sorted(riders, key = lambda r: playOrderKey(r, snapshot))

def playOrderKey(rider, snapshot):
    rules = rider.personnage.playOrderRules
    if not rules:
        return (0, -absolutePosition(rider))
    return min(rule.keyFor(rider, snapshot) for rule in rules)


class PlayOrderRule:
    """Interface for influencing a rider's play order priority.

    Implement this to override or refine when a rider plays during a turn.
    Each rule returns a sort key (tuple); rules attached to the same rider are
    min-composed, and riders are ordered ascending. Lower key = plays earlier.
    """
    def keyFor(self, rider, snapshot):
        """Return the sort key tuple for `rider` given the race `snapshot`."""
        pass

