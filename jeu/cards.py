#!/usr/bin/env python3

# La classe des cartes doit changer si les règles de manipulations des cartes d'une équipe changent.
# Par exemple, si un coureur pioche les cartes par 6, peut rejouer certaines cartes, ou ne se débarasse plus de ses cartes fatigue.
# Si on ne doit plus mélanger le deck, ou si on doit le mélanger après chaque coup.


def noop(list):
    pass

class Cards:
    def __init__(self, deck, shuffle = noop, endOfRaceDecksManagers = None):
        self.deck = deck
        self.discard = []
        self.played = []
        self.shuffle = shuffle
        self.handSize = 4
        self.endOfRaceDecksManagers = endOfRaceDecksManagers if endOfRaceDecksManagers is not None else []
        shuffle(self.deck)

    def inDeck(self):
        return len(self.deck)

    def discardCount(self):
        return len(self.discard)

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
        card.onPlay(self)

    def commitPlay(self, card, pile):
        """Helper for Card.onPlay implementations: removes `card` from
        the hand, places it on `pile` (set to None to make it vanish),
        records `lastDiscarded`, and discards the rest of the hand.
        """
        self.hand.remove(card)
        if pile is not None:
            pile.append(card)
        self.lastDiscarded = self.hand.copy()
        self.discard += self.hand
        self.hand = []

    def discardHand(self):
        self.discard += self.hand
        self.hand = []

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

    def cardsLeft(self):
        return len(self.deck) + len(self.hand) + len(self.discard)


class ExhaustRecovery:
    def __init__(self, percentageToRemove):
        self.percentageToRemove = percentageToRemove

    def modifyCards(self, cards):
        removeExhausts(cards.deck, int(countExhaust(cards.deck) * self.percentageToRemove))

def removeExhausts(deck, count):
    for i, card in enumerate(exhaustCards(deck)):
        if i >= count:
            return
        deck.remove(card)

def countExhaust(deck):
    return len(exhaustCards(deck))

def exhaustCards(deck):
    return [card for card in deck if card.label() == "f"]


class Card:
    """Interface for anything the player can pick to play each turn.

    Covers both cards cycling through the deck (SimpleCard,
    FatigueCard, OpportunisticCard) and permanent extras added by
    talents (BoostChoice, AccelerationChoice, SkipProvider). The
    object doesn't need to know whether it lives in a deck cycle or
    as a permanent extra — those are just two ways the propulsor
    makes it available.

    Each card carries its own energy and label (used both for the
    pick menu and animations). onPlay(cards) applies the side effect
    (deck mutation, internal counter, etc.) and returns the Card
    contributed to the turn's list — often `self`. doesEndTurn()
    tells the propulsor whether to keep offering picks or commit.
    """
    def label(self): pass
    def energy(self): pass
    def isAvailable(self): pass
    def newRace(self): pass
    def onPlay(self, cards): pass
    def doesEndTurn(self): pass


class SimpleCard(Card):
    def __init__(self, number):
        self.number = number

    def label(self):
        return str(self.number)

    def energy(self):
        return self.number

    def setEnergy(self, value):
        """Mutate the card's energy in place. Talents that increment/decrement
        a card should call this rather than swapping the card with a new one,
        so that other systems holding a reference to the card stay in sync.
        """
        self.number = value

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def onPlay(self, cards):
        cards.commitPlay(self, cards.played)
        return self

    def doesEndTurn(self):
        return True


class FatigueCard(Card):
    def label(self):
        return "f"

    def energy(self):
        return 2

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def onPlay(self, cards):
        cards.commitPlay(self, None)
        return self

    def doesEndTurn(self):
        return True


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
        assert_similars([1, 2, 3, 4], energies(cards.draw()))

    def testCardPlayedIsOut(self):
        cards = Cards(deck(4))
        drawAndPlay(cards, 1)
        assert_similars([2, 3, 4], energies(cards.draw()))

    def testShuffleOnlyAfterAllDeckDrawn(self):
        cards = Cards(deck(8), increasingOrder)
        drawAndPlay(cards, 1)
        assert_similars([5, 6, 7, 8], energies(cards.draw()))

    def testDraw4EvenWhen2CardsLeftInDeck(self):
        cards = Cards(deck(6), increasingOrder)
        drawAndPlay(cards, 2)
        assert_similars([5, 6, 1, 3], energies(cards.draw()))


    def testSeveralDiscards(self):
        cards = Cards(deck(10), increasingOrder)
        drawAndPlay(cards, 2)
        drawAndPlay(cards, 5)
        drawAndPlay(cards, 9)
        drawAndPlay(cards, 4)
        assert_similars([1, 3, 6, 7], energies(cards.draw()))


    def testSeveralShuffles(self):
        cards = Cards(deck(6), increasingOrder)
        drawAndPlay(cards, 1)
        drawAndPlay(cards, 5)
        drawAndPlay(cards, 2)
        assert_similars([3, 4, 6], energies(cards.draw()))

    def test1card(self):
        cards = Cards(deck(1))
        drawAndPlay(cards, 1)
        assert_similars([], cards.draw())
        assert_similars([], cards.discard)

    def testPlayingExhaustCardDontShowIt(self):
        cards = Cards(createCards([3, 4, 5, "f"]))
        hand = cards.draw()
        fatigue = [card for card in hand if card.label() == "f"][0]
        cards.play(fatigue)
        assert_similars([], cards.played)

    def testCardsAreRestoredAfterRace(self):
        cards = Cards(deck(4), noop)
        drawAndPlay(cards, 1)
        cards.newRace()
        assert_similars([], cards.played)
        assert_similars(energies(deck(4)), energies(cards.deck))
        assert_similars([], cards.discard)

    def testExhaustRemoved(self):
        cards = Cards(createCards(["f", 3, 4, 5, "f", "f"]), noop, [ExhaustRecovery(1)])
        drawAndPlay(cards, 3)
        cards.newRace()
        assert_similars([3, 4, 5], energies(cards.deck))

    def testHalfRecovery(self):
        cards = Cards(createCards(["f", 3, 4, 5, "f", "f"]), noop, [ExhaustRecovery(0.5)])
        cards.newRace()
        assert_similars(["f", "f", "3", "4", "5"], labels(cards.deck))

def energies(cards):
    return [ card.energy() for card in cards ]

def labels(cards):
    return [ card.label() for card in cards ]

def deck(n):
    return [ SimpleCard(i) for i in reversed(range(1, n + 1)) ]

def createCards(list):
    return [ SimpleCard(int(i)) if i != "f" else FatigueCard() for i in list ]

def increasingOrder(list):
    list.sort(key=lambda x: x.energy())

def drawAndPlay(cards, energy):
    hand = cards.draw()
    picked = [card for card in hand if card.energy() == energy][0]
    cards.play(picked)

if __name__ == "__main__":
    runTests(CardsTester())
