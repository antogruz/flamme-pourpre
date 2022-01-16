#!/usr/bin/env python3

import tkinter as tk
import colors
from frames import Frames

def main():
    window = tk.Tk()
    window.title("Library")
    frames = Frames(window)
    reliefs(frames.new())
    showColors(frames.new())
    window.bind("<space>", lambda e: window.destroy())
    window.mainloop()


def reliefs(window):
    row = 0
    for value in ["sunken", "raised", "groove", "ridge", "flat"]:
        tk.Label(window, text = value, width = 100, relief = value).grid(row=row)
        row += 1


def showColors(window):
    row = 0
    col = 0
    for color in colors.allColors:
        tk.Label(window, text = color, background = color).grid(row = row, column = col, sticky = "ew")
        row += 1
        if (row > 36):
            row = 0
            col += 1

main()


