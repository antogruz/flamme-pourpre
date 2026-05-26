#!/usr/bin/env python3

from unittests import runTests, assert_equals


class Move:
    """Interface for the result of a propulsor's generateMove().

    A Move is what a propulsor produces on each turn; the engine then
    converts it into actual energy through EnergyRules and BonusRule.
    The UI may consume `label()` to display the played card / combined
    choices in animations.

    Implementations: SimpleCard, FatigueCard (cards.py), EmptyCard
    (deckPropulsor.py), and the combining wrappers BoostedCard /
    MultipliedCard (deckPropulsor.py).
    """
    def label(self):
        """Human-readable representation, suitable for animations."""
        pass

    def energy(self):
        """Base energy yielded by this move before bonuses."""
        pass


class EnergyRules:
    """Interface for converting a Move into consumable energy.

    The default implementation simply returns `move.energy()`. Talents may
    decorate it (Effort Long, Économie d'Énergie, Super Sprint, etc.) by
    wrapping the rider's `energyRules`.
    """
    def energyFromMove(self, move):
        """Return the energy yielded by `move` for the rider."""
        return move.energy()


class BonusRule:
    """Interface for bonus energy rules attached to a personnage.

    Implement this to add extra energy on top of the move's base energy,
    typically based on the race snapshot (group position, escape, sprint phase, etc.).
    Bonuses from all rules attached to a rider are summed.
    """
    def bonusFor(self, move, rider, snapshot):
        """Return the bonus energy granted to `rider` for playing `move`."""
        pass


class EnergyRulesTest:
    def __before__(self):
        self.rules = EnergyRules()

    def testNumberCard(self):
        assert_equals(9, self.rules.energyFromMove(StubMove("9", 9)))

    def testFatigueLikeMove(self):
        assert_equals(2, self.rules.energyFromMove(StubMove("f", 2)))

    def testEmptyMove(self):
        assert_equals(2, self.rules.energyFromMove(StubMove("", 2)))


class StubMove(Move):
    def __init__(self, label, energy):
        self._label = label
        self._energy = energy

    def label(self):
        return self._label

    def energy(self):
        return self._energy


if __name__ == "__main__":
    runTests(EnergyRulesTest())
