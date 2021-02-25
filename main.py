#!/usr/bin/env python3

import tkinter as tk

def allWidgets():
    window = tk.Tk()
    window.title("Tac first window")
    frame = tk.Frame(window)
    label = tk.Label(window, text = "Bienvenue chez moi !").pack()
    button = tk.Button(frame, text = "Ne clique pas !").pack()
    canvas = tk.Canvas(window).pack()
    check = tk.Checkbutton(window).pack()
    entry = tk.Entry(frame).pack()
    frame.pack()
    window.mainloop()

allWidgets()
