#!/usr/bin/env python3

class Rider():
    def __init__(self, name, cards, riderMove):
        self.name = name
        self.cards = cards
        self.riderMove = riderMove

    def draw(self):
        return self.cards.draw()

    def play(self, card):
        self.cards.play(card)
        if card == "f":
            self.nextMove = 2
        else:
            self.nextMove = card

    def position(self):
        return self.riderMove.position()

    def move(self, distance, track, obstacles):
        return self.riderMove.move(distance, track, obstacles)

    def getSlipstream(self, track):
        return self.riderMove.getSlipstream(track)

    def getSquare(self):
        return self.riderMove.position()[0]

    def exhaust(self):
        self.cards.discard.append("f")

