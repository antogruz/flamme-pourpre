from unittests import Tester

class VisualTester(Tester):
    def __init__(self, frames):
        self.frames = frames

    def __before__(self):
        self.frame = self.frames.new()


