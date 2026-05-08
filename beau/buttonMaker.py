#!/usr/bin/env python3

import tkinter as tk


def makeButton(label, onClick):
    label.pressed = False
    label.armed = False

    def onPress(e):
        e.widget.pressed = True
        e.widget.armed = True
        e.widget.config(relief = "sunken")

    def onLeave(e):
        if e.widget.pressed:
            e.widget.armed = False
            e.widget.config(relief = "raised")

    def onEnter(e):
        if e.widget.pressed:
            e.widget.armed = True
            e.widget.config(relief = "sunken")

    def onRelease(e):
        fired = e.widget.armed
        e.widget.pressed = False
        e.widget.armed = False
        e.widget.config(relief = "raised")
        if fired:
            onClick()

    label.bind("<ButtonPress-1>", onPress)
    label.bind("<Leave>", onLeave)
    label.bind("<Enter>", onEnter)
    label.bind("<ButtonRelease-1>", onRelease)
