#!/usr/bin/env python3

from jeu.riderBuilder import RiderBuilder
from beau.cardsDisplay import CardsDisplay
from beau.opportunisticDisplay import OpportunisticDisplay


class RiderBuilderWithSpecialDisplay(RiderBuilder):
    """
    Builder qui construit un rider et enregistre en plus
    les displays "spéciaux" (cartes en main, set opportuniste...)
    associés à ce rider.
    """

    def __init__(self, displayRegistry, cardFrame, specialFrame):
        super().__init__()
        self.displayRegistry = displayRegistry
        self.cardFrame = cardFrame
        self.specialFrame = specialFrame
        self.displayFactories = []

    def buildDeck(self, *args, **kwargs):
        super().buildDeck(*args, **kwargs)
        self.displayFactories.append(CardsDisplayFactory(self.cardFrame))

    def buildOpportunisticDeck(self, baseCards, sets=["goldenrod", "magenta"], *args, **kwargs):
        super().buildOpportunisticDeck(baseCards, sets, *args, **kwargs)
        self.displayFactories.append(CardsDisplayFactory(self.cardFrame))
        self.displayFactories.append(OpportunisticDisplayFactory(self.specialFrame, sets))

    def getResult(self):
        rider = super().getResult()
        for factory in self.displayFactories:
            self.displayRegistry.register(factory.create(rider))
        return rider


class CardsDisplayFactory:
    def __init__(self, cardFrame):
        self.cardFrame = cardFrame

    def create(self, rider):
        return CardsDisplay(self.cardFrame, rider)


class OpportunisticDisplayFactory:
    def __init__(self, specialFrame, sets):
        self.specialFrame = specialFrame
        self.sets = sets

    def create(self, rider):
        sorted_sets = [
            sorted([card for card in rider.propulsor.cards.deck if color in str(card)])
            for color in self.sets
        ]
        return OpportunisticDisplay(self.specialFrame, sorted_sets, rider.propulsor.cards)
