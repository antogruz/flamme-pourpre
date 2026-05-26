#! /usr/bin/env python3

from cards import Cards, FatigueCard, SimpleCard, TerminatingChoice, createCards


class DeckPropulsor:
    def __init__(self, cards, oracle):
        self.cards = cards
        self.oracle = oracle
        self.extras = []

    def addExtraChoice(self, provider):
        self.extras.append(provider)

    def generateMove(self):
        primary = list(self.cards.draw())
        combining = []
        while True:
            available = [e for e in self.extras if e.isAvailable() and e not in combining]
            choices = primary + available
            if not choices:
                return EmptyCard()
            index = self.pick([c.label() for c in choices], "Play a card")
            choice = choices[index]
            if isinstance(choice, CombiningChoice):
                combining.append(choice)
                continue
            labelAndEnergy = choice.onPlay(self.cards)
            for c in reversed(combining):
                labelAndEnergy = c.combine(labelAndEnergy, self)
            return labelAndEnergy

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

class EmptyCard:
    def label(self):
        return ""

    def energy(self):
        return 2


class CombiningChoice:
    """A choice that stacks on top of a TerminatingChoice to modify the move.

    Combining choices are picked one after another; the propulsor keeps
    offering choices until a TerminatingChoice is picked. Then each
    combining choice's combine(labelAndEnergy, propulsor) runs in reverse
    pick order (last picked first applied) on the terminating choice's
    result.

    Both `label()` and `energy()` of the returned object can be modified:
    energy is what the engine uses to move the rider, label is what the UI
    can display (animations, played-card history, etc.).

    Typical examples: Boost (adds a bonus to the played card), Accélération
    en col (sets a flag bypassing the mountain limit).
    """
    def label(self): pass
    def isAvailable(self): pass
    def newRace(self): pass
    def combine(self, labelAndEnergy, propulsor):
        """Modify the move (label + energy) produced by a previous choice.

        Returns an object exposing label() and energy() — typically a
        decorator that wraps the previous one (see BoostedCard,
        MultipliedCard for reference patterns).
        """
        return labelAndEnergy


from unittests import assert_equals, runTests, assert_similars
class TerminatingChoiceExample(TerminatingChoice):
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


class CombiningChoiceExample(CombiningChoice):
    def __init__(self, bonus):
        self.bonus = bonus

    def label(self):
        return f"+{self.bonus}"

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def combine(self, value, propulsor):
        return BoostedCard(value, self.bonus)


class MultiplyingChoiceExample(CombiningChoice):
    def __init__(self, factor):
        self.factor = factor

    def label(self):
        return f"x{self.factor}"

    def isAvailable(self):
        return True

    def newRace(self):
        pass

    def combine(self, value, propulsor):
        return MultipliedCard(value, self.factor)


class BoostedCard:
    def __init__(self, base, bonus):
        self.base = base
        self.bonus = bonus

    def label(self):
        return f"{self.base.label()}+{self.bonus}"

    def energy(self):
        return self.base.energy() + self.bonus


class MultipliedCard:
    def __init__(self, base, factor):
        self.base = base
        self.factor = factor

    def label(self):
        return f"{self.base.label()}x{self.factor}"

    def energy(self):
        return self.base.energy() * self.factor


class DeckPropulsorTest:
    def testPlayFirstCard(self):
        cards = Cards(createCards([9, 3, "f", 5]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        assert_equals(9, propulsor.generateMove().energy())
        assert_equals(3, propulsor.generateMove().energy())
        assert_equals(2, propulsor.generateMove().energy())  # fatigue
        assert_equals(5, propulsor.generateMove().energy())
        assert_equals(2, propulsor.generateMove().energy())  # empty hand default

    def testPlayTerminatingExtra(self):
        cards = Cards(createCards([9, 3, "f", 5]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(TerminatingChoiceExample(8))
        assert_equals(8, propulsor.generateMove().energy())

    def testCombiningExtraStacksOnCard(self):
        cards = Cards(createCards([5, 5, 5, 5]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(CombiningChoiceExample(2))
        assert_equals(7, propulsor.generateMove().energy())

    def testCombiningExtraStacksOnTerminatingExtra(self):
        cards = Cards([])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        propulsor.addExtraChoice(CombiningChoiceExample(3))
        propulsor.addExtraChoice(TerminatingChoiceExample(10))
        assert_equals(13, propulsor.generateMove().energy())

    def testCombiningExtrasAppliedInReverseOrder(self):
        cards = Cards(createCards([4, 4, 4, 4]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(CombiningChoiceExample(1))
        propulsor.addExtraChoice(MultiplyingChoiceExample(2))
        # Pick order: Add(1) then Mul(2) then Card(4).
        # Reverse application: Mul first, then Add → (4 * 2) + 1 = 9.
        move = propulsor.generateMove()
        assert_equals(9, move.energy())
        assert_equals("4x2+1", move.label())

    def testEmptyHandReturnsEmptyCard(self):
        cards = Cards([])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        move = propulsor.generateMove()
        assert_equals("", move.label())
        assert_equals(2, move.energy())

    def testExhaustPushesFatigueCard(self):
        cards = Cards(createCards([5]))
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        propulsor.exhaust()
        assert_equals(1, len(cards.discard))
        assert_equals("f", cards.discard[0].label())


class ChoiceDoer():
    def __init__(self, always):
        self.always = always

    def pick(self, possibilities, *_):
        return self.always


if __name__ == "__main__":
    runTests(DeckPropulsorTest())
