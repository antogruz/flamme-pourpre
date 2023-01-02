#!/usr/bin/env python3

class Rider():
    def __init__(self, name, cards, riderMove = None):
        self.name = name
        self.cards = cards
        self.riderMove = riderMove

    def draw(self):
        return self.cards.draw()

    def play(self, card):
        self.cards.play(card)
        if card == "f" or card == "":
            self.nextMove = 2
        else:
            self.nextMove = card

    def position(self):
        return self.riderMove.position()

    def move(self, track, obstacles):
        return self.riderMove.move(self.nextMove, track, obstacles)

    def getSlipstream(self, track):
        return self.riderMove.getSlipstream(track)

    def getSquare(self):
        return self.riderMove.position()[0]

    def exhaust(self):
        self.cards.discard.append("f")


from unittests import *
from player import Player, ChoiceDoer
from cards import Cards

class IntegrationTester():
    def testEmptyDeck(self):
        rider = Rider("exhausted", Cards([]))
        player = Player(ChoiceDoer([0, 0, 0]), [rider])
        player.pickNextMoves()
        assert_equals(2, rider.nextMove)


if __name__ == "__main__":
    runTests(IntegrationTester())

