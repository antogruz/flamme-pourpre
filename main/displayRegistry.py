#!/usr/bin/env python3

class DisplayRegistry:
    def __init__(self):
        self.displays = []
        
    def register(self, display):
        self.displays.append(display)
        
    def getAll(self):
        return self.displays
        