#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
import tkinter as tk
from frames import Frames

class ResultsTester(VisualTester):
    def testResults(self):
        displayResults(self.frame, [("green", 3), ("blue", 1), ("red", 0)], [("green rouleur", 0), ("blue sprinteur", 50), ("red rouleur", 60), ("green sprinteur", 60), ("blue rouleur", 100), ("red sprinteur", 700)])

def displayResults(window, scores, times):
    subFrames = Frames(window)
    title = subFrames.new()
    tk.Label(title, text = "Tour ranking").pack()
    for (team, score) in scores:
        (name, points) = subFrames.newLine(2)
        tk.Label(name, text = team, fg = team).pack()
        tk.Label(points, text = score, fg = "white", bg = team).pack()

    subtitle = subFrames.new()
    tk.Label(subtitle, text = "Times ranking").pack()
    for (rider, time) in times:
        (name, points) = subFrames.newLine(2)
        color, riderName = rider.split()
        tk.Label(name, text = riderName, fg = color).pack()
        tk.Label(points, text = secondsToMinutes(time), fg = "white", bg = color).pack()


def secondsToMinutes(n):
    if n == 0:
        return "    "

    minutes = int(n / 60)
    seconds = int(n % 60)
    display = ""
    if minutes:
        display += str(minutes) + "m"
    if seconds:
        display += str(seconds) + "s"
    return display


if __name__ == "__main__":
    runVisualTestsInWindow(ResultsTester)
