#!/usr/bin/env python3

# Point d'entrée de Flamme Pourpre.
#
# Choisit l'UI selon --ui (par défaut "tk"), instancie le UserInterface
# correspondant, puis délègue à main/main.py qui orchestre la partie.
#
# C'est le SEUL fichier qui connaît la liste des UI disponibles.
# Pour ajouter une UI, l'ajouter dans UIS et la mettre dans son propre
# dossier (cf. homeMadeUI/ pour l'UI Tk).
#
# Les factories acceptent un kwarg `fast` (booléen) : si True, l'UI doit
# tourner au plus vite (utile pour integrationTests). Chaque UI choisit
# ce que ça veut dire pour elle (Tk : clock d'animation réduit).

import argparse

import main as orchestrator


def _tkUserInterface(fast = False):
    from tkUserInterface import TkUserInterface, FAST_CLOCK, DEFAULT_CLOCK
    return TkUserInterface(clock = FAST_CLOCK if fast else DEFAULT_CLOCK)


UIS = {
    "tk": _tkUserInterface,
}


def main():
    parser = argparse.ArgumentParser(description="Flamme Pourpre")
    parser.add_argument("--ui", default="tk", choices=sorted(UIS.keys()),
                        help="UI à utiliser")
    args = parser.parse_args()

    ui = UIS[args.ui]()
    ui.run(lambda: orchestrator.run(ui))


if __name__ == "__main__":
    main()
