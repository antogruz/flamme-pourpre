import random
from cards import SimpleCard, FatigueCard
from deckPropulsor import EmptyCard

class DicePropulsor:
    """Propulsion basée sur un choix aléatoire (bots)"""

    def __init__(self, moves):
        self.moves = [asMove(m) for m in moves]

    def generateMove(self):
        return random.choice(self.moves)

    def newRace(self):
        pass

    def exhaust(self):
        pass


def asMove(raw):
    return SimpleCard(int(raw))
