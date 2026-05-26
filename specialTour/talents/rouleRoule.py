from talent import Talent
from jeu.cards import SimpleCard

class RouleRoule(Talent):
    def applyTo(self, personnage):
        personnage.propulsor.cards.deck.append(SimpleCard(7))

    def displayRule(self):
        return "Roule, Roule: Ajoutez une carte 7 à votre deck de départ"

from unittests import assert_equals, runTests
from jeu.riderBuilder import RiderBuilder

class RouleRouleTest:
    def testRouleRouleAdds7ToDeck(self):
        rb = RiderBuilder()
        rb.buildDeck([3, 4, 5, 6, 7] * 3)
        personnage = rb.getResult()
        personnage.gainTalent(RouleRoule())
        assert_equals(4, sum(1 for c in personnage.propulsor.cards.deck if c.label() == "7"))

if __name__ == "__main__":
    runTests(RouleRouleTest())
