#! /usr/bin/env python3

import random

class DrawOnePropulsor:
    def __init__(self, cards, shuffle = random.shuffle):
        self.cards = cards
        self.shuffle = shuffle
        self.newRace()

    def generateMove(self):
        if self.index >= len(self.cards):
            return ""
        move = self.cards[self.index]
        self.index += 1
        return move
    
    def newRace(self):
        self.index = 0
        self.shuffle(self.cards)
    
    def exhaust(self):
        pass