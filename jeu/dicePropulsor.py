import random

class DicePropulsor:
    """Propulsion basée sur un choix aléatoire (bots)"""
    
    def __init__(self, moves):
        self.moves = moves
        self.nextMove = None
    
    def generateMove(self):
        self.nextMove = random.choice(self.moves)
        return self.nextMove
    
    def newRace(self):
        pass
    
    def exhaust(self):
        pass 