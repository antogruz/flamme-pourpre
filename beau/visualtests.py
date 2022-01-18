from unittests import Tester
from frames import Frames

class VisualTester(Tester):
    def __init__(self, window):
        self.frames = Frames(window)
        window.bind("<space>", lambda e: window.destroy())

    def __before__(self):
        self.frame = self.frames.new()


import tkinter as tk
def runVisualTestsInWindow(testerClass):
    window = tk.Tk()
    testerClass(window).runTests()
    window.mainloop()


