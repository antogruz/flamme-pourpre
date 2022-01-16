#!/usr/bin/env python3

from unittests import assert_equals, Tester, assert_similars

def tests():
    CardsTester().runTests()

class CardsTester(Tester):
    def testDrawAllDeck(self):
        cards = Cards(deck(4), noop)
        cards.draw()
        assert_equals(0, cards.inDeck())

    def testNoDraw(self):
        cards = Cards(deck(4), noop)
        assert_equals(4, cards.inDeck())

    def testDrawGet4Cards(self):
        cards = Cards(deck(6), noop)
        drawn = cards.draw()
        assert_equals(4, len(drawn))
        assert_equals(2, cards.inDeck())

    def testDeckIsShuffled(self):
        cards = Cards(deck(6), increasingOrder)
        assert_similars([1, 2, 3, 4], cards.draw())

    def testCardPlayedIsOut(self):
        cards = Cards(deck(4), noop)
        cards.draw()
        cards.play(1)
        assert_similars([2, 3, 4], cards.draw())

    def testShuffleOnlyAfterAllDeckDrawn(self):
        cards = Cards(deck(8), increasingOrder)
        cards.draw()
        cards.play(1)
        assert_similars([5, 6, 7, 8], cards.draw())

    def testDraw4EvenWhen2CardsLeftInDeck(self):
        cards = Cards(deck(6), increasingOrder)
        cards.draw()
        cards.play(2)
        assert_similars([5, 6, 1, 3], cards.draw())

    def testSeveralDiscards(self):
        cards = Cards(deck(10), increasingOrder)
        cards.draw()
        cards.play(2)
        cards.draw()
        cards.play(5)
        assert_similars([9, 10, 1, 3], cards.draw())
        cards.play(9)
        assert_similars([4, 6, 7, 8], cards.draw())
        cards.play(4)
        assert_similars([1, 3, 6, 7], cards.draw())


    def testSeveralShuffles(self):
        cards = Cards(deck(6), increasingOrder)
        cards.draw()
        cards.play(1)
        cards.draw()
        cards.play(5)
        cards.draw()
        cards.play(2)
        assert_similars([3, 4, 6], cards.draw())

    def test1card(self):
        cards = Cards(deck(1), noop)
        cards.draw()
        cards.play(1)
        assert_similars([], cards.draw())
        assert_similars([], cards.discard)

def deck(n):
    return [ i for i in reversed(range(1, n + 1)) ]


def noop(list):
    pass

def increasingOrder(list):
    list.sort()

class Cards():
    def __init__(self, deck, shuffle = noop):
        self.deck = deck
        self.discard = []
        self.played = []
        self.shuffle = shuffle
        shuffle(self.deck)

    def inDeck(self):
        return len(self.deck)

    def draw(self):
        self.hand = []
        for i in range(4):
            self.drawOne()
        return self.hand

    def drawOne(self):
        if not self.deck:
            self.deck = [ card for card in self.discard ]
            self.shuffle(self.deck)
            self.discard = []

        if not self.deck:
            return

        self.hand.append(self.deck.pop(0))

    def play(self, card):
        self.hand.remove(card)
        self.played.append(card)
        self.discard += self.hand

def noop(a):
    pass

if __name__ == "__main__":
    tests()
