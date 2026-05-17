from talent import Talent

class SprintFinal(Talent):
    def applyTo(self, personnage):
        personnage.addBonusRule(SprintFinalBonus())
    
    def displayRule(self):
        return "Sprint Final: Si vous avez 3 cartes ou moins dans votre deck, ajoutez 2 à votre carte jouée. Si vous avez 7 cartes ou moins dans votre deck, ajoutez 1 à votre carte jouée."

class SprintFinalBonus:
    def bonusFor(self, card, rider, snapshot):
        if rider.personnage.propulsor.cards.cardsLeft() <= 4:
            return 2
        if rider.personnage.propulsor.cards.cardsLeft() <= 8:
            return 1
        return 0
