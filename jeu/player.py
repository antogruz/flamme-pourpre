#!/usr/bin/env python3

from unittests import runTests, assert_equals, assert_similars

def tests():
    runTests(PlayerTest())

class PlayerTest():
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


    def testDefaultIfInvalidChoice(self):
        choices = ChoiceDoer([-1, 9999])
        rouleur = createRouleur()
        p = Player(choices, [rouleur])
        p.pickNextMoves()
        assert_equals(3, rouleur.nextMove)

    def testNoCardsLeftMeans2(self):
        rider = Rider("exhausted", [])
        Player(ChoiceDoer([0, 0, 0]), [rider]).pickNextMoves()
        assert_equals(2, rider.nextMove)

    def testSeveralChoices(self):
        choices = ChoiceDoer([0, 3, 0, 2])
        rider = createRouleur()
        p = Player(choices, [rider])
        p.pickNextMoves()
        p.pickNextMoves()
        assert_equals(7, rider.nextMove)


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
        ridersToPick = [r for r in self.riders]
        while (ridersToPick):
            self.pickOneMove(ridersToPick)

    def pickOneMove(self, riders):
        rider = self.pickRider(riders)
        rider.play(self.pickCard(rider))

    def pickRider(self, riders):
        choice = self.pick([r.name for r in riders])
        return riders.pop(choice)

    def pickCard(self, rider):
        cards = rider.draw()
        if not cards:
            return 2
        return cards[self.pick(cards)]

    def pick(self, list):
        choice = self.oracle.pick(list)
        if choice < 0 or choice >= len(list):
            return 0
        return choice


if __name__ == "__main__":
    tests()
