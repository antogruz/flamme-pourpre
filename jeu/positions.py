#!/usr/bin/env python3

def headToTail(riders):
    return sorted(riders, key = absolutePosition, reverse = True)

def tailToHead(riders):
    return sorted(riders, key = absolutePosition)

def absolutePosition(rider):
    square, lane = rider.position()
    return 10*square + 1 - lane

