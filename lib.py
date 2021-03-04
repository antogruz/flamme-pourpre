#!/usr/bin/env python3

import tkinter as tk
import colors

def main():
    window = tk.Tk()
    window.title("Library")
    frames = Frames()
    reliefs(frames.new(window))
    showColors(frames.new(window))
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

class Frames():
    def __init__(self):
        self.count = 0

    def new(self, window):
        result = tk.Frame(window)
        self.count += 1
        result.grid(row = self.count)
        return result

main()


