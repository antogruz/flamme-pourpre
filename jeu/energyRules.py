#!/usr/bin/env python3

import re
from unittests import runTests, assert_equals

# Convertit la carte jouée par un coureur en énergie consommable par MovementRules.
# Une instance par coureur : permet à certains coureurs d'avoir des règles spécifiques
# (fatigue à 3, carte peloton dépendant des alliés, etc.) en sous-classant.

class EnergyRules:
    def energyFromCard(self, card):
        if card == "" or card == "f":
            return 2
        return extractNumberFrom(card)

def extractNumberFrom(card):
    return int(re.sub("[a-z]||[A-Z]", "", str(card)))


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
