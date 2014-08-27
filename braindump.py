import os
from collections import OrderedDict
import random
import numpy
from matplotlib import pyplot


class Brainwave(object):
    def __init__(self, amplitudes, deltas):
        self.amplitudes = amplitudes
        self.deltas = deltas

    def graph(self):
        pyplot.figure(random.randint(1, 2 ** 10))
        plotted, = pyplot.plot(
            self.deltas,
            self.amplitudes,
        )
        pyplot.xlabel('Time (ms)')
        pyplot.ylabel(u'Voltage (\u03bcV)')
        pyplot.show()

    def __len__(self):
        return len(self.amplitudes)


class Brain(object):
    def __init__(self, brainwaves, regions=None):
        regions = regions or (str(x) for x in range(len(brainwaves) + 1)[1:])
        self.data = OrderedDict(zip(regions, brainwaves))

    @staticmethod
    def from_file(fpath):
        waves = []
        if not os.path.exists(fpath):
            if os.path.exists(os.path.join('data', fpath)):
                fpath = os.path.join('data', fpath)
        data = numpy.genfromtxt(fpath, delimiter='\t')
        deltas = [i * 4 for i in range(data.shape[0])]
        for etrode in range(data.shape[1] - 1):  # Discard reference node
            waves.append(Brainwave(data[:, etrode], deltas))
        return Brain(waves)

    def montage(self, *electrodes):
        electrodes = electrodes or self.data.keys()
        sum = numpy.zeros(len(self.data['1']))
        for electrode in electrodes:
            brainwave = self.data[str(electrode)]
            sum += brainwave.amplitudes
        return Brainwave(sum / float(len(electrodes)), brainwave.deltas)

    def graph(self, *electrodes):
        electrodes = electrodes or self.data.keys()
        for count, electrode in enumerate(electrodes):
            pyplot.subplot(210)
            plotted, = pyplot.plot(
                self.data[str(electrode)].deltas,
                self.data[str(electrode)].amplitudes,
            )
        pyplot.show()

if __name__ == '__main__':
    brain = Brain.from_file('data/omar_note_A.txt')
    brain.graph(1, 2, 3)
    brain.montage(22, 23, 24).graph()
