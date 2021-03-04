#!/usr/bin/env python3

import tkinter as tk
from track import createTrack

def main():
    window = tk.Tk()
    window.title("flamme rouge")
    run(window)
    window.mainloop()

def run(window):
    trackWidgets = createTrack(window)
    riders = createRiders()
    setPositions(riders)
    displayRiders(trackWidgets, riders)

def displayRiders(track, riders):
    for rider in riders:
        rider.display(track[rider.square][rider.lane])

class Rider():
    def __init__(self, color, display):
        self.color = color
        self.text = display
        self.square = 0
        self.lane = 0

    def display(self, widget):
        widget.config(text = self.text, fg = self.color)

    def set(self, square, lane):
        self.square = square
        self.lane = lane

def createRiders():
    riders = []
    riders.append(createRouleur("green"))
    riders.append(createRouleur("red"))
    riders.append(createRouleur("blue"))
    riders.append(createRouleur("black"))
    riders.append(createSprinteur("green"))
    return riders

def setPositions(riders):
    riders[0].set(5, 1)
    riders[1].set(6, 1)
    riders[2].set(4, 1)
    riders[3].set(5, 0)
    riders[4].set(8, 1)


def createRouleur(color):
    return Rider(color, "o±ỏ")

def createSprinteur(color):
    return Rider(color, "o/ỏ")

main()



