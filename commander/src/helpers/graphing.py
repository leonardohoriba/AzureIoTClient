import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

class Graphing:
    def __init__(self, numPlots: int, numPoints: int):
        self._numPlots = numPlots
        self._numPoints = numPoints
        self._fig, self._ax = plt.subplots()
        self._line = numPlots*[Line2D]
        for plotNumber in range(0, numPlots):
            self._line[plotNumber], = self._ax.plot(np.random.rand(numPoints))
        self._ax.set_ylim(-500, 500)
        self._y = numPlots*[numPoints*[0]]

    def __update(self, data):
        for plotNumber in range(0, self._numPlots):        
            self._line[plotNumber].set_ydata(self._y[plotNumber])
        return self._line

    def plotValue(self, value: list[float]):
        for plotNumber in range(0, self._numPlots):
            self._y[plotNumber].append(value[plotNumber])
            self._y[plotNumber] = (self._y[plotNumber])[-self._numPoints:]

    def plotGraph(self) -> None:
        # Don't delete this variable ani below, otherwise graph doesn't plot
        # TODO: Find out why
        ani = animation.FuncAnimation(self._fig, self.__update, interval=10, blit=True)
        plt.show()