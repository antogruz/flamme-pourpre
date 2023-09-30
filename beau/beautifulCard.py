#!/usr/bin/env python3

import re

class BeautifulCard:
    def __init__(self, text, color = "black", background = "white"):
        self.text = text
        self.color = color
        self.background = background


def createBeautifulCard(card, defaultColor = "black"):
    card = str(card)
    if card == "f":
        return BeautifulCard("f", "white", "red")
    if thereIsColorIn(card):
        text, color = extractColor(card)
        return BeautifulCard(text, color)
    return BeautifulCard(card, defaultColor)

def colorsBank():
    return ["goldenrod", "magenta", "red", "blue", "green", "black", "pink"]

def thereIsColorIn(string):
    for color in colorsBank():
        if color in string:
            return True
    return False

def extractColor(string):
    for color in colorsBank():
        if color in string:
            return re.sub(color, "", string), color

