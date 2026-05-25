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
            if hasattr(extra, "newRace"):
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
        propulsor.addExtraChoice(ExtraChoice(8))
        assert_equals(8, propulsor.generateMove())

class ChoiceDoer():
    def __init__(self, always):
        self.always = always

    def pick(self, possibilities, *_):
        return self.always

if __name__ == "__main__":
    runTests(DeckPropulsorTest())