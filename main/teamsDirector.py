from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion
from ridersDirector import RidersDirector
from riderBuilderWithAppearance import RiderBuilderWithAppearance
from team import DefaultOracle

class TeamsDirector:
    def __init__(self, appearances):
        self.appearances = appearances

    def makeStandardBots(self, color):
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        director = RidersDirector(RiderBuilderWithAppearance(self.appearances))
        tb.addRider(director.makeRouleur(DefaultOracle(), color))
        tb.addRider(director.makeSprinteur(DefaultOracle(), color))
        return tb.getResult()

    def makeDiceBots(self, color):
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        riderDirector = RidersDirector(RiderBuilderWithAppearance(self.appearances))
        tb.addRider(riderDirector.makeDiceRider(color))
        tb.addRider(riderDirector.makeDiceSprinteur(color))
        return tb.getResult()

    def makeMuscleTeam(self, color):
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        riderDirector = RidersDirector(RiderBuilderWithAppearance(self.appearances))
        tb.addRider(riderDirector.makeMuscleRouleur(color))
        tb.addRider(riderDirector.makeMuscleSprinteur(color))
        return tb.getResult()