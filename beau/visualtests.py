from unittests import runTests
from frames import Frames

class VisualTester():
    def __init__(self, window):
        self.frames = Frames(window)
        window.bind("<space>", lambda e: window.destroy())

    def __before__(self):
        self.frame = self.frames.new()


import tkinter as tk
def runVisualTestsInWindow(testerClass):
    window = tk.Tk()
    runTests(testerClass(window))
    window.mainloop()


