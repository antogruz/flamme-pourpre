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
        choices = [CardChoice(c) for c in cards]
        availableExtras = [e for e in self.extras if e.isAvailable()]
        choices = choices + [e for e in availableExtras]
        if not choices:
            return ""
        index = self.pick([c.label() for c in choices], "Play a card")
        choice = choices[index]
        choice.applyTo(self)
        return choice.label()

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

class CardChoice:
    def __init__(self, value):
        self.value = value

    def label(self):
        return self.value

    def isAvailable(self):
        return True

    def applyTo(self, propulsor):
        propulsor.cards.play(self.value)

class ExtraChoice:
    """Interface for non-card choices offered by a DeckPropulsor.

    Extras are registered via DeckPropulsor.addExtraChoice() and appear
    alongside the drawn cards each turn, letting talents propose options
    that don't directly come from the hand (skip the hand, play a card
    with a special effect, trigger a free movement, etc.).

    On each turn, the propulsor first asks each extra if it `isAvailable()`,
    then builds the choice list with `label()`. If the oracle picks the
    extra, `applyTo(propulsor)` runs the effect, and `label()` is read
    again to produce the value returned by `generateMove()` (this value
    is then fed to EnergyRules.energyFromCard()).
    """

    def label(self):
        """Return the display name before pick, and the played value after.

        Called twice per generateMove(): once to populate the choice list
        shown to the oracle, and once after applyTo() to provide the move
        value returned to the engine. Implementations may return a fixed
        text label when the choice has not been picked yet, and switch to
        the actual card value (or "") once applyTo() has decided what is
        actually being played.
        """
        pass

    def isAvailable(self):
        """Return whether this extra should be offered this turn.

        Called once per generateMove(), after the hand has been drawn.
        Use this to gate the choice on remaining uses, hand size, road
        type, or any other condition.
        """
        pass

    def applyTo(self, propulsor):
        """Apply this extra's effect when picked by the oracle.

        Receives the owning DeckPropulsor so the effect can access
        `propulsor.cards` (to play, discard, or otherwise manipulate the
        hand) and `propulsor.oracle` (to ask the player for follow-up
        choices, e.g. which card to actually play).
        """
        pass

    def newRace(self):
        """Reset per-race state at the start of a new race.

        Called by DeckPropulsor.newRace(). Override to reset counters
        such as remaining uses for once-per-race effects.
        """
        pass

class ExtraChoiceExample(ExtraChoice):
    def __init__(self, value):
        self.value = value

    def label(self):
        return self.value

    def isAvailable(self):
        return True

    def applyTo(self, propulsor):
        propulsor.cards.discardHand()

class DeckPropulsorTest:
    def testPlayFirstCard(self):
        cards = Cards([9, 3, "f", 5])
        propulsor = DeckPropulsor(cards, ChoiceDoer(0))
        assert_equals(9, propulsor.generateMove())
        assert_equals(3, propulsor.generateMove())
        assert_equals("f", propulsor.generateMove())
        assert_equals(5, propulsor.generateMove())
        assert_equals("", propulsor.generateMove())

    def testPlayExtra(self):
        cards = Cards([9, 3, "f", 5])
        propulsor = DeckPropulsor(cards, ChoiceDoer(4))
        propulsor.addExtraChoice(ExtraChoiceExample(8))
        assert_equals(8, propulsor.generateMove())

class ChoiceDoer():
    def __init__(self, always):
        self.always = always

    def pick(self, possibilities, *_):
        return self.always

if __name__ == "__main__":
    runTests(DeckPropulsorTest())