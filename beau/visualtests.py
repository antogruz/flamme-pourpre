from unittests import runTests
from frames import Frames
import tkinter as tk

class VisualTester():
    def __init__(self, window):
        self.frames = Frames(window)
        window.bind("<space>", lambda e: window.destroy())

    def __before__(self):
        self.frame = self.frames.new()

    def __display__(self, testName):
        titleFrame = self.frames.new()
        tk.Label(titleFrame, text = str(testName)).pack()


def runVisualTestsInWindow(testerClass):
    window = tk.Tk()
    runTests(testerClass(window))
    window.mainloop()


