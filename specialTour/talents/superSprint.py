from talent import Talent

class SuperSprint(Talent):
    def applyTo(self, personnage):
        personnage.addBonusRule(SuperSprintBonus())

    def displayRule(self):
        return "Super Sprint: Vos 9 font 11"

class SuperSprintBonus:
    def bonusFor(self, card, rider, snapshot):
        if card == 9:
            return 2
        return 0