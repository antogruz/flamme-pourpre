from positions import absolutePosition

class SeFaufiler:
    def applyTo(self, personnage):
        personnage.addPlayOrderRule(SeFaufilerRule())

    def displayRule(self):
        return "Se faufiler: Joue toujours en premier de son groupe."


class SeFaufilerRule:
    def keyFor(self, rider, snapshot):
        group = snapshot.groupOf(rider)
        head = max(group.riders, key = absolutePosition)
        return (0, -(absolutePosition(head) + 1))