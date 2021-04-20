#!/usr/bin/env python3

import tkinter as tk

def displayTrack(window, track):
    widgets = []
    column = 0
    bigRow = 0
    while (track.getRoadType(column) != "out"):
        square = []
        for row in range(2):
            lane = getLabel(window, track.getRoadType(column))
            setGrid(lane, column, row)
            square.append(lane)
        lane = invisible(window)
        setGrid(lane, column, 2)
        square.append(lane)
        widgets.append(square)
        column += 1
    return widgets

maxColumn = 30
def setGrid(label, square, lane):
    corridor = int(square / maxColumn)
    label.grid(row = 3 * corridor + 2 - lane, column = square % maxColumn, padx = 1, pady = 1)

def getLabel(window, roadType):
    if roadType == "start":
        return slot(window, 'goldenrod')

    if roadType == "end":
        return slot(window, 'goldenrod')

    if roadType == "ascent":
        return slot(window, 'red')

    if roadType == "descent":
        return slot(window, 'blue')

    if roadType == "target":
        return slot(window, 'green')

    return slot(window, 'black')

def slot(window, border):
    return tk.Label(window, text = "", highlightthickness = 1, highlightbackground = border, width = 3)

def invisible(window):
    return tk.Label(window, width = 3)

def empty(widget):
    widget.config(text = "", fg = "black")
