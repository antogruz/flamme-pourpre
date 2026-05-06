#!/usr/bin/env python3

import tkinter as tk
from frames import clear
from results import displayResults

class ResultsWindow:
    def __init__(self, parentWindow, tour, appearances):
        self.tour = tour
        self.appearances = appearances
        self.window = tk.Toplevel(parentWindow)
        self.window.title("🏁 Résultats du Tour")
        self.window.geometry("600x400")
        self.mainFrame = tk.Frame(self.window)
        self.mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.update()

    def update(self):
        clear(self.mainFrame)
        ridersData = [self._toViewModel(r) for r in self.tour.ridersResults()]
        displayResults(self.mainFrame, ridersData)

    def _toViewModel(self, result):
        appearance = self.appearances.of(result['rider'])
        return {
            'name': appearance.name,
            'color': appearance.color,
            'time': result['time'],
            'score': result['score'],
            'climberPoints': result['climberPoints'],
        }
