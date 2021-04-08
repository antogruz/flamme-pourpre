#!/usr/bin/env python3

import tkinter as tk

def displayTrack(window):
    widgets = []
    for column in range(60):
        square = []
        for row in range(2):
            lane = None
            if column <= 4:
                lane = start(window)
            elif column >= 13 and column < 19:
                lane = mountain(window)
            elif column >= 19 and column < 23:
                lane = descent(window)
            elif column >= 55:
                lane = end(window)
            else:
                lane = slot(window)
            lane.grid(row = row, column = column, padx = 1, pady = 1)
            square.append(lane)
        widgets.append(square)
    return widgets

def end(window):
    return start(window)

def start(window):
    return slot(window, 'goldenrod')

def mountain(window):
    return slot(window, 'red')

def descent(window):
    return slot(window, 'blue')

def slot(window, border='black'):
    return tk.Label(window, text = "-", highlightthickness = 1, highlightbackground = border, width = 3)

def empty(widget):
    widget.config(text = "-", fg = "black")
