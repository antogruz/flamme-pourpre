#!/usr/bin/env python3

# Interface complète d'une UI pour Flamme Pourpre.
#
# Une UI = un objet qui sait :
#   - initialiser et tenir une fenêtre/contexte graphique (run);
#   - poser des questions de configuration à l'utilisateur (menu);
#   - construire l'oracle interactif du joueur humain (playerOracle);
#   - construire le DisplayBinder pour les displays "pull" (displays);
#   - construire l'AnimationBinder pour les observers "push" (animations);
#   - construire le director qui sait peupler son layout per-rider
#     (playerRidersDirector);
#   - construire le director qui peuple les bots (botsTeamsDirector).
#
# Le launcher charge UNE UserInterface (selon --ui) et passe la main à
# main/main.py qui orchestre la partie en ne dépendant que de cette
# interface.
#
# Convention de cycle de vie :
#   ui = SomeUserInterface()
#   ui.run(callback)   # initialise le contexte, appelle callback() dedans,
#                      # puis entre dans la boucle finale (mainloop, etc.)
#
# Les autres méthodes (menu, displays, ...) ne sont valides qu'à
# l'intérieur de l'appel à run().


class UserInterface:
    def run(self, mainCallback):
        """Initialise l'UI, exécute mainCallback() dans son contexte, puis
        entre dans la boucle d'événements finale jusqu'à fermeture."""
        pass

    def menu(self):
        """Retourne un Menu pour les choix de configuration."""
        pass

    def playerOracle(self, appearances):
        """Retourne un Oracle interactif pour le joueur humain."""
        pass

    def displays(self, appearances):
        """Retourne un DisplayBinder neuf pour cette partie."""
        pass

    def animations(self, displays):
        """Retourne un AnimationBinder couplé au DisplayBinder donné."""
        pass

    def playerRidersDirector(self, ridersCount, displays, appearances):
        """Retourne UN director capable de construire ridersCount coureurs
        à la chaîne (makeRouleur, makeSprinteur, ...), en branchant pour
        chacun les displays per-rider sur le DisplayBinder fourni."""
        pass

    def botsTeamsDirector(self, appearances):
        """Retourne un TeamsDirector pour fabriquer les équipes de bots."""
        pass
