#!/usr/bin/env python3

import tkinter as tk

class Frames():
    def __init__(self, window):
        self.count = 0
        self.window = window

    def new(self):
        result = tk.Frame(self.window)
        self.count += 1
        result.grid(row = self.count)
        return result

