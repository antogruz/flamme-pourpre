#!/usr/bin/env python3

import tkinter as tk

def main():
    window = tk.Tk()
    window.title("Tac first window")
    login(window)
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


def grid(window):
    for name, i in zip(["Rouleur", "Sprinteur"], [0, 1]):
        a = 0
        tk.Checkbutton(window, text = name, variable = a, onvalue = 1, offvalue = 0).grid(row = i)


def commands(window):
    def addLabel():
        tk.Label(window, text = "Ça vient de sortir!").pack()

    tk.Button(window, text = "C'est quoi flamme écarlate ?", command = addLabel).pack()

def clicks(window):
    def leftClick(e):
        label("À Gauche !")

    def rightClick(e):
        label("À Droite !")

    def middleClick(e):
        label("Au milieu !")

    def label(text):
        tk.Label(window, text = text).pack()

    window.bind("<Button-1>", leftClick)
    window.bind("<Button-2>", middleClick)
    window.bind("<Button-3>", rightClick)

def login(window):
    for field, row in zip(["Username", "Password"], [0, 1]):
        tk.Label(window, text = field).grid(row = row, column = 0)
        tk.Entry(window).grid(row = row, column = 1)
    tk.Checkbutton(window, text = "Keep me logged in").grid(columnspan = 2)



main()
