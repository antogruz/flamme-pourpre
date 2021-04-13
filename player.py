#!/usr/bin/env python3

from unittests import Tester, assert_equals, assert_similars

def tests():
    PlayerTest().runTests()

class PlayerTest(Tester):
    def testChoiceBetweenRiders(self):
        choices = ChoiceLogger()
        p = Player(choices, [createRouleur(), createSprinteur()])
        p.pickNextMoves()
        assert_similars(["Rouleur", "Sprinteur"], choices.get(0))

    def testSelectRiderCard(self):
        choices = ChoiceLogger()
        p = Player(choices, [createRouleur()])
        p.pickNextMoves()
        assert_similars(["Rouleur"], choices.get(0))
        assert_similars([3, 4, 6, 7], choices.get(1))

    def testNextMovesSelected(self):
        choices = ChoiceDoer([0, 3, 0, 2])
        rouleur = createRouleur()
        sprinteur = createSprinteur()
        p = Player(choices, [rouleur, sprinteur])
        p.pickNextMoves()
        assert_equals(6, rouleur.nextMove)
        assert_equals(4, sprinteur.nextMove)


    #Test default if invalid choice

class ChoiceLogger():
    def __init__(self):
        self.choices = []

    def pick(self, possibilities):
        self.choices.append(possibilities)
        return 0

    def get(self, n):
        return self.choices[n]

class ChoiceDoer():
    def __init__(self, future):
        self.future = future

    def pick(self, possibilities):
        return self.future.pop(0)

class Rider():
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    def draw(self):
        return self.cards

    def play(self, card):
        self.nextMove = card

def createRouleur():
    return Rider("Rouleur", [3, 4, 7, 6])

def createSprinteur():
    return Rider("Sprinteur", [2, 9, 4, 5])

class Player():
    def __init__(self, oracle, riders):
        self.oracle = oracle
        self.riders = riders

    def pickNextMoves(self):
        ridersToPick = self.riders
        while (ridersToPick):
            self.pickOneMove(ridersToPick)

    def pickOneMove(self, riders):
        choice = self.oracle.pick([r.name for r in riders])
        rider = riders.pop(choice)

        cards = rider.draw()
        choice = self.oracle.pick(cards)
        rider.play(cards[choice])


if __name__ == "__main__":
    tests()
