#!/usr/bin/env python3

import tkinter

def allWidgets():
    window = tkinter.Tk()
    window.title("Tac first window")
    frame = tkinter.Frame(window)
    label = tkinter.Label(window, text = "Bienvenue chez moi !").pack()
    button = tkinter.Button(frame, text = "Ne clique pas !").pack()
    canvas = tkinter.Canvas(window).pack()
    check = tkinter.Checkbutton(window).pack()
    entry = tkinter.Entry(frame).pack()
    frame.pack()
    window.mainloop()

def frames():
    window = tkinter.Tk()
