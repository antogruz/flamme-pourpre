#!/usr/bin/env python3

from unittests import runTests, assert_equals


class EnergyRules:
    """Interface for converting a played Card into consumable energy.

    A turn yields a list of Cards (see `DeckPropulsor.generateMoves`).
    `Race.energyOf` calls `energyFromMove` on each Card in the list and
    sums the results. The default implementation simply returns
    `card.energy()`. Talents may decorate it (Effort Long, Économie
    d'Énergie, Super Sprint, etc.) by wrapping the rider's `energyRules`.
    """
    def energyFromMove(self, card):
        """Return the energy yielded by `card` for the rider."""
        return card.energy()


class BonusRule:
    """Interface for bonus energy rules attached to a personnage.

    Implement this to add extra energy on top of the cards' base
    energies, typically based on the race snapshot (group position,
    escape, sprint phase, etc.). Bonuses from all rules attached to a
    rider are summed.
    """
    def bonusFor(self, moves, rider, snapshot):
        """Return the bonus energy granted to `rider` for playing `moves`.

        `moves` is the list of Cards played this turn.
        """
        pass


class EnergyRulesTest:
    def __before__(self):
        self.rules = EnergyRules()

    def testNumberCard(self):
        assert_equals(9, self.rules.energyFromMove(StubCard("9", 9)))

    def testFatigueLikeMove(self):
        assert_equals(2, self.rules.energyFromMove(StubCard("f", 2)))

    def testEmptyMove(self):
        assert_equals(2, self.rules.energyFromMove(StubCard("", 2)))


class StubCard:
    def __init__(self, label, energy):
        self._label = label
        self._energy = energy

    def label(self):
        return self._label

    def energy(self):
        return self._energy


if __name__ == "__main__":
    runTests(EnergyRulesTest())
