#! /usr/bin/env python3

from cards import Cards, Card, FatigueCard, SimpleCard, createCards


class DeckPropulsor:
    def __init__(self, cards, oracle):
        self.cards = cards
        self.oracle = oracle
        self.extras = []

    def addExtraChoice(self, provider):
        self.extras.append(provider)

    def generateMoves(self):
        """Returns the list of Moves played this turn.

        The list contains the played card first (or EmptyCard for empty
        hand / skip), followed by each non-terminating choice's own Move
        contribution, in pick order. Each Move exposes label() + energy();
        the engine sums their energies, animations can iterate them.
        """
        primary = list(self.cards.draw())
        picked = []
        moves = []
        while True:
            available = [e for e in self.extras if e.isAvailable() and e not in picked]
            choices = primary + available
            if not choices:
                return [EmptyCard()]
            index = self.pick([c.label() for c in choices], "Play a card")
            choice = choices[index]
            move = choice.onPlay(self.cards)
            if choice.doesEndTurn():
                return [move] + moves
            picked.append(choice)
            moves.append(move)

    def newRace(self):
        self.cards.newRace()
        for extra in self.extras:
            extra.newRace()

    def pick(self, list, instruction):
        choice = self.oracle.pick(list, instruction)
        if choice < 0 or choice >= len(list):
            return 0
        return choice

    def exhaust(self):
        self.cards.discard.append(FatigueCard())

class EmptyCard(Card):
    """Fallback card returned by the propulsor when the hand is empty."""
    def label(self):
        return ""

    def energy(self):
        return 2

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def onPlay(self, cards):
        return self

    def doesEndTurn(self):
        return True


from unittests import assert_equals, runTests, assert_similars
class TerminatingExample(Card):
    def __init__(self, energy):
        self._energy = energy

    def label(self):
        return str(self._energy)

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def onPlay(self, cards):
        cards.discardHand()
        return self

    def energy(self):
        return self._energy

    def doesEndTurn(self):
        return True


class CombiningExample(Card):
    def __init__(self, bonus):
        self.bonus = bonus

    def label(self):
        return f"+{self.bonus}"

    def energy(self):
        return self.bonus

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def onPlay(self, cards):
        return self

    def doesEndTurn(self):
        return False


class DeckPropulsorTest:
    def testPlayFirstCard(self):
        cards = Cards(createCards([9, 3, "f", 5]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        assert_equals([9], energies(propulsor.generateMoves()))
        assert_equals([3], energies(propulsor.generateMoves()))
        assert_equals([2], energies(propulsor.generateMoves()))  # fatigue
        assert_equals([5], energies(propulsor.generateMoves()))
        assert_equals([2], energies(propulsor.generateMoves()))  # empty hand default

    def testPlayTerminatingExtra(self):
        cards = Cards(createCards([9, 3, "f", 5]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(TerminatingExample(8))
        assert_equals([8], energies(propulsor.generateMoves()))

    def testCombiningExtraStacksOnCard(self):
        cards = Cards(createCards([5, 5, 5, 5]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(CombiningExample(2))
        moves = propulsor.generateMoves()
        assert_equals([5, 2], energies(moves))
        assert_equals(["5", "+2"], labels(moves))

    def testCombiningExtraStacksOnTerminatingExtra(self):
        cards = Cards([])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        propulsor.addExtraChoice(CombiningExample(3))
        propulsor.addExtraChoice(TerminatingExample(10))
        moves = propulsor.generateMoves()
        assert_equals([10, 3], energies(moves))

    def testCombiningExtrasInPickOrder(self):
        cards = Cards(createCards([4, 4, 4, 4]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(CombiningExample(1))
        propulsor.addExtraChoice(CombiningExample(2))
        # Pick order: +1, then +2 (now first in extras list), then Card(4).
        # The list reflects all moves of the turn.
        moves = propulsor.generateMoves()
        # Terminating card comes first, then combining cards in pick order.
        assert_equals(["4", "+1", "+2"], labels(moves))
        assert_equals(7, sum(m.energy() for m in moves))

    def testEmptyHandReturnsEmptyCard(self):
        cards = Cards([])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        moves = propulsor.generateMoves()
        assert_equals([""], labels(moves))
        assert_equals([2], energies(moves))

    def testExhaustPushesFatigueCard(self):
        cards = Cards(createCards([5]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        propulsor.exhaust()
        assert_equals(1, len(cards.discard))
        assert_equals("f", cards.discard[0].label())


def labels(moves):
    return [m.label() for m in moves]

def energies(moves):
    return [m.energy() for m in moves]


class ChoiceDoer():
    def __init__(self, always):
        self.always = always

    def pick(self, possibilities, *_):
        return self.always


if __name__ == "__main__":
    runTests(DeckPropulsorTest())
