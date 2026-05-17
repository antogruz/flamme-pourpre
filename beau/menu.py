#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
import tkinter as tk
from frames import clear

def createSimpleMenu(frame, choices, title = ""):
    optionsSelector = UserChoice(frame)
    i = optionsSelector.pick(choices, title)
    return choices[i]

def createMenu(frame, choices, title = ""):
    optionsSelector = UserChoice(frame)
    i = optionsSelector.pick([c[0] for c in choices], title)
    return choices[i][1]


from beautifulCard import createBeautifulCard
from buttonMaker import makeButton

class UserChoice():
    def __init__(self, frame, appearances = None):
        self.frame = frame
        self.appearances = appearances
        self.answer = tk.IntVar()

    def pickRider(self, riders, instruction = ""):
        return self.pickWithRiders([(r, "") for r in riders], instruction)

    def pick(self, choices, title = ""):
        if title:
            tk.Label(self.frame, text = title).pack()

        for i, choice in enumerate(choices):
            card = createBeautifulCard(choice)
            label = tk.Label(self.frame, text = card.text,
                     fg = card.color, bg = card.background,
                     padx = 10, pady = 5,
                     relief = "raised", borderwidth = 2)
            makeButton(label, lambda n = i: self.answer.set(n))
            label.pack(side = "left")

        self.frame.update()
        self.frame.wait_variable(self.answer)

        clear(self.frame)
        return self.answer.get()

    def pickWithRiders(self, choices, instruction = ""):
        return self.pick([self.nicePrefix(rider) + " - " + choice for rider, choice in choices], instruction)

    def nicePrefix(self, rider):
        appearance = self.appearances.of(rider)
        return appearance.name + " " + appearance.shade

    def niceChoice(self, rider, choice):
        if not choice:
            return self.nicePrefix(rider)
        return self.nicePrefix(rider) + " - " + choice


    def dontWait(self):
        self.answer.set(-1)


class MenuTester(VisualTester):
    def testSimpleMenu(self):
        choice = createSimpleMenu(self.frame, ["Un choix", "Un autre", "Un dernier pour la route"], "Quel choix faire ?")
        tk.Label(self.frame, text = choice).pack()

    def testSimpleColors(self):
        choice = createSimpleMenu(self.frame, ["3green", "5magenta", "5goldenrod", "f"])
        tk.Label(self.frame, text = choice).pack()

    def testMenu(self):
        choice = createMenu(self.frame, [("Un choix", "A"), ("Un autre", "B"), ("Un dernier pour la route", "C")])
        tk.Label(self.frame, text = choice).pack()


if __name__ == "__main__":
    runVisualTestsInWindow(MenuTester)
