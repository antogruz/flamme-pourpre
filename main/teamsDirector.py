from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion
from ridersDirector import RidersDirector
from tkRidersDirector import TkRidersDirector
from riderBuilderWithAppearance import RiderBuilderWithAppearance
from oracle import DefaultOracle

class TeamsDirector:
    def __init__(self, appearances):
        self.appearances = appearances

    def makeStandardBots(self, color):
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        director = self._makeDirector()
        tb.addRider(director.makeRouleur(DefaultOracle(), color))
        tb.addRider(director.makeSprinteur(DefaultOracle(), color))
        return tb.getResult()

    def makeDiceBots(self, color):
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        director = self._makeDirector()
        tb.addRider(director.makeDiceRider(color))
        tb.addRider(director.makeDiceSprinteur(color))
        return tb.getResult()

    def makeMuscleTeam(self, color):
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        director = self._makeDirector()
        tb.addRider(director.makeMuscleRouleur(color))
        tb.addRider(director.makeMuscleSprinteur(color))
        return tb.getResult()

    def _makeDirector(self):
        return TkRidersDirector(RidersDirector(RiderBuilderWithAppearance(self.appearances)), self.appearances)
