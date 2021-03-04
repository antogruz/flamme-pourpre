#!/usr/bin/env python3

import tkinter as tk

def main():
    window = tk.Tk()
    window.title("Tac first window")
    run(window)
    window.mainloop()

def run(window):
    for column in range(60):
        for row in range(2):
            spot = None
            if column == 5:
                spot = rouleur(window)
            else:
                spot = empty(window)
            spot.grid(row = row, column = column)

def empty(window):
    return tk.Label(window, text = "-", relief = "raised")

def rouleur(window):
    return tk.Label(window, text = "R", relief = "raised")

main()



