#!/usr/bin/env python3

# Orchestrateur UI-agnostique de Flamme Pourpre.
#
# Reçoit une UserInterface déjà initialisée (run() en cours) et pilote la
# séquence : menus initiaux → construction de l'équipe humaine → choix des
# bots → tour de courses. Ne dépend que des interfaces engine/ (Menu,
# UserInterface, DisplayBinder, AnimationBinder).
#
# Le launcher (main/launcher.py) est seul à connaître les implémentations
# concrètes d'UserInterface.

from tour import Tour
from teamBuilder import TeamBuilder
from tracks import randomPresetTrack
from propulsion import SequentialPropulsion
from appearances import Appearances
from specialTour.teamProgression import TalentTeamProgression
from engineRunner import EngineRunner


TEAM_COLOR = "green"
BOT_COLORS = ["blue", "red", "black"]


def run(ui):
    """Orchestre une partie en consommant l'UserInterface fournie.

    Doit être appelé à l'intérieur de ui.run(...) pour que les factories
    (menu, displays, ...) disposent du contexte graphique initialisé."""
    menu = ui.menu()
    gameMode = menu.choose(["Tour", "Special Tour"], "Game mode")
    racesCount = menu.choose(list(range(1, 6)), "How many races to play?")
    ridersCount = menu.choose([1, 2, 3, 4], "How many riders in your team?")

    appearances = Appearances()
    displays = ui.displays(appearances)
    director = ui.playerRidersDirector(ridersCount, displays, appearances)
    oracle = ui.playerOracle(appearances)

    humanTeam = _buildHumanTeam(menu, ridersCount, gameMode, oracle, director)
    botTeams = _buildBotTeams(menu, ui.botsTeamsDirector(appearances))

    tour = Tour([humanTeam] + botTeams)
    tracks = [randomPresetTrack for _ in range(racesCount)]
    animations = ui.animations(displays)
    runner = EngineRunner(displays, animations)
    bonusPerRace = 2 if gameMode == "Special Tour" else 0
    runner.runTour(tour, tracks, bonusPerRace)


def _buildHumanTeam(menu, ridersCount, gameMode, oracle, director):
    tb = TeamBuilder()
    tb.buildOracle(oracle)
    tb.buildPropulsion(SequentialPropulsion(oracle))
    for _ in range(ridersCount):
        riderType = menu.choose(
            ["Rouleur", "Sprinteur", "Grimpeur", "Opportunistic"],
            "Add a rider to your team",
        )
        rider = _makeRider(director, riderType, oracle)
        tb.addRider(rider)
    if gameMode == "Special Tour":
        tb.buildProgression(TalentTeamProgression(tb.riders, oracle))
    return tb.getResult()


def _makeRider(director, riderType, oracle):
    if riderType == "Rouleur":
        return director.makeRouleur(oracle, TEAM_COLOR)
    if riderType == "Sprinteur":
        return director.makeSprinteur(oracle, TEAM_COLOR)
    if riderType == "Grimpeur":
        return director.makeGrimpeur(oracle, TEAM_COLOR)
    if riderType == "Opportunistic":
        return director.makeOpportunistic(oracle, TEAM_COLOR)
    raise ValueError(f"Unknown rider type: {riderType}")


def _buildBotTeams(menu, botsDirector):
    factory = menu.chooseLabeled(
        [
            ("Standard", botsDirector.makeStandardBots),
            ("Dice", botsDirector.makeDiceBots),
            ("Muscle", botsDirector.makeMuscleTeam),
        ],
        "Choose the type of bots",
    )
    return [factory(color) for color in BOT_COLORS]
