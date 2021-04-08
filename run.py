#!/usr/bin/env python3

import tkinter as tk
from trackDisplay import displayTrack, empty
from frames import Frames
from riders import createRiders, setPositions
from track import createTrack

def main():
    window = tk.Tk()
    window.title("flamme rouge")
    riders = createRiders()
    frames = Frames()
    track = createTrack()
    boardWidgets = displayBoard(frames.new(window), track, riders)
    buttons(boardWidgets, frames.new(window), riders)
    window.mainloop()


def displayBoard(window, track, riders):
    trackWidgets = displayTrack(window, track)
    setPositions(riders)
    displayRiders(trackWidgets, riders)
    return trackWidgets


def buttons(boardWidgets, window, riders):
    def forward(n):
        rider = riders[4]
        rider.set(rider.square + n, 1)
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


def displayRiders(track, riders):
    for rider in riders:
        rider.display(track[rider.square][rider.lane])

main()



