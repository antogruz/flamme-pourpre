#!/usr/bin/env python3

import tkinter as tk

def main():
    window = tk.Tk()
    window.title("flamme rouge")
    run(window)
    window.mainloop()

def run(window):
    trackWidgets = createTrack(window)
    addRiders(trackWidgets)

def addRiders(widgets):
    addRouleur(widgets[5][1], "green")
    addRouleur(widgets[6][1], "red")
    addRouleur(widgets[4][1], "blue")
    addRouleur(widgets[5][0], "black")
    addSprinteur(widgets[8][1], "green")

def createTrack(window):
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

def addRouleur(widget, color):
    widget.config(text = "o±ỏ", fg = color)

def addSprinteur(widget, color):
    widget.config(text = "o/ỏ", fg = color)

main()



