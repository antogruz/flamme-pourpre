#!/usr/bin/env python3

# La classe des cartes doit changer si les règles de manipulations des cartes d'une équipe changent.
# Par exemple, si un coureur pioche les cartes par 6, peut rejouer certaines cartes, ou ne se débarasse plus de ses cartes fatigue.
# Si on ne doit plus mélanger le deck, ou si on doit le mélanger après chaque coup.


def noop(list):
    pass

class Cards:
    def __init__(self, deck, shuffle = noop, endOfRaceDecksManagers = []):
        self.deck = deck
        self.discard = []
        self.played = []
        self.shuffle = shuffle
        self.handSize = 4
        self.endOfRaceDecksManagers = endOfRaceDecksManagers
        shuffle(self.deck)

    def inDeck(self):
        return len(self.deck)

    def draw(self):
        self.hand = []
        for i in range(self.handSize):
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
        if not card:
            return
        self.hand.remove(card)
        if card != "f":
            self.played.append(card)
        self.discard += self.hand

    def newRace(self):
        self.deck = self.deck + self.discard
        self.discard = []
        for deckManager in self.endOfRaceDecksManagers:
            deckManager.modifyCards(self)
        self.reshuffleAll()

    def reshuffleAll(self):
        self.deck = self.deck + self.played
        self.played = []
        self.shuffle(self.deck)


class ExhaustRecovery:
    def __init__(self, percentageToRemove):
        self.percentageToRemove = percentageToRemove

    def modifyCards(self, cards):
        removeExhausts(cards.deck, int(countExhaust(cards.deck) * self.percentageToRemove))

def removeExhausts(deck, count):
    for i in range(count):
        deck.remove("f")

def countExhaust(deck):
    return deck.count("f")


from unittests import assert_equals, runTests, assert_similars
class CardsTester():
    def testDrawAllDeck(self):
        cards = Cards(deck(4))
        cards.draw()
        assert_equals(0, cards.inDeck())

    def testNoDraw(self):
        cards = Cards(deck(4))
        assert_equals(4, cards.inDeck())

    def testDrawGet4Cards(self):
        cards = Cards(deck(6))
        drawn = cards.draw()
        assert_equals(4, len(drawn))
        assert_equals(2, cards.inDeck())

    def testDeckIsShuffled(self):
        cards = Cards(deck(6), increasingOrder)
        assert_similars([1, 2, 3, 4], cards.draw())

    def testCardPlayedIsOut(self):
        cards = Cards(deck(4))
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
        cards = Cards(deck(1))
        cards.draw()
        cards.play(1)
        assert_similars([], cards.draw())
        assert_similars([], cards.discard)

    def testPlayingExhaustCardDontShowIt(self):
        cards = Cards([3, 4, 5, "f"])
        cards.draw()
        cards.play("f")
        assert_similars([], cards.played)

    def testCardsAreRestoredAfterRace(self):
        cards = Cards(deck(4), noop)
        cards.draw()
        cards.play(1)
        cards.newRace()
        assert_similars([], cards.played)
        assert_similars(deck(4), cards.deck)
        assert_similars([], cards.discard)

    def testExhaustRemoved(self):
        cards = Cards(["f", 3, 4, 5, "f", "f"], noop, [ExhaustRecovery(1)])
        cards.draw()
        cards.play(3)
        cards.newRace()
        assert_similars([3, 4, 5], cards.deck)

    def testHalfRecovery(self):
        cards = Cards(["f", 3, 4, 5, "f", "f"], noop, [ExhaustRecovery(0.5)])
        cards.newRace()
        assert_similars(["f", "f", 3, 4, 5], cards.deck)


def deck(n):
    return [ i for i in reversed(range(1, n + 1)) ]


def increasingOrder(list):
    list.sort()


if __name__ == "__main__":
    runTests(CardsTester())
