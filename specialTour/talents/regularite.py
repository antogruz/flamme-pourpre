from talent import Talent
from jeu.cards import SimpleCard

class Regularite(Talent):
    def applyTo(self, personnage):
        deck = personnage.propulsor.cards.deck
        nine = next(c for c in deck if c.label() == "9")
        deck.remove(nine)
        deck.extend([SimpleCard(6), SimpleCard(6), SimpleCard(6)])

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
        deck = personnage.propulsor.cards.deck
        assert_equals(3, countLabel(deck, "6"))
        assert_equals(2, countLabel(deck, "9"))

def countLabel(cards, label):
    return sum(1 for c in cards if c.label() == label)

if __name__ == "__main__":
    runTests(RegulariteTest())
