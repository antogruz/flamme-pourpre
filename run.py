#!/usr/bin/env python3

import tkinter as tk
from track import createTrack, empty
from frames import Frames
from riders import createRiders, setPositions

def main():
    window = tk.Tk()
    window.title("flamme rouge")
    riders = createRiders()
    frames = Frames()
    tracks = track(frames.new(window), riders)
    buttons(tracks, frames.new(window), riders)
    window.mainloop()


def track(window, riders):
    trackWidgets = createTrack(window)
    setPositions(riders)
    displayRiders(trackWidgets, riders)
    return trackWidgets


def buttons(tracks, window, riders):
    def forward(n):
        rider = riders[4]
        rider.set(rider.square + n, 1)
        updateDisplay(tracks, riders)

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


def updateDisplay(tracks, riders):
    removeTokens(tracks)
    displayRiders(tracks, riders)


def removeTokens(tracks):
    for square in tracks:
        for lane in square:
            empty(lane)


def displayRiders(track, riders):
    for rider in riders:
        rider.display(track[rider.square][rider.lane])

main()



