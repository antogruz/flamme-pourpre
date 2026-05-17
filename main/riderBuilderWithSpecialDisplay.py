#!/usr/bin/env python3

from riderBuilderWithAppearance import RiderBuilderWithAppearance
from beau.cardsDisplay import CardsDisplay
from beau.opportunisticDisplay import OpportunisticDisplay
from beau.decorators.talentsDisplay import TalentsDisplay


class RiderBuilderWithSpecialDisplay(RiderBuilderWithAppearance):
    """
    Builder qui construit un rider et enregistre en plus
    les displays "spéciaux" (cartes en main, set opportuniste, talents...)
    associés à ce rider.
    """

    def __init__(self, displayRegistry, appearances, cardFrame, specialFrame, talentsFrame):
        super().__init__(appearances)
        self.displayRegistry = displayRegistry
        self.cardFrame = cardFrame
        self.specialFrame = specialFrame
        self.talentsFrame = talentsFrame
        self.displayFactories = []

    def buildDeck(self, *args, **kwargs):
        super().buildDeck(*args, **kwargs)
        self.displayFactories.append(CardsDisplayFactory(self.cardFrame))
        self.displayFactories.append(TalentsDisplayFactory(self.talentsFrame))

    def buildOpportunisticDeck(self, baseCards, sets=["goldenrod", "magenta"], *args, **kwargs):
        super().buildOpportunisticDeck(baseCards, sets, *args, **kwargs)
        self.displayFactories.append(CardsDisplayFactory(self.cardFrame))
        self.displayFactories.append(OpportunisticDisplayFactory(self.specialFrame, sets))
        self.displayFactories.append(TalentsDisplayFactory(self.talentsFrame))

    def getResult(self):
        rider = super().getResult()
        for factory in self.displayFactories:
            self.displayRegistry.register(factory.create(rider, self.appearances))
        return rider


class CardsDisplayFactory:
    def __init__(self, cardFrame):
        self.cardFrame = cardFrame

    def create(self, rider, appearances):
        return CardsDisplay(self.cardFrame, rider, appearances)


class OpportunisticDisplayFactory:
    def __init__(self, specialFrame, sets):
        self.specialFrame = specialFrame
        self.sets = sets

    def create(self, rider, appearances):
        sorted_sets = [
            sorted([card for card in rider.propulsor.cards.deck if color in str(card)])
            for color in self.sets
        ]
        return OpportunisticDisplay(self.specialFrame, sorted_sets, rider.propulsor.cards)


class TalentsDisplayFactory:
    def __init__(self, talentsFrame):
        self.talentsFrame = talentsFrame

    def create(self, rider, appearances):
        return TalentsDisplay(self.talentsFrame, rider)
