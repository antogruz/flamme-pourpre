#!/usr/bin/env python3

# Cette fonction (slipstreaming) gère les régles d'aspiration.
# Elle doit être modifiée si les règles changent.
# Dans l'état actuel des choses, elle devra aussi être modifiée si certains coureurs ont leurs propres règles d'aspiration, mais il faudra sûrement ajouter des tests pour vérifier cela. Il faudra travailler à définir de nouvelles méthodes à l'interface du rider pour ne pas toucher à cette classe lorsque de nouveaux pouvoirs liés à l'aspiration apparaissent TODO

from groups import splitByGroupBehind
from positions import tailToHead, headToTail
from obstacles import Obstacles, obstaclesFromRiders


def slipstreaming(riders, track, observers = None, obstacles = None):
    if observers is None:
        observers = []
    if obstacles is None:
        obstacles = obstaclesFromRiders(riders)
    applyPersonalRules(riders, track, observers, obstacles)
    candidates = tailToHead(riders)
    while candidates:
        group, others = splitByGroupBehind(candidates)

        if not someCanSlipstream(group, others, track):
            candidates = others
            continue

        moves, streamedRiders = streamGroup(group, track, obstacles)
        for observer in observers:
            observer.onSlipstream(moves)
        candidates = tailToHead(streamedRiders) + others


def streamGroup(group, track, obstacles):
    moves = []
    group.riders = headToTail(group.riders)
    for i, rider in enumerate(group.riders):
        if not streamable(track.getRoadType(rider.getSquare())):
            return moves, keepFirsts(group.riders, i)
        origin = rider.position()
        rider.earnSquares(1, track, obstacles)
        moves.append((rider, origin, rider.position()))
        if rider.getSquare() == origin[0]:
            return moves, group.riders
    return moves, group.riders


def keepFirsts(l, count):
    return l[0:count]

def someCanSlipstream(group, otherRiders, track):
    for rider in otherRiders:
        if couldSlipstream(group.head, rider, track):
            return True
    return False

def couldSlipstream(square, rider, track):
    if not streamable(track.getRoadType(rider.getSquare())):
        return False

    return rider.getSquare() == square + 2

def applyPersonalRules(riders, track, observers, obstacles):
    for rider in tailToHead(riders):
        distances = []
        for rule in rider.personnage.slipstreamRules:
            distance = rule.squaresEarned(rider, riders, track)
            if distance > 0:
                distances.append(distance)
        if distances:
            origin = rider.position()
            rider.earnSquares(max(distances), track, obstacles)
            if rider.position() != origin:
                for observer in observers:
                    observer.onSlipstream([(rider, origin, rider.position())])


class SlipstreamRule:
    """Interface for personal slipstreaming rules.

    Implement this to grant a rider extra squares beyond standard slipstreaming,
    based on their personal context (talents like Remontée de Peloton, Inlarguable, etc.).
    Returned distances of all rules attached to a rider are max-composed.
    """
    def squaresEarned(self, rider, riders, track):
        """Return the number of squares `rider` earns from this rule (0 if none)."""
        pass


from specialTour.talents.remonteeDePeloton import RemonteeDePeloton
from specialTour.talents.inlarguable import Inlarguable
from unittests import assert_equals, runTests
from riderInRace import RiderInRace
from track import Track, streamable
from obstacles import Obstacles
class SlipstremingTester():
    def __before__(self):
        self.rider = createRider(0, 0)
        self.track = Track([(10, "normal")])
        self.others = []

    def slipstream(self):
        slipstreaming([self.rider] + self.others, self.track, None, obstaclesFromRiders([self.rider] + self.others))

    def addRider(self, square):
        self.others.append(createRider(square, 0))

    def assertPosition(self, square):
        assert_equals((square, 0), self.rider.position())

    def testOneRiderDontMove(self):
        self.slipstream()
        self.assertPosition(0)

    def testTwoRiders(self):
        self.addRider(2)
        self.slipstream()
        self.assertPosition(1)

    def testTooFar(self):
        self.addRider(3)
        self.slipstream()
        self.assertPosition(0)

    def testNoSlipstreamInSameGroup(self):
        self.addRider(1)
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def test3Groups(self):
        self.rider = createRider(3, 0)
        self.addRider(0)
        self.addRider(5)
        self.slipstream()
        self.assertPosition(4)

    def testWholeGroupStreamed(self):
        self.rider = createRider(1, 0)
        self.addRider(0)
        self.addRider(2)
        self.addRider(4)
        self.slipstream()
        self.assertPosition(2)

    def testChainStream(self):
        self.addRider(2)
        self.addRider(4)
        self.slipstream()
        self.assertPosition(2)

    def testRiderInAscentIsNotStreamed(self):
        self.track = Track([(1, "ascent"), (10, "normal")])
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def testRiderInAscentCannotStreamOthers(self):
        self.track = Track([(2, "normal"), (1, "ascent")])
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def testHeadOfGroupInAscent(self):
        self.track = Track([(1, "normal"), (1, "ascent"), (2, "normal")])
        self.addRider(1)
        self.addRider(3)
        self.slipstream()
        self.assertPosition(0)

    def testBackOfGroupInAscent(self):
        track = Track([(1, "ascent"), (9, "normal")])
        grimpeur = createRider(0, 0)
        rouleur = createRider(1, 0)
        streamer = createRider(3, 0)
        slipstreaming([grimpeur, rouleur, streamer], track)
        assert_equals((0, 0), grimpeur.position())
        assert_equals((2, 0), rouleur.position())

    def testNoSlipstreamingAfterEnd(self):
        self.track = Track([(1, "normal"), (5, "end")])
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def testSlipstreamLogs(self):
        self.track = Track([(10, "normal")])
        self.addRider(1)
        self.addRider(3)
        self.addRider(4)
        self.addRider(6)
        riders = [self.rider] + self.others
        observer = Logger()
        slipstreaming(riders, self.track, [observer])
        assert_equals([[2, 1], [5, 4, 3, 2]], observer.groups)

    def testRiderOnStoneIsNotStreamed(self):
        self.track = Track([(1, "stone"), (10, "normal")])
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def testRiderOnStoneCannotStreamOthers(self):
        self.track = Track([(2, "normal"), (1, "stone")])
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    # --- | o/o |
    # o/o | o/o | --- | o/o |
    def testGroupSlipstreamedInRoadReduction(self):
        self.track = Track([(2, "normal", 2), (2, "normal", 1)])
        self.others.append(createRider(1, 0))
        self.others.append(createRider(1, 1))
        self.addRider(3)
        self.slipstream()
        assert_equals((0, 0), self.rider.position())
        assert_equals((2, 0), self.others[0].position())
        assert_equals((1, 0), self.others[1].position())

    # --- | o/o |
    # o/o | o/o | --- | o/o | --- | o/o |
    def testRoadReductionThenOtherGroupIncludesAll(self):
        self.track = Track([(2, "normal", 2), (4, "normal", 1)])
        self.others.append(createRider(1, 0))
        self.others.append(createRider(1, 1))
        self.addRider(3)
        self.addRider(5)
        self.slipstream()
        self.assertPosition(1)

    def testRemonteeDePeloton(self):
        self.rider.personnage.gainTalent(RemonteeDePeloton())
        self.addRider(1)
        self.addRider(2)
        self.slipstream()
        assert_equals((1, 1), self.rider.position())

    def testRemonteeDePelotonWithOtherRiders(self):
        self.rider = createRider(2, 0)
        self.rider.personnage.gainTalent(RemonteeDePeloton())
        self.addRider(0)
        self.addRider(4)
        self.slipstream()
        self.assertPosition(3)
        assert_equals((2, 0), self.others[0].position())

    def testRemonteeDePelotonNeedsSomeone2SquaresFront(self):
        self.rider.personnage.gainTalent(RemonteeDePeloton())
        self.addRider(1)
        self.slipstream()
        self.assertPosition(0)

    def testRemonteeDePelotonNeedsRoomToProgress(self):
        self.rider.personnage.gainTalent(RemonteeDePeloton())
        self.others.append(createRider(1, 0))
        self.others.append(createRider(1, 1))
        self.others.append(createRider(2, 0))
        self.slipstream()
        self.assertPosition(0)

    def testRemonteeDePelotonUselessInAscent(self):
        self.track = Track([(10, "ascent")])
        self.rider.personnage.gainTalent(RemonteeDePeloton())
        self.addRider(1)
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def testInlarguable(self):
        self.rider.personnage.gainTalent(Inlarguable())
        self.addRider(3)
        self.addRider(4)
        self.slipstream()
        self.assertPosition(2)

    def testInlarguableDoesNotWorkWithEscape(self):
        self.rider = createRider(2, 0)
        self.addRider(0)
        self.addRider(1)
        self.rider.personnage.gainTalent(Inlarguable())
        self.addRider(5)
        self.slipstream()
        self.assertPosition(2)

    def testInlarguableWorkOnPelotonEvenIfThereIsAnEscape(self):
        self.rider.personnage.gainTalent(Inlarguable())
        self.addRider(3)
        self.addRider(4)
        self.addRider(8)
        self.addRider(9)
        self.slipstream()
        self.assertPosition(2)

from riderBuilder import RiderBuilder
def createRider(square, lane):
    rb = RiderBuilder()
    return RiderInRace(rb.getResult(), square, lane)

class Logger():
    def __init__(self):
        self.groups = []

    def onSlipstream(self, moves):
        self.groups.append([end[0] for _, _, end in moves])


def display(groups):
    for g in groups:
        print("group")
        for rider in g.riders:
            print (rider.position())

if __name__ == "__main__":
    runTests(SlipstremingTester())
