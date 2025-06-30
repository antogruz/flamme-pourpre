#! /usr/bin/env python3

class NewRider():
    def __init__(self, name, movementRules, propulsor):
        self.name = name
        self.movementRules = movementRules
        self.propulsor = propulsor

    def __str__(self):
        return self.name