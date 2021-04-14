#!/usr/bin/env python3

from unittests import assert_equals, Tester, assert_similars

def tests():
    CardsTester().runTests()

class CardsTester(Tester):
    def testDrawAllDeck(self):
        cards = Cards([1, 2, 3, 4], noop)
        cards.draw()
        assert_equals(0, cards.inDeck())

    def testNoDraw(self):
        cards = Cards([1, 2, 3, 4], noop)
        assert_equals(4, cards.inDeck())

    def testDrawGet4Cards(self):
        cards = Cards([1, 2, 3, 4, 5, 6], noop)
        drawn = cards.draw()
        assert_equals(4, len(drawn))
        assert_equals(2, cards.inDeck())

    def testDeckIsShuffled(self):
        cards = Cards([6, 5, 4, 3, 2, 1], increasingOrder)
        assert_similars([1, 2, 3, 4], cards.draw())


def noop(list):
    pass

def increasingOrder(list):
    list.sort()

class Cards():
    def __init__(self, deck, shuffle):
        self.deck = deck
        shuffle(self.deck)

    def inDeck(self):
        return len(self.deck)

    def draw(self):
        return [ self.deck.pop(0) for i in range(4) ]


if __name__ == "__main__":
    tests()
