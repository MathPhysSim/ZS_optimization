# Imports
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
# Ensure using PyQt5 backend
# matplotlib.use('QT5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
# Matplotlib canvas class to create figure


# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()  # self.axs = plt.subplots(1,2)
        self.axs = [0, 0, 0]
        self.axs[0] = self.fig.add_subplot(211)
        self.axs[1] = self.fig.add_subplot(212, sharex=self.axs[0])
#        self.axs[2] = self.axs[1].twinx()
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

# Matplotlib widget


class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(NavigationToolbar(self.canvas, self))
        self.setLayout(self.vbl)

