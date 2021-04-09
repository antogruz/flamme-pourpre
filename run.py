#!/usr/bin/env python3

import tkinter as tk
from trackDisplay import displayTrack, empty
from frames import Frames
from riderDisplay import createRiders
from track import Track
from riders import Riders

def main():
    window = tk.Tk()
    window.title("flamme rouge")
    riders = createRiders()
    track = Track(createTrack())
    frames = Frames()
    boardWidgets = displayBoard(frames.new(window), track, riders)
    buttons(boardWidgets, frames.new(window), track, riders)
    window.mainloop()


def createTrack():
    return [(5, "start"), (8, "normal"), (6, "ascent"), (4, "descent"), (32, "normal"), (5, "end")]

def displayBoard(window, road, riders):
    trackWidgets = displayTrack(window, road)
    displayRiders(trackWidgets, riders)
    return trackWidgets


def buttons(boardWidgets, window, road, riders):
    obstacles = Riders(riders)

    def forward(n):
        rider = riders[2]
        rider.move(n, road, obstacles)
        updateDisplay(boardWidgets, riders)

    def plus1():
        forward(1)
    def plus2():
        forward(2)
    def plus5():
        forward(5)
    def plus9():
        forward(9)

    for i, plus in zip([1, 2, 5, 9], [plus1, plus2, plus5, plus9]):
        tk.Button(window, text = i, command = plus).pack(side = "left")


def updateDisplay(boardWidgets, riders):
    removeTokens(boardWidgets)
    displayRiders(boardWidgets, riders)


def removeTokens(boardWidgets):
    for square in boardWidgets:
        for lane in square:
            empty(lane)


def displayRiders(boardWidgets, riders):
    for rider in riders:
        rider.display(boardWidgets)

main()



