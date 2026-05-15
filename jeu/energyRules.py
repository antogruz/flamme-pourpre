#!/usr/bin/env python3

import re
from unittests import runTests, assert_equals

# Convertit la carte jouée par un coureur en énergie consommable par MovementRules.
# Une instance par coureur : permet à certains coureurs d'avoir des règles spécifiques
# (fatigue à 3, carte peloton dépendant des alliés, etc.) en sous-classant.

class EnergyRules:
    """Interface for converting a played card into consumable energy.

    The default implementation returns the numeric value of the card
    (2 for fatigue or empty hand). Talents may decorate it (Effort Long,
    Économie d'Énergie, etc.) by wrapping the rider's `energyRules`.
    """
    def energyFromCard(self, card):
        """Return the energy yielded by `card` for the rider."""
        if card == "" or card == "f":
            return 2
        return extractNumberFrom(card)

def extractNumberFrom(card):
    return int(re.sub("[a-z]||[A-Z]", "", str(card)))


class BonusRule:
    """Interface for bonus energy rules attached to a personnage.

    Implement this to add extra energy on top of the card's base value,
    typically based on the race snapshot (group position, escape, sprint phase, etc.).
    Bonuses from all rules attached to a rider are summed.
    """
    def bonusFor(self, card, rider, snapshot):
        """Return the bonus energy granted to `rider` for playing `card`."""
        pass


class EnergyRulesTest:
    def __before__(self):
        self.rules = EnergyRules()

    def testNumberCard(self):
        assert_equals(9, self.rules.energyFromCard(9))

    def testColoredNumberCard(self):
        assert_equals(5, self.rules.energyFromCard("5magenta"))

    def testFatigue(self):
        assert_equals(2, self.rules.energyFromCard("f"))

    def testNoCard(self):
        assert_equals(2, self.rules.energyFromCard(""))


if __name__ == "__main__":
    runTests(EnergyRulesTest())
