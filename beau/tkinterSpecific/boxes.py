#! /usr/bin/env python3

import tkinter as tk

class Box:
    
    def __init__(self, border_frame, content_label):
        self.border_frame = border_frame
        self.content_label = content_label
        self.defaultBackground = content_label.cget('bg')

    def setContent(self, content, color):
        self.content_label.config(text=content, fg=color)

    def setBackground(self, color):
        if color == "default":
            color = self.defaultBackground
        self.content_label.config(bg=color)

    def clear(self):
        self.content_label.config(text="", fg="black", bg=self.defaultBackground)

    def setBorder(self, color, thickness=1):
        self.border_frame.config(bg=color)


class BoxFactory:

    def __init__(self, frame):
        self.frame = frame
        self.maxColumn = 30

    def getBox(self, row, column):
        width = 40
        height = 20
        border_frame = tk.Frame(self.frame, width=width, height=height)
        border_frame.pack_propagate(False) # prevent the frame from being resized
        content_label = tk.Label(border_frame, width=width - 2)
        content_label.place(x=1, y=1, width=width - 2, height=height - 2) # place the content label in the center of the frame
        grid_row = 4 * (column // self.maxColumn) + 3 - row
        grid_column = column % self.maxColumn
        border_frame.grid(row=grid_row, column=grid_column, padx=1, pady=1)
        return Box(border_frame, content_label)

def buildBoxFactory(frame):
    return BoxFactory(frame)