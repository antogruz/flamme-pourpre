#!/usr/bin/env python3

import tkinter as tk

class RiderDisplay():
    def __init__(self, color, display):
        self.color = color
        self.text = display

    def displayInWidget(self, widget):
        widget.config(text = self.text, fg = self.color)


from riderMove import Rider
class DisplayableRider(Rider, RiderDisplay):
    def __init__(self, shape, color, square, lane):
        Rider.__init__(self, square, lane)
        RiderDisplay.__init__(self, color, shape)

    def display(self, boardWidgets):
        square, lane = self.position()
        self.displayInWidget(boardWidgets[square][lane])


def createRiders():
    riders = []
    riders.append(createRouleur("green", 5, 0))
    riders.append(createRouleur("red", 6, 0))
    riders.append(createRouleur("blue", 4, 0))
    riders.append(createRouleur("black", 5, 1))
    riders.append(createSprinteur("green", 8, 0))
    return riders

def createRouleur(color, square, lane):
    return DisplayableRider("o±ỏ", color, square, lane)

def createSprinteur(color, square, lane):
    return DisplayableRider("o/ỏ", color, square, lane)

