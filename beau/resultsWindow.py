#!/usr/bin/env python3

import tkinter as tk
from frames import clear
from results import displayResults

class ResultsWindow:
    def __init__(self, parentWindow, tour):
        self.tour = tour
        self.window = tk.Toplevel(parentWindow)
        self.window.title("🏁 Résultats du Tour")
        self.window.geometry("600x400")
        self.mainFrame = tk.Frame(self.window)
        self.mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.update()
        
    def update(self):
        clear(self.mainFrame)
        ridersData = self.tour.ridersResults()
        displayResults(self.mainFrame, ridersData)
    