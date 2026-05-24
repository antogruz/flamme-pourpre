#!/usr/bin/env python3

# Implémentation Tk de Menu : wrapper minimal au-dessus de beau.menu
# (createSimpleMenu/createMenu) avec un Frame Tk capturé.

from menu import Menu
from beau.menu import createSimpleMenu, createMenu


class TkMenu(Menu):
    def __init__(self, frame):
        self.frame = frame

    def choose(self, choices, title = ""):
        return createSimpleMenu(self.frame, list(choices), title)

    def chooseLabeled(self, labeledChoices, title = ""):
        return createMenu(self.frame, list(labeledChoices), title)
