import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from time import sleep
import threading


fig, ax = plt.subplots()
line, = ax.plot(np.random.rand(100))
ax.set_ylim(-1, 1)
y = 100*[0]
def update(data):
    line.set_ydata(y)
    return line,

def plotValue(value: float):
    global y
    y.append(value)
    y = y[-100:]
    sleep(0.001)

def plot():
    x = 0
    while True:
        x+=1
        plotValue(math.sin(x*2*math.pi/360))

plotThread = threading.Thread(target=plot, name="plotThread")
plotThread.start()
ani = animation.FuncAnimation(fig, update, interval=10, blit=True)
plt.show()


