from talent import Talent

class Regularite(Talent):
    def applyTo(self, personnage):
        personnage.propulsor.cards.deck.remove(9)
        personnage.propulsor.cards.deck.append(6)
        personnage.propulsor.cards.deck.append(6)
        personnage.propulsor.cards.deck.append(6)

    def displayRule(self):
        return "Regularité: Transformez un 9 en trois 6"

from unittests import assert_equals, runTests
from jeu.riderBuilder import RiderBuilder

class RegulariteTest:
    def testRegularite(self):
        rb = RiderBuilder()
        rb.buildDeck([2, 3, 4, 5, 9] * 3)
        personnage = rb.getResult()
        personnage.gainTalent(Regularite())
        assert_equals(3, personnage.propulsor.cards.deck.count(6))
        assert_equals(2, personnage.propulsor.cards.deck.count(9))

if __name__ == "__main__":
    runTests(RegulariteTest())