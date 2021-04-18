#!/usr/bin/env python3

import tkinter as tk

def displayRider(boardWidgets, rider):
    displayRiderAtPosition(boardWidgets, rider, rider.position())

def displayRiderAtPosition(boardWidgets, rider, position):
    square, lane = position[0], position[1]
    widget = boardWidgets[square][lane]
    widget.config(text = rider.shade, fg = rider.color)

def addRouleurDisplay(rider, color):
    rider.color = color
    rider.shade = "o±ỏ"

def addSprinteurDisplay(rider, color):
    rider.color = color
    rider.shade = "o/ỏ"

def copyDisplay(target, model):
    target.color = model.color
    target.shade = model.shade
