from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion
from ridersDirector import RidersDirector

class TeamsDirector:
    def makeStandardBots(self, color):
        oracle = FirstOracle()
        tb = TeamBuilder()
        tb.buildColor(color)
        tb.buildPropulsion(SimpleTeamPropulsion())
        tb.buildOracle(oracle)
        director = RidersDirector()
        tb.addRider(director.makeRouleur(oracle))
        tb.addRider(director.makeSprinteur(oracle))
        return tb.getResult()

    def makeDiceBots(self, color):
        tb = TeamBuilder()
        tb.buildColor(color)
        tb.buildPropulsion(SimpleTeamPropulsion())
        riderDirector = RidersDirector()
        tb.addRider(riderDirector.makeDiceRider())
        tb.addRider(riderDirector.makeDiceSprinteur())
        return tb.getResult()

class FirstOracle():
    def pick(self, *_):
        return 0