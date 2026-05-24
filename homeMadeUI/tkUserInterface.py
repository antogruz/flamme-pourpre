#!/usr/bin/env python3

# Implémentation Tk de UserInterface.
#
# Gère le sandwich lifecycle : run(main) crée la root Tk + sa fenêtre
# principale, exécute main() (qui consomme les autres factories), puis
# entre dans mainloop() jusqu'à fermeture.
#
# Les fenêtres secondaires (oracle, layouts per-rider) sont créées
# paresseusement par les factories qui en ont besoin. Aucune contrainte
# d'ordre entre playerOracle() et playerRidersDirector().
#
# self.appearances est l'Appearances Tk-spécifique de cette UI (name +
# shade ASCII + couleur Tk). Partagé en interne entre tous les composants
# (oracle, displays, directors). L'orchestrateur n'y a pas accès — c'est
# un détail d'implémentation de l'UI.

import tkinter as tk
from functools import partial

from userInterface import UserInterface
from appearances import Appearances
from beau.frames import Frames
from beau.menu import UserChoice
from tkMenu import TkMenu
from tkDisplayBinder import TkDisplayBinder
from tkAnimationBinder import TkAnimationBinder
from tkRidersDirector import TkRidersDirector
from teamsDirector import TeamsDirector
from ridersDirector import RidersDirector


DEFAULT_CLOCK = 0.3
FAST_CLOCK = 0.003


class TkUserInterface(UserInterface):
    def __init__(self, clock = DEFAULT_CLOCK):
        self.clock = clock
        self.appearances = Appearances()
        self.root = None
        self.window = None

    def run(self, mainCallback):
        self.root = tk.Tk()
        self.root.title("flamme rouge")
        self.window = tk.Frame(self.root)
        self.window.grid()

        mainCallback()

        self.window.bind("<Escape>", lambda e: self.window.destroy())
        self.window.mainloop()

    def menu(self):
        return TkMenu(self.window)

    def playerOracle(self):
        oracleFrame = tk.Frame(tk.Toplevel(self.root))
        oracleFrame.pack()
        oracle = UserChoice(oracleFrame, self.appearances)
        def onExit(o):
            o.dontWait()
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", partial(onExit, oracle))
        return oracle

    def displays(self):
        return TkDisplayBinder(self.window, self.clock, self.appearances)

    def animations(self, displays):
        return TkAnimationBinder(displays)

    def playerRidersDirector(self, ridersCount, displays):
        layout = _RidersLayout(tk.Toplevel(self.root), ridersCount)
        layouts = list(zip(layout.cards, layout.specials, layout.talents))
        return TkRidersDirector(RidersDirector(), displays, self.appearances, layouts)

    def botsTeamsDirector(self):
        return TeamsDirector(self.appearances)


class _RidersLayout:
    def __init__(self, window, ridersCount):
        frames = Frames(window)
        self.cards = frames.newLine(ridersCount)
        self.specials = frames.newLine(ridersCount)
        self.talents = frames.newLine(ridersCount)
