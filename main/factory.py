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
    def __init__(self, rootWindow, userFrame):
        self.rootWindow = rootWindow
        self.userFrame = userFrame

    def createTeam(self, color, specialists):
        team = Team(color, [kind.createRider([]) for kind in specialists])
        player = self.createPlayer(team)
        team.player = player
        return team

    def createPlayer(self, team):
        oracle = UserChoice(self.userFrame)
        def onExit(oracle):
            oracle.dontWait()
            self.rootWindow.destroy()
        self.rootWindow.protocol("WM_DELETE_WINDOW", partial(onExit, oracle))
        return Player(oracle, team.riders, [CardDecorator()])

    def createSpecialDisplays(self, specialists, specialFrames):
        return [ s.createSpecialDisplay(f) for (s, f) in zip(specialists, specialFrames) ]


class Bot:
    def createTeam(self, color, specialists = classicDuo()):
        team = Team(color, [kind.createRider([ExhaustRecovery(0.5)]) for kind in specialists])
        player = self.createPlayer(team)
        team.player = player
        return team

    def createPlayer(self, team):
        return Player(FirstOracle(), team.riders, [CardDecorator()])


class FirstOracle():
    def pick(self, *_):
        return 0

