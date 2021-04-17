#!/usr/bin/env python3

import tkinter as tk

def displayRider(boardWidgets, rider):
    square, lane = rider.position()
    widget = boardWidgets[square][lane]
    widget.config(text = rider.shade, fg = rider.color)

def addRouleurDisplay(rider, color):
    rider.color = color
    rider.shade = "o±ỏ"

def addSprinteurDisplay(rider, color):
    rider.color = color
    rider.shade = "o/ỏ"

