#!/usr/bin/env python3

import tkinter as tk

class Frames():
    def __init__(self):
        self.count = 0

    def new(self, window):
        result = tk.Frame(window)
        self.count += 1
        result.grid(row = self.count)
        return result

