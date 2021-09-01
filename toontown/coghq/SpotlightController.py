from direct.interval.IntervalGlobal import *
import random

class SpotlightController:

    def __init__(self):
        self.sequences = {}

    def delete(self):
        for sequence in list(self.sequences.values()):
            sequence.pause()

        self.sequences = {}

    def start(self, spotlights):
        self.delete()
        for i, spotlight in enumerate(spotlights):
            if '6' in spotlight.getName():
                continue
            spotlight.setY(-1.75)
            self.startSpotlightSequence(i, spotlight, random.uniform(-5, 5))

    def startSpotlightSequence(self, i, spotlight, lastR):
        if i in self.sequences:
            self.sequences[i].pause()
        sequence = Sequence(Wait(random.uniform(0, 1)), spotlight.hprInterval(random.uniform(3.5, 5.5), (0, 0, -6), (0, 0, lastR), blendType='easeInOut'),
                            spotlight.hprInterval(random.uniform(3.5, 5.5), (0, 0, 6), (0, 0, -6), blendType='easeInOut'), Func(self.startSpotlightSequence, i, spotlight, 6))
        self.sequences[i] = sequence
        sequence.start()