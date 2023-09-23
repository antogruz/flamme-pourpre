#!/usr/bin/env python3

# Cette classe est une fusion des différentes interfaces du rider utilisées par toutes les classes et fonctions utilisant un Rider dans le package jeu.
# Elle est un peu lourde et on pourrait sûrement utiliser une autre méthode (merge object?), mais faire l'assemblage ici permet de garder un scope minimal pour chaque "sous-classe" (riderMove, cards, ...)
# On pourrait hériter de classes différentes, et faire ajouter des attributs nécessaires en appelant des fonctions du genre "makeObjectPositionable"

class Rider():
    def __init__(self, name, cards, riderMove):
        self.name = name
        self.cards = cards
        self.riderMove = riderMove

    def draw(self):
        return self.cards.draw()

    def play(self, card):
        self.cards.play(card)
        self.nextMove = getCardValue(card)

    def position(self):
        return self.riderMove.position()

    def move(self, track, obstacles):
        self.riderMove.move(self.nextMove, track, obstacles)
        self.nextMove = None

    def getSlipstream(self, track):
        return self.riderMove.getSlipstream(track)

    def getSquare(self):
        return self.riderMove.position()[0]

    def exhaust(self):
        self.cards.discard.append("f")

def getCardValue(card):
    if card == "f" or card == "":
        return 2
    return extractNumberFrom(card)

import re
def extractNumberFrom(card):
    return int(re.sub("[a-z]||[A-Z]", "", card))


from unittests import *
from player import Player, ChoiceDoer
from cards import Cards
from opportunistic import createOpportunisticCards

class IntegrationTester():
    def testEmptyDeck(self):
        rider = Rider("exhausted", Cards([]), None)
        player = Player(ChoiceDoer([0, 0, 0]), [rider])
        player.pickNextMoves()
        assert_equals(2, rider.nextMove)

    def testOpportunistic(self):
        rider = Rider("Opportunistic", createOpportunisticCards([5], ["magenta"], noop), None)
        player = Player(ChoiceDoer([0, 2]), [rider])
        player.pickNextMoves()
        assert_equals(5, rider.nextMove)

def noop(*_):
    pass

if __name__ == "__main__":
    runTests(IntegrationTester())

