#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
import tkinter as tk

def createSimpleMenu(frame, choices):
    optionsSelector = PlayerChoice(frame)
    i = optionsSelector.pick(choices)
    return choices[i]

def createMenu(frame, choices):
    optionsSelector = PlayerChoice(frame)
    i = optionsSelector.pick([c[0] for c in choices])
    return choices[i][1]


from functools import partial
class PlayerChoice():
    def __init__(self, frame):
        self.frame = frame

    def pick(self, choices):
        answer = tk.IntVar()
        def setChoice(n):
            answer.set(n)

        for i, choice in enumerate(choices):
            tk.Button(self.frame, text = choice, command = partial(setChoice, i)).pack(side = "left")

        self.frame.update()
        self.frame.wait_variable(answer)

        clear(self.frame)
        return answer.get()

def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

class MenuTester(VisualTester):
    def testSimpleMenu(self):
        choice = createSimpleMenu(self.frame, ["Un choix", "Un autre", "Un dernier pour la route"])
        tk.Label(self.frame, text = choice).pack()

    def testMenu(self):
        choice = createMenu(self.frame, [("Un choix", "A"), ("Un autre", "B"), ("Un dernier pour la route", "C")])
        tk.Label(self.frame, text = choice).pack()


if __name__ == "__main__":
    runVisualTestsInWindow(MenuTester)
