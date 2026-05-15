from positions import absolutePosition

class ImblocableClimber:
    def applyTo(self, personnage):
        personnage.addPlayOrderRule(MountainPriority())
        personnage.addObstacleFactory(MountainObstacleFactory())

    def displayRule(self):
        return "Grimpeur Imblocable: En montagne, jouez avant tous les coureurs. Seuls vos équipiers peuvent se placer sur les autres couloirs de votre case."


class MountainObstacleFactory:
    def createFor(self, rider, track):
        return MountainObstacle(rider, track)


class MountainObstacle:
    def __init__(self, rider, track):
        self.rider = rider
        self.track = track

    def isFree(self, position):
        if self.track.getRoadType(self.rider.getSquare()) != "ascent":
            return True
        return position[0] != self.rider.getSquare()


class MountainPriority:
    def keyFor(self, rider, snapshot):
        end = rider.personnage.movementRules.computeNewPosition(rider.position(), snapshot.energyOf(rider), snapshot.track, snapshot.obstaclesFor(rider))
        if anyAscentBetween(snapshot.track, rider.position()[0], end[0]):
            return (-1, -absolutePosition(rider))
        return (0, -absolutePosition(rider))

def anyAscentBetween(track, start, end):
    for s in range(start, end + 1):
        if track.getRoadType(s) == "ascent":
            return True
    return False
