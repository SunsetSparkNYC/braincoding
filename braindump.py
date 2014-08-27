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
        plotted.set_antialiased(False)
        pyplot.xlabel('Time (ms)')
        pyplot.ylabel(u'Voltage (\u03bcV)')
        pyplot.show()

    def __len__(self):
        return len(self.amplitudes)


class Brain(object):
    def __init__(self, brainwaves, regions=None):
        regions = regions or (str(x) for x in range(len(brainwaves) + 1)[1:])
        self.data = dict(zip(regions, brainwaves))

    @staticmethod
    def from_file(fpath):
        waves = []
        data = numpy.genfromtxt(fpath, delimiter='\t')
        deltas = [i * 4 for i in range(data.shape[0])]
        for etrode in range(data.shape[1] - 1):  # Discard reference node
            waves.append(Brainwave(data[:, etrode], deltas))
        return Brain(waves)

    def montage(self, *electrodes):
        electrodes = electrodes or range(len(self.data))
        sum = numpy.zeros(len(self.data['1']))
        for electrode in electrodes:
            brainwave = self.data[str(electrode)]
            sum += brainwave.amplitudes
        return Brainwave(sum / float(len(electrodes)), brainwave.deltas)


if __name__ == '__main__':
    brain = Brain.from_file('data/omar_note_A.txt')
    brain.montage(22, 23, 24).graph()
