#!/usr/bin/env python3

import tkinter as tk

def main():
    window = tk.Tk()
    window.title("Tac first window")
    allWidgets(window)
    frames(window)
    window.mainloop()

def allWidgets(window):
    frame = tk.Frame(window)
    label = tk.Label(window, text = "Bienvenue chez moi !").pack()
    button = tk.Button(frame, text = "Ne clique pas !").pack()
    canvas = tk.Canvas(window).pack()
    check = tk.Checkbutton(window).pack()
    entry = tk.Entry(frame).pack()
    frame.pack()

def frames(window):
    top = tk.Frame(window).pack()
    bot = tk.Frame(window).pack(side = "bottom")
    riders = []
    for name in ["rouleur", "sprinteur"]:
        riders.append(tk.Button(top, text = name, fg = "green").pack())

    cards = []
    for i in range(2, 6):
        cards.append(tk.Button(bot, text = str(i), bg = "green").pack(side = "left"))



main()
