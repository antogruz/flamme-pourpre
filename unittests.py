#!/usr/bin/env python3

def findAllMethods(object):
    return [method for method in dir(object) if callable(getattr(object, method))]

class Tester:
    def runTests(self):
        methodNames = findAllMethods(self)
        testNames = [m for m in methodNames if "test" in m]
        for test in testNames:
            print(test)
            self.__init__()
            getattr(self, test)()
            try:
                self.__del__()
            except:
                pass


def assert_equals(expected, actual):
    if expected != actual:
        print("Expected", expected, "got", actual)
        raise Exception("Error in test")

def assert_contains(expected, collection):
    if expected not in collection:
        print("Expected", expected, "to be in", collection)
        raise Exception("Error in test")

def assert_similars(expected, actual):
    if not len(expected) == len(actual):
        print("Expected size of", expected, "(", len(expected), ") to be", len(actual), "the size of", actual)
    for e in expected:
        assert_contains(e, actual)
