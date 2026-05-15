from positions import absolutePosition

class ImblocableClimber:
    def applyTo(self, personnage):
        personnage.addPlayOrderRule(MountainPriority())

    def displayRule(self):
        return "Grimpeur Imblocable: En montagne, jouez avant tous les coureurs. Seuls vos équipiers peuvent se placer sur les autres couloirs de votre case."

class MountainPriority:
    def keyFor(self, rider, snapshot):
        end = rider.personnage.movementRules.computeNewPosition(rider.position(), snapshot.energyOf(rider), snapshot.track, snapshot.obstacles)
        if anyAscentBetween(snapshot.track, rider.position()[0], end[0]):
            return (-1, -absolutePosition(rider))
        return (0, -absolutePosition(rider))

def anyAscentBetween(track, start, end):
    for s in range(start, end + 1):
        if track.getRoadType(s) == "ascent":
            return True
    return False