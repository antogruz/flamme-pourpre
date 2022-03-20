#!/usr/bin/env python3

import tkinter as tk

class Frames():
    def __init__(self, window):
        self.row = 0
        self.window = window

    def new(self):
        self.row += 1
        result = tk.Frame(self.window)
        result.grid(row = self.row)
        return result

    def newLine(self, count):
        frame = self.new()
        line = []
        for column in range(count):
            subframe = tk.Frame(frame)
            subframe.grid(row = 0, column = column)
            line.append(subframe)
        return line


def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()
