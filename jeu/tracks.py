#!/usr/bin/env python3
from track import Track

def corsoPaseo():
    return createTrack("abcdefghijklmnopqrstu")

def colDuBallon():
    return createTrack("AnLHgceqtrMBoipjDFkSu")

def hauteMontagne():
    return createTrack("abcfimetKGLHJsdopRQNU")

def classicissima():
    return createTrack("AebQRNHPcgikDFsLojmtu")

def rondeVanWevelgem():
    return createTrack("abcmgfteqonLPjkIDHrSu")

def firenzeMilano():
    return createTrack("abcgiDHqntmKOLrepJsfu")

def createTrack(letters):
    roads = []
    for l in letters:
        roads += getRoad(l)
    return Track(roads)

def getRoad(letter):
    d = {}
    d['a'] = "5s1n"
    for l in "bcdflmn":
        d[l] = "6n"
    for l in "eghijkopqrst":
        d[l] = "2n"
    d['u'] = "1n5e"
    d['A'] = "4s2n"
    d['B'] = "4d2n"
    d['C'] = "3n3a"
    d['D'] = "5a1d"
    d['F'] = "3d3n"
    d['L'] = "3a3d"
    d['M'] = "2n4a"
    d['N'] = "6a"
    d['U'] = "2a4e"
    for l in "EGKOQR":
        d[l] = "2a"
    for l in "IJST":
        d[l] = "2n"
    for l in "HP":
        d[l] = "2d"
    return decode(d[letter])

def decode(s):
    return [decodeCouple(couple) for couple in divide(s)]

def decodeCouple(couple):
    return (int(couple[0]), getLand(couple[1]))

def getLand(l):
    if l == 'n':
        return "normal"
    if l == 'a':
        return "ascent"
    if l == 's':
        return "start"
    if l == 'd':
        return "descent"
    if l == 'e':
        return "end"

def divide(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]

