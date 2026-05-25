#! /usr/bin/env python3

class DeckPropulsor:
    def __init__(self, cards, oracle):
        self.cards = cards
        self.oracle = oracle
        self.extras = []

    def addExtraChoice(self, provider):
        self.extras.append(provider)

    def generateMove(self):
        cards = self.cards.draw()
        primary = [CardChoice(c) for c in cards]
        combining = []
        while True:
            available = [e for e in self.extras if e.isAvailable() and e not in combining]
            choices = primary + available
            if not choices:
                return ""
            index = self.pick([c.label() for c in choices], "Play a card")
            choice = choices[index]
            if isinstance(choice, CombiningChoice):
                combining.append(choice)
                continue
            value = choice.applyTo(self)
            for c in reversed(combining):
                value = c.combine(value, self)
            return value

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
        self.cards.discard.append("f")


from unittests import *
from cards import Cards


class Choice:
    """Common base for entries in the propulsor's per-turn choice list.

    Each turn, DeckPropulsor.generateMove() builds a list of Choices made
    of (a) the drawn cards, wrapped in CardChoice, and (b) the extras
    registered by talents via addExtraChoice(). The oracle picks one of
    them by index; the propulsor then loops or stops depending on the
    choice's type — see TerminatingChoice and CombiningChoice for the
    two specialisations.

    Subclasses should always inherit from TerminatingChoice or
    CombiningChoice rather than directly from Choice.
    """

    def label(self):
        """Return the display name shown to the oracle in the choice list."""
        pass

    def isAvailable(self):
        """Return whether this choice should be offered this turn.

        Called once per loop iteration in generateMove(), after the hand
        has been drawn. Use this to gate the choice on remaining uses,
        hand size, road type, etc.
        """
        pass

    def newRace(self):
        """Reset per-race state at the start of a new race.

        Called by DeckPropulsor.newRace(). Override to reset counters
        such as remaining uses for once-per-race effects.
        """
        pass


class TerminatingChoice(Choice):
    """A choice that ends the per-turn loop and yields the move value.

    The canonical case is CardChoice (play a card from the hand). Talents
    can also expose terminating choices that replace the card play
    altogether (e.g. EconomieEnergie's "skip the hand").
    """

    def applyTo(self, propulsor):
        """Apply the choice's effect and return the move value.

        Called once the oracle picks this choice as the final one of the
        turn. Should play or discard cards on `propulsor.cards` and
        return the value to be fed to EnergyRules.energyFromCard()
        (possibly after combining choices apply on top of it).
        """
        pass


class CombiningChoice(Choice):
    """A choice that stacks on top of a later choice to modify its value.

    Combining choices are picked one after another; the propulsor keeps
    offering choices until a TerminatingChoice is picked. Then each
    combining choice's combine(value, propulsor) runs in reverse pick
    order (last picked first applied) on the terminating choice's value.

    Typical examples: Boost (adds a bonus to the played card), Accélération
    en col (sets a flag bypassing the mountain limit).
    """

    def combine(self, value, propulsor):
        """Modify the move value produced by a previous choice.

        Should apply the side effect (set a bypass flag, decrement usage
        counter, ...) and return the new move value.
        """
        return value


class CardChoice(TerminatingChoice):
    def __init__(self, value):
        self.value = value

    def label(self):
        return self.value

    def isAvailable(self):
        return True

    def applyTo(self, propulsor):
        propulsor.cards.play(self.value)
        return self.value


class TerminatingChoiceExample(TerminatingChoice):
    def __init__(self, value):
        self.value = value

    def label(self):
        return self.value

    def isAvailable(self):
        return True

    def applyTo(self, propulsor):
        propulsor.cards.discardHand()
        return self.value


class CombiningChoiceExample(CombiningChoice):
    def __init__(self, bonus):
        self.bonus = bonus

    def label(self):
        return f"+{self.bonus}"

    def isAvailable(self):
        return True

    def combine(self, value, propulsor):
        return value + self.bonus


class MultiplyingChoiceExample(CombiningChoice):
    def __init__(self, factor):
        self.factor = factor

    def label(self):
        return f"x{self.factor}"

    def isAvailable(self):
        return True

    def combine(self, value, propulsor):
        return value * self.factor


class DeckPropulsorTest:
    def testPlayFirstCard(self):
        cards = Cards([9, 3, "f", 5])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        assert_equals(9, propulsor.generateMove())
        assert_equals(3, propulsor.generateMove())
        assert_equals("f", propulsor.generateMove())
        assert_equals(5, propulsor.generateMove())
        assert_equals("", propulsor.generateMove())

    def testPlayTerminatingExtra(self):
        cards = Cards([9, 3, "f", 5])
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(TerminatingChoiceExample(8))
        assert_equals(8, propulsor.generateMove())

    def testCombiningExtraStacksOnCard(self):
        cards = Cards([5, 5, 5, 5])
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(CombiningChoiceExample(2))
        assert_equals(7, propulsor.generateMove())

    def testCombiningExtraStacksOnTerminatingExtra(self):
        cards = Cards([])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        propulsor.addExtraChoice(CombiningChoiceExample(3))
        propulsor.addExtraChoice(TerminatingChoiceExample(10))
        assert_equals(13, propulsor.generateMove())

    def testCombiningExtrasAppliedInReverseOrder(self):
        cards = Cards([4, 4, 4, 4])
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(CombiningChoiceExample(1))
        propulsor.addExtraChoice(MultiplyingChoiceExample(2))
        # Pick order: Add(1) then Mul(2) then Card(4).
        # Reverse application: Mul first, then Add → (4 * 2) + 1 = 9.
        assert_equals(9, propulsor.generateMove())


class ChoiceDoer():
    def __init__(self, always):
        self.always = always

    def pick(self, possibilities, *_):
        return self.always

if __name__ == "__main__":
    runTests(DeckPropulsorTest())
