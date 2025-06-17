#! /usr/bin/env python3

import tkinter as tk

class Box:
    def __init__(self, widget):
        self.widget = widget
        self.defaultBackground = widget.cget('bg')

    def setContent(self, content, color):
        self.widget.config(text = content, fg = color)

    def setBackground(self, color):
        print(color)
        if color == "default":
            color = self.defaultBackground
        self.widget.config(bg = color)

    def clear(self):
        self.widget.config(text = "", fg = "black", bg = self.defaultBackground)

    def setBorder(self, color, thickness=1):
        self.widget.config(highlightthickness=thickness, highlightbackground=color)

class BoxFactory:
    def __init__(self, frame):
        self.frame = frame
        self.maxColumn = 30
    
    def getBox(self, row, column):
        label = tk.Label(self.frame, width = 3)
        label.grid(row = 4 * (column // self.maxColumn) + 3 - row, column = column % self.maxColumn, padx = 1, pady = 1)
        return Box(label)
    