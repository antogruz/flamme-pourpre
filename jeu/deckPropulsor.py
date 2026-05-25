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
            if not choice.isCombining():
                value = choice.applyTo(self)
                for c in reversed(combining):
                    value = c.combine(value, self)
                return value
            combining.append(choice)

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


class ExtraChoice:
    """Interface for non-card choices offered by a DeckPropulsor.

    Extras are registered via DeckPropulsor.addExtraChoice() and appear
    alongside the drawn cards each turn, giving talents a way to surface
    options that don't directly come from the hand: skip the hand, play
    a card with a special effect, boost the energy of another choice,
    bypass a road-type limit, etc.

    There are two flavours of extra, distinguished by isCombining():

    - Terminating choices (the default) end the choice loop and provide
      the value that becomes the rider's move. CardChoice itself is a
      terminating choice; talent examples include EconomieEnergie's
      "skip the hand" choice.

    - Combining choices are picked first and stack on top of a later
      choice. The propulsor loops: each time a combining choice is
      picked it is held aside and another choice is offered, until the
      oracle picks a terminating choice. The terminating choice
      provides an initial value, then each combining choice's
      combine(value, propulsor) is applied in reverse order of
      selection (last picked, first applied).
    """

    def label(self):
        """Return the display name shown to the oracle in the choice list."""
        pass

    def isAvailable(self):
        """Return whether this extra should be offered this turn.

        Called once per loop iteration in generateMove(), after the
        hand has been drawn. Use this to gate the choice on remaining
        uses, hand size, road type, etc.
        """
        pass

    def isCombining(self):
        """Return False for a terminating choice, True for a combining one.

        Defaults to terminating, the most common case.
        """
        return False

    def applyTo(self, propulsor):
        """Apply a terminating choice's effect and return the move value.

        Only called for terminating choices, once the oracle has picked
        this choice as the final one of the turn. Should play/discard
        cards as needed on `propulsor.cards` and return the value to be
        fed to EnergyRules.energyFromCard() (possibly after combining
        choices apply on top).
        """
        pass

    def combine(self, value, propulsor):
        """Modify the move value produced by an earlier choice.

        Only called for combining choices, in reverse pick order, once
        the terminating choice has provided an initial value. Should
        apply the side effect (set a bypass flag, decrement usage, ...)
        and return the new value.
        """
        return value

    def newRace(self):
        """Reset per-race state at the start of a new race.

        Called by DeckPropulsor.newRace(). Override to reset counters
        such as remaining uses for once-per-race effects.
        """
        pass


class CardChoice(ExtraChoice):
    def __init__(self, value):
        self.value = value

    def label(self):
        return self.value

    def isAvailable(self):
        return True

    def applyTo(self, propulsor):
        propulsor.cards.play(self.value)
        return self.value


class TerminatingExtraExample(ExtraChoice):
    def __init__(self, value):
        self.value = value

    def label(self):
        return self.value

    def isAvailable(self):
        return True

    def applyTo(self, propulsor):
        propulsor.cards.discardHand()
        return self.value


class CombiningExtraExample(ExtraChoice):
    def __init__(self, bonus):
        self.bonus = bonus

    def label(self):
        return f"+{self.bonus}"

    def isAvailable(self):
        return True

    def isCombining(self):
        return True

    def combine(self, value, propulsor):
        return value + self.bonus


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
        propulsor.addExtraChoice(TerminatingExtraExample(8))
        assert_equals(8, propulsor.generateMove())

    def testCombiningExtraStacksOnCard(self):
        cards = Cards([5, 5, 5, 5])
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(CombiningExtraExample(2))
        assert_equals(7, propulsor.generateMove())

    def testCombiningExtraStacksOnTerminatingExtra(self):
        cards = Cards([])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        propulsor.addExtraChoice(CombiningExtraExample(3))
        propulsor.addExtraChoice(TerminatingExtraExample(10))
        assert_equals(13, propulsor.generateMove())

    def testCombiningExtrasAppliedInReverseOrder(self):
        cards = Cards([4, 4, 4, 4])
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(CombiningExtraExample(1))
        propulsor.addExtraChoice(MultiplyingCombining(2))
        # Pick order: Add(1) then Mul(2) then Card(4).
        # Reverse application: Mul first, then Add → (4 * 2) + 1 = 9.
        assert_equals(9, propulsor.generateMove())


class MultiplyingCombining(ExtraChoice):
    def __init__(self, factor):
        self.factor = factor

    def label(self):
        return f"x{self.factor}"

    def isAvailable(self):
        return True

    def isCombining(self):
        return True

    def combine(self, value, propulsor):
        return value * self.factor


class ChoiceDoer():
    def __init__(self, always):
        self.always = always

    def pick(self, possibilities, *_):
        return self.always

if __name__ == "__main__":
    runTests(DeckPropulsorTest())
