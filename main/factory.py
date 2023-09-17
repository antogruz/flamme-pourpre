#!/usr/bin/env python3

import tkinter as tk
from player import Player
from animation import CardDecorator
from tour import Tour, Team
from ridersFactory import *
from menu import UserChoice
from functools import partial

def classicDuo():
    return [rouleurSpecialist(), sprinteurSpecialist()]

class Human:
    def __init__(self, rootWindow):
        self.rootWindow = rootWindow

    def createTeam(self, color, specialists = classicDuo()):
        team = Team(color, [self.createRider(kind) for kind in specialists])
        player = self.createPlayer(team)
        team.player = player
        return team

    def createPlayer(self, team):
        frameForChoices = tk.Toplevel(self.rootWindow)
        oracle = UserChoice(frameForChoices)
        def onExit(oracle):
            oracle.dontWait()
            self.rootWindow.destroy()
        self.rootWindow.protocol("WM_DELETE_WINDOW", partial(onExit, oracle))
        return Player(oracle, team.riders, [CardDecorator()])

    def createRider(self, kind):
        return createRider(kind, reshuffleAll)


class Bot:
    def createTeam(self, color, specialists = classicDuo()):
        team = Team(color, [self.createRider(kind) for kind in specialists])
        player = self.createPlayer(team)
        team.player = player
        return team

    def createPlayer(self, team):
        return Player(FirstOracle(), team.riders, [CardDecorator()])

    def createRider(self, kind):
        return createRider(kind, halfRecovery)


class FirstOracle():
    def pick(self, *_):
        return 0
