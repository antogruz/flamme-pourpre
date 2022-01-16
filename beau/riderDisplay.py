#!/usr/bin/env python3

rouleurShade = "o±ỏ"
sprinteurShade = "o/ỏ"

def displayRider(boardWidgets, rider):
    displayRiderAtPosition(boardWidgets, rider, rider.position())

def displayRiderAtPosition(boardWidgets, rider, position):
    square, lane = position[0], position[1]
    widget = boardWidgets[square][lane]
    widget.config(text = rider.shade, fg = rider.color)

def addRouleurDisplay(rider, color):
    rider.color = color
    rider.shade = rouleurShade

def addSprinteurDisplay(rider, color):
    rider.color = color
    rider.shade = sprinteurShade

