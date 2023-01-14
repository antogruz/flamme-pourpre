#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
import tkinter as tk
from frames import Frames

class ResultsTester(VisualTester):
    def testResults(self):
        displayResults(self.frame, [("green", 3), ("blue", 1), ("red", 0)], [("green rouleur", 0), ("blue sprinteur", 50), ("red rouleur", 60), ("green sprinteur", 60), ("blue rouleur", 100), ("red sprinteur", 700)])

def displayResults(window, scores, times):
    frames = Frames(window)
    packArray(frames, "Tour ranking", scores, parseTeamScore)
    packArray(frames, "Times ranking", times, parseRiderTime)


def packArray(frames, title, lines, parse):
    tk.Label(frames.new(), text = title).pack()
    for line in lines:
        key, value, color = parse(line)
        keyFrame, valueFrame = frames.newLine(2)
        tk.Label(keyFrame, text = key, fg = color).pack()
        tk.Label(valueFrame, text = value, fg = "white", bg = color).pack()


def parseTeamScore(line):
    return line[0], line[1], line[0]

def parseRiderTime(line):
    rider, time = line
    color, name = rider.split()
    return name, secondsToMinutes(time), color


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
