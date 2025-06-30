#!/usr/bin/env python3

from visualtests import VisualTester, runVisualTestsInWindow
import tkinter as tk
from frames import Frames

class ResultsTester(VisualTester):
    def testResults(self):
        ridersData = [
            {'name': 'rouleur', 'color': 'green', 'time': 0, 'score': 3, 'climberPoints': 4},
            {'name': 'sprinteur', 'color': 'blue', 'time': 50, 'score': 2, 'climberPoints': 0},
            {'name': 'rouleur', 'color': 'red', 'time': 60, 'score': 1, 'climberPoints': 0},
            {'name': 'sprinteur', 'color': 'green', 'time': 60, 'score': 0, 'climberPoints': 0},
            {'name': 'rouleur', 'color': 'blue', 'time': 100, 'score': 0, 'climberPoints': 0},
            {'name': 'sprinteur', 'color': 'red', 'time': 700, 'score': 0, 'climberPoints': 5}
        ]
        displayResults(self.frame, ridersData)

def displayResults(window, ridersData):
    frames = Frames(window)

    titleFrame = frames.new()
    titleLabel = tk.Label(titleFrame, text="🏁 RÉSULTATS DE LA COURSE 🏁", font=("Arial", 16, "bold"), fg="darkblue")
    titleLabel.pack(pady=10)

    # Identifier le meilleur score de grimpeur pour le maillot à pois
    bestClimberScore = max((rider['climberPoints'] for rider in ridersData), default=0)

    createTableHeader(frames)
    for position, rider in enumerate(ridersData, 1):
        _createRiderRow(frames, position, rider, bestClimberScore)

def createTableHeader(frames):
    """Crée l'en-tête du tableau avec les colonnes"""
    headerFrame = frames.new()
    headerFrame.config(bg="lightgray", relief="raised", bd=2)

    # Configuration de la grille pour l'en-tête
    cols = [
        ("Pos", 6, "center"),
        ("Coureur", 15, "w"),
        ("⏱️ Temps", 12, "center"),
        ("🏆 Points", 8, "center"),
        ("⛰️ Grimpeur", 10, "center")
    ]

    for i, (title, width, anchor) in enumerate(cols):
        label = tk.Label(headerFrame, text=title, font=("Arial", 10, "bold"),
                        bg="lightgray", width=width, anchor=anchor)
        label.grid(row=0, column=i, padx=2, pady=5, sticky="ew")

def _createRiderRow(frames, position, rider, bestClimberScore):
    """Crée une ligne pour un coureur dans le tableau"""
    rowFrame = frames.new()

    # Couleur de fond alternée
    bgColor = "white" if position % 2 == 1 else "#f0f0f0"
    rowFrame.config(bg=bgColor, relief="solid", bd=1)

    # Médaille pour les 3 premiers
    positionText = _getPositionDisplay(position)

    # Nom du coureur avec symbole de maillot à pois si meilleur grimpeur
    riderName = rider['name']
    if rider['climberPoints'] > 0 and rider['climberPoints'] == bestClimberScore:
        riderName += " 🔴⚪"  # Maillot à pois

    # Données du coureur
    timeText = secondsToMinutes(rider['time']) if rider['time'] > 0 else "Vainqueur!"
    riderPoints = rider['score'] if rider['score'] > 0 else "-"
    climberPoints = rider['climberPoints'] if rider['climberPoints'] > 0 else "-"

    # Création des colonnes
    cols = [
        (positionText, 6, "center", "black"),
        (riderName, 15, "w", rider['color']),
        (timeText, 12, "center", "black"),
        (str(riderPoints), 8, "center", "darkgreen"),
        (str(climberPoints), 10, "center", "darkred")
    ]

    for i, (text, width, anchor, color) in enumerate(cols):
        label = tk.Label(rowFrame, text=text, width=width, anchor=anchor,
                        bg=bgColor, fg=color, font=("Arial", 9))
        label.grid(row=0, column=i, padx=2, pady=3, sticky="ew")

def _getPositionDisplay(position):
    """Retourne l'affichage de la position avec médailles pour le podium"""
    if position == 1:
        return "🥇 1er"
    elif position == 2:
        return "🥈 2ème"
    elif position == 3:
        return "🥉 3ème"
    else:
        return f"{position}ème"

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
