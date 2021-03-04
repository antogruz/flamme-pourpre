#!/usr/bin/env python3

import tkinter as tk

def main():
    window = tk.Tk()
    window.title("flamme rouge")
    run(window)
    window.mainloop()

def run(window):
    for column in range(60):
        for row in range(2):
            spot = None
            if column <= 4:
                spot = start(window)
            elif column >= 13 and column < 19:
                spot = mountain(window)
            elif column >= 19 and column < 23:
                spot = descent(window)
            elif column >= 55:
                spot = end(window)
            else:
                spot = slot(window)

            if column == 5 and row == 1:
                addRouleur(spot, "green")
            spot.grid(row = row, column = column, padx = 1, pady = 1)

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

main()



