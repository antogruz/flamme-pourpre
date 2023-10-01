#!/usr/bin/env python3
from beautifulCard import createBeautifulCard
from cardsDisplay import smallCard, bigCard

class OpportunisticDisplay:
    def __init__(self, window, sets, cards):
        self.sets = sets
        self.window = window
        self.labels = self.createLabels()
        self.cards = cards

    def update(self):
        for line, set in zip(self.labels, self.sets):
            for square, card in zip(line, set):
                if card not in self.cards.deck + self.cards.discard:
                    square.config(bg = "black")
                else:
                    square.config(bg = "white")

    def createLabels(self):
        labels = []
        for line, set in enumerate(self.sets):
            lineLabels = []
            for column, card in enumerate(set):
                label = bigCard(self.window, createBeautifulCard(card))
                label.grid(row = line, column = column, padx = 1, pady = 1)
                lineLabels.append(label)
            labels.append(lineLabels)
        return labels


from visualtests import VisualTester, runVisualTestsInWindow
class OpportunisticTester(VisualTester):
    def testAllCardsDisplay(self):
        sets = make2Sets()
        cards = Cards(sets[0], sets[1], [])
        display = OpportunisticDisplay(self.frame, sets, cards)
        display.update()

    def testMissingAndPlayedCards(self):
        sets = make2Sets()
        cards = Cards(sets[0][0:3], sets[1][1:4], ["9magenta"])
        display = OpportunisticDisplay(self.frame, sets, cards)
        display.update()

def make2Sets():
        return [[str(number) + color for number in [ 2, 3, 4, 5, 9 ]] for color in ["magenta", "blue"]]


class Cards:
    def __init__(self, deck, discard, played):
        self.deck = deck
        self.discard = discard
        self.played = played


if __name__ == "__main__":
    runVisualTestsInWindow(OpportunisticTester)
