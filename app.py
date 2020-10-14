import sys
import numpy as np
from math import hypot
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import solver
import traceback


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        # Window Configurations
        self.setWindowTitle("PWS App")

        # Variables
        self.points = []
        self.sol = []

        #for x in range(6):
        #    for y in range(6):
        #        self.points.append((100 + 50* x, 100 + 50*y))

        # Widgets
        self.oplosKnop = QPushButton(self, text="Vind Oplossingen")
        self.oplosKnop.setGeometry(10, 10, 150, 30)

        # Connections
        self.oplosKnop.clicked.connect(self.get_oplossingen)

        self.showMaximized()

    def mousePressEvent(self, a0) -> None:
        lbl = QLabel(self)
        lbl.setGeometry(a0.x()-5, a0.y()-5, 30, 15)
        lbl.setText(str(len(self.points)))
        #lbl.setAlignment(Qt.AlignTop)
        lbl.show()
        self.points.append((a0.x(), a0.y()))

    def get_oplossingen(self):
        afstandsmatrix = np.zeros([len(self.points), len(self.points)], dtype=object)
        coordinaten = []
        self.sol = None

        for index_x, x in enumerate(self.points):
            for index_y, y in enumerate(self.points):
                if x == y:
                    continue
                afstandsmatrix[index_x, index_y] = hypot(abs(x[0] - y[0]), abs(x[1] - y[1]))
        afstandsmatrix[0][0] = float('inf')

        solver.afstandsmatrix = afstandsmatrix
        solver.main([x for x in range(len(afstandsmatrix))])

        for _ in range(5):
            # try it 10 times
            app.processEvents()
            sol = solver.solver.solveOnce()
            app.processEvents()

            if not self.sol:
                self.sol = sol

            elif sol[1] < self.sol[1]:
                self.sol = sol

        print(self.sol)
        self.update()

    def paintEvent(self, a0):

        try:
            if self.sol:
                painter = QPainter(self)
                painter.setPen(Qt.red)

                self.sol[0].append(self.sol[0][0])

                for i, pt in enumerate(self.sol[0][:-1]):
                    try:
                        painter.drawLine(*self.points[pt], *self.points[self.sol[0][i+1]])
                    except:
                        painter.drawLine(*self.points[pt], *self.points[0])
        except:
            traceback.print_exc()
            sys.exit()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
