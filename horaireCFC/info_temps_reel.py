import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator

from definitions import *


noms_gares = [gare['nom'] for gare in Gares]

def position(horaire):
    axes = plt.subplot()

    plt.plot([0, 1, 2, 3, 4, 6], [0, 0, 0, 0, 0, 0], 'bo', linestyle='-', label=noms_gares)
    for xy in zip([0, 1, 2, 3, 4, 6], [0, 0, 0, 0, 0, 0]):
        axes.annotate(noms_gares[[0, 1, 2, 3, 4, 6].index(xy[0])], xy=xy, textcoords='offset points', ha='center', xytext=(0, -20))

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()