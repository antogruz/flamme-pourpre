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
    addRiders(trackWidgets)

def addRiders(widgets):
    addRouleur(widgets[5][1], "green")
    addRouleur(widgets[6][1], "red")
    addRouleur(widgets[4][1], "blue")
    addRouleur(widgets[5][0], "black")
    addSprinteur(widgets[8][1], "green")


def addRouleur(widget, color):
    widget.config(text = "o±ỏ", fg = color)

def addSprinteur(widget, color):
    widget.config(text = "o/ỏ", fg = color)

main()



