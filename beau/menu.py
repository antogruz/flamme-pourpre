#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
import tkinter as tk
from frames import clear

def createSimpleMenu(frame, choices):
    optionsSelector = UserChoice(frame)
    i = optionsSelector.pick(choices)
    return choices[i]

def createMenu(frame, choices):
    optionsSelector = UserChoice(frame)
    i = optionsSelector.pick([c[0] for c in choices])
    return choices[i][1]


from functools import partial
class UserChoice():
    def __init__(self, frame):
        self.frame = frame
        self.answer = tk.IntVar()

    def pick(self, choices):
        def setChoice(n):
            self.answer.set(n)

        for i, choice in enumerate(choices):
            tk.Button(self.frame, text = choice, command = partial(setChoice, i)).pack(side = "left")

        self.frame.update()
        self.frame.wait_variable(self.answer)

        clear(self.frame)
        return self.answer.get()

    def dontWait(self):
        self.answer.set(-1)


class MenuTester(VisualTester):
    def testSimpleMenu(self):
        choice = createSimpleMenu(self.frame, ["Un choix", "Un autre", "Un dernier pour la route"])
        tk.Label(self.frame, text = choice).pack()

    def testMenu(self):
        choice = createMenu(self.frame, [("Un choix", "A"), ("Un autre", "B"), ("Un dernier pour la route", "C")])
        tk.Label(self.frame, text = choice).pack()


if __name__ == "__main__":
    runVisualTestsInWindow(MenuTester)
