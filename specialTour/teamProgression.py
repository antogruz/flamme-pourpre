#!/usr/bin/env python3

# TalentTeamProgression : progression appliquée aux équipes du joueur entre
# deux courses du SpecialTour. Tire des talents équitablement parmi les
# coureurs éligibles, puis demande à un oracle de choisir lequel acquérir.
# L'interface TeamProgression vit dans jeu/team.py (default no-op pour les bots).

from team import TeamProgression
from specialTour.talentDraw import drawTalents


class TalentTeamProgression(TeamProgression):
    def __init__(self, riders, oracle):
        self.riders = riders
        self.oracle = oracle

    def progress(self):
        eligibles = [r for r in self.riders if r.profile is not None]
        choices = drawTalents(eligibles)
        if not choices:
            return
        instantiated = [(personnage, talentClass()) for (personnage, talentClass) in choices]
        index = self.oracle.pick(
            [talent.displayRule() for (_, talent) in instantiated],
            "Choisissez un talent",
        )
        personnage, talent = instantiated[index]
        personnage.gainTalent(talent)
        personnage.profile.nextTier()
