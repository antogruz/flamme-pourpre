import random

class DicePropulsor:
    """Propulsion basée sur un choix aléatoire (bots)"""

    def __init__(self, moves):
        self.moves = moves

    def generateMove(self):
        return random.choice(self.moves)

    def newRace(self):
        pass

    def exhaust(self):
        pass
