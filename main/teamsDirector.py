from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion
from ridersDirector import RidersDirector
from riderBuilderWithAppearance import RiderBuilderWithAppearance

class TeamsDirector:
    def __init__(self, appearances):
        self.appearances = appearances

    def makeStandardBots(self, color):
        oracle = FirstOracle()
        tb = TeamBuilder()
        tb.buildColor(color)
        tb.buildPropulsion(SimpleTeamPropulsion())
        tb.buildOracle(oracle)
        director = RidersDirector(RiderBuilderWithAppearance(self.appearances))
        tb.addRider(director.makeRouleur(oracle, color))
        tb.addRider(director.makeSprinteur(oracle, color))
        return tb.getResult()

    def makeDiceBots(self, color):
        tb = TeamBuilder()
        tb.buildColor(color)
        tb.buildPropulsion(SimpleTeamPropulsion())
        riderDirector = RidersDirector(RiderBuilderWithAppearance(self.appearances))
        tb.addRider(riderDirector.makeDiceRider(color))
        tb.addRider(riderDirector.makeDiceSprinteur(color))
        return tb.getResult()

    def makeMuscleTeam(self, color):
        tb = TeamBuilder()
        tb.buildColor(color)
        tb.buildPropulsion(SimpleTeamPropulsion())
        riderDirector = RidersDirector(RiderBuilderWithAppearance(self.appearances))
        tb.addRider(riderDirector.makeMuscleRouleur(color))
        tb.addRider(riderDirector.makeMuscleSprinteur(color))
        return tb.getResult()

class FirstOracle():
    def pick(self, *_):
        return 0

    def pickRider(self, *_):
        return 0