#!/usr/bin/env python3

# Display des talents gagnés par un coureur.
# Lit dynamiquement personnage.talents à chaque update, donc les talents
# acquis en cours de tour (SpecialTour) apparaissent automatiquement.
# Chaque talent implémente l'interface jeu.talent.Talent : displayRule()
# (description statique) et stats() (liste de strings dynamiques, optionnelle).

import tkinter as tk
from frames import clear


class TalentsDisplay:
    def __init__(self, frame, personnage):
        self.frame = frame
        self.personnage = personnage

    def update(self):
        clear(self.frame)
        for talent in self.personnage.talents:
            block = tk.Frame(self.frame, relief = "ridge", borderwidth = 1, padx = 4, pady = 4)
            block.pack(anchor = "w", fill = "x", pady = 2)
            tk.Label(block, text = talent.displayRule(), wraplength = 300, justify = "left").pack(anchor = "w")
            for stat in talent.stats():
                tk.Label(block, text = stat, fg = "gray30").pack(anchor = "w")


from visualtests import VisualTester, runVisualTestsInWindow
from talent import Talent

class TalentsDisplayTester(VisualTester):
    def testNoTalents(self):
        display = TalentsDisplay(self.frame, FakePersonnage([]))
        display.update()

    def testSingleTalentWithoutStats(self):
        personnage = FakePersonnage([
            FakeTalent("Roule, Roule: Ajoutez une carte 7 à votre deck de départ"),
        ])
        display = TalentsDisplay(self.frame, personnage)
        display.update()

    def testSeveralTalentsWithAndWithoutStats(self):
        personnage = FakePersonnage([
            FakeTalent("Roule, Roule: Ajoutez une carte 7 à votre deck de départ"),
            FakeTalent(
                "Endurance à la fatigue: Quête. Jouer des cartes fatigue.",
                stats = ["Fatigues jouées: 5"],
            ),
            FakeTalent(
                "Récupération active: si on avance du minimum en ravitaillement ou en descente, on peut augmenter de 1 une carte de sa main.",
                stats = ["Cartes boostées: 2", "Dernière: 4 → 5"],
            ),
        ])
        display = TalentsDisplay(self.frame, personnage)
        display.update()

    def testTalentsAddedDynamicallyAreShownAfterUpdate(self):
        personnage = FakePersonnage([FakeTalent("Premier talent")])
        display = TalentsDisplay(self.frame, personnage)
        display.update()
        personnage.talents.append(FakeTalent("Second talent acquis plus tard", stats = ["Stat dynamique: ok"]))
        display.update()


class FakePersonnage:
    def __init__(self, talents):
        self.talents = talents


class FakeTalent(Talent):
    def __init__(self, rule, stats = []):
        self.rule = rule
        self._stats = stats

    def displayRule(self):
        return self.rule

    def stats(self):
        return self._stats


if __name__ == "__main__":
    runVisualTestsInWindow(TalentsDisplayTester)
