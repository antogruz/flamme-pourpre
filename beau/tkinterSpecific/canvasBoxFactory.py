#!/usr/bin/env python3

import tkinter as tk

class CanvasBox:
    """Équivalent de Box mais pour Canvas - même interface publique"""
    
    def __init__(self, canvas, rect_id, text_id):
        self.canvas = canvas
        self.rect_id = rect_id
        self.text_id = text_id
        self.defaultBackground = "white"

    def setContent(self, content, color):
        """Met à jour le texte et sa couleur"""
        self.canvas.itemconfig(self.text_id, text=content, fill=color)

    def setBackground(self, color):
        """Change la couleur de fond de la case"""
        if color == "default":
            color = self.defaultBackground
        self.canvas.itemconfig(self.rect_id, fill=color)

    def clear(self):
        """Remet la case à vide avec couleur par défaut"""
        self.canvas.itemconfig(self.text_id, text="", fill="black")
        self.canvas.itemconfig(self.rect_id, fill=self.defaultBackground)

    def setBorder(self, color, thickness=1):
        """Change la couleur de la bordure"""
        self.canvas.itemconfig(self.rect_id, outline=color, width=thickness)


class CanvasBoxFactory:
    """Factory qui crée des boxes sur Canvas au lieu de widgets Tkinter"""
    
    def __init__(self, frame):
        self.frame = frame
        self.maxColumn = 30
        
        # Créer le Canvas qui va contenir toutes les boxes
        # Taille estimée : 30 colonnes * 42px + marge
        canvas_width = self.maxColumn * 42 + 100
        canvas_height = 500  # Suffisant pour les plus grands circuits + cases invisibles
        
        self.canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Configurer le frame pour que le canvas s'étende
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
    def getBox(self, row, column):
        """Crée une box à la position donnée - même interface que BoxFactory"""
        width = 40
        height = 20
        
        # Calculer la position sur le canvas
        # Reproduire la même logique de placement que l'original
        grid_row = 4 * (column // self.maxColumn) + 3 - row
        grid_column = column % self.maxColumn
        
        # Convertir en coordonnées pixels
        x = grid_column * 42 + 10  # +10 pour marge, +2 pour espacement
        y = grid_row * 22 + 10     # +10 pour marge, +2 pour espacement
        
        # Créer le rectangle (bordure)
        rect_id = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            outline="white", width=1, fill="white"
        )
        
        # Créer le texte centré
        text_x = x + width // 2
        text_y = y + height // 2
        text_id = self.canvas.create_text(
            text_x, text_y
        )
        
        # Créer et retourner la box
        box = CanvasBox(self.canvas, rect_id, text_id)
        
        return box

def buildCanvasFactory(frame):
    return CanvasBoxFactory(frame)