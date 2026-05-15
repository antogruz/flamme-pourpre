#!/usr/bin/env python3

class Obstacles:
    def __init__(self, obstacles, track = None):
        self.obstacles = obstacles
        self.track = track

    def isFree(self, slot):
        for o in self.obstacles:
            if o.position() == slot:
                return False
            if self.track is not None and self.blockedByRules(o, slot):
                return False
        return True

    def blockedByRules(self, blocker, slot):
        if not hasattr(blocker, "personnage"):
            return False
        for rule in blocker.personnage.blockingRules:
            if rule.blocks(blocker, slot, self.track):
                return True
        return False

