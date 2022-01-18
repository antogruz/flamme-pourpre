#!/usr/bin/env python3

def findAllMethods(object):
    return [method for method in dir(object) if callable(getattr(object, method))]

class Tester:
    def runTests(self):
        methodNames = findAllMethods(self)
        testNames = [m for m in methodNames if "test" in m]
        for test in testNames:
            print(test)
            if "__before__" in methodNames:
                self.__before__()
            getattr(self, test)()
            try:
                self.__del__()
            except:
                pass


def assert_equals(expected, actual):
    if expected != actual:
        raise Exception("Expected", expected, "got", actual)

def assert_contains(expected, collection):
    if expected not in collection:
        raise Exception("Expected", expected, "to be in", collection)

def assert_similars(expected, actual):
    if not len(expected) == len(actual):
        raise Exception("Expected size of {}, but got {}. So actual {} is not similar to expected {}".format(len(expected), len(actual), actual, expected))
    for e in expected:
        assert_contains(e, actual)
