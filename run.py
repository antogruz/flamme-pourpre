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
    def forward():
        rider = riders[4]
        rider.set(rider.square + 1, 1)
        updateDisplay(tracks, riders)

    tk.Button(window, text = "Avance!", command = forward).pack()


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



