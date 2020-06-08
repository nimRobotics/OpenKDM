from fbs_runtime.application_context.PyQt5 import ApplicationContext
# https://gist.github.com/MalloyDelacroix/2c509d6bcad35c7e35b1851dfc32d161

import sys
from PyQt5.QtCore import QObject, pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QRadioButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget,  QMessageBox, QSizePolicy, QGridLayout, QPlainTextEdit, QCheckBox)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mechanismClass import *
#  for analytical solutions
from analytical import sliderCrank


class plot_figure(FigureCanvas):

    def __init__(self, width=50, height=50, dpi=100, parent=None,):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def draw_graph_fourbar(self, a, b, p, q, omega):
        self.ax1 = self.fig.add_subplot(2,1,1)
        # self.ax2 = self.fig.add_subplot(2,1,2)
        self.m = My_mechanism(a,b,p,q,omega)
        self.anim = animation.FuncAnimation(self.fig, self.animate_loop_fourbar, interval=10)
        self.draw()

    def animate_loop_fourbar(self,i):
        p_x,p_y = self.m.rod_p_position(self.m.k)
        q_x,q_y = self.m.rod_q_position(self.m.k)
        # c_x = self.m.piston_position(self.m.k)
        self.ax1.clear()
        # self.ax2.clear()
        # rod P
        self.ax1.plot([link_p_pivot[0],p_x],[link_p_pivot[1],p_y],linewidth=3,color='blue')
        # rod Q
        self.ax1.plot([p_x,q_x],[p_y,q_y],linewidth=3,color='green')
        # rod A
        self.ax1.plot([q_x,link_a_pivot[0]],[q_y,link_a_pivot[1]],linewidth=3,color='red')
        # rod B
        # self.ax1.plot([q_x,c_x],[q_y,link_a_pivot[1]],linewidth=3,color='yellow')
        # Piston (c)
        # self.ax1.plot(c_x,link_a_pivot[1],'s',markersize=20,color='magenta')
        self.ax1.set_xlim(-50,50)
        self.ax1.set_ylim(-50,50)
        self.ax1.set_title('Crankshaft, connecting rod and piston mechanism')
        # Piston speed
        # self.m.c_speed.append(self.m.c_dot(self.m.k))
        # self.m.c_time.append(100*self.m.k)
        # self.ax2.plot(self.m.c_time,self.m.c_speed,color='green')
        # self.ax2.set_xlim(0,600)
        # self.ax2.set_ylim(0,200)
        # self.ax2.set_ylabel("Speed $(m/s)$")
        # self.ax2.set_xlabel("time $(s*100)$")
        # self.ax2.set_title('Piston speed')
        self.ax1.set_aspect("equal")
        # self.ax2.set_aspect("equal")
        self.m.k += 0.01


    def draw_graph_sixbar(self, a, b, p, q, omega):
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        self.m = My_mechanism(a,b,p,q,omega)
        self.anim = animation.FuncAnimation(self.fig, self.animate_loop_sixbar, interval=10)
        self.draw()

    def animate_loop_sixbar(self,i):
        p_x,p_y = self.m.rod_p_position(self.m.k)
        q_x,q_y = self.m.rod_q_position(self.m.k)
        c_x = self.m.piston_position(self.m.k)
        self.ax1.clear()
        self.ax2.clear()
        # rod P
        self.ax1.plot([link_p_pivot[0],p_x],[link_p_pivot[1],p_y],linewidth=3,color='blue')
        # rod Q
        self.ax1.plot([p_x,q_x],[p_y,q_y],linewidth=3,color='green')
        # rod A
        self.ax1.plot([q_x,link_a_pivot[0]],[q_y,link_a_pivot[1]],linewidth=3,color='red')
        # rod B
        self.ax1.plot([q_x,c_x],[q_y,link_a_pivot[1]],linewidth=3,color='yellow')
        # Piston (c)
        self.ax1.plot(c_x,link_a_pivot[1],'s',markersize=20,color='magenta')
        self.ax1.set_xlim(-50,130)
        self.ax1.set_ylim(-50,50)
        self.ax1.set_title('Crankshaft, connecting rod and piston mechanism')
        # Piston speed
        self.m.c_speed.append(self.m.c_dot(self.m.k))
        self.m.c_time.append(100*self.m.k)
        self.ax2.plot(self.m.c_time,self.m.c_speed,color='green')
        self.ax2.set_xlim(0,600)
        self.ax2.set_ylim(0,200)
        self.ax2.set_ylabel("Speed $(m/s)$")
        self.ax2.set_xlabel("time $(s*100)$")
        self.ax2.set_title('Piston speed')
        self.ax1.set_aspect("equal")
        self.ax2.set_aspect("equal")
        self.m.k += 0.01


    def draw_graph_slider(self, a, b, omega):
        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        self.m = My_mechanism_slider(a,b,omega)
        self.anim = animation.FuncAnimation(self.fig, self.animate_loop_slider, interval=10)
        self.draw()

    def animate_loop_slider(self,i):
        # p_x,p_y = self.m.rod_p_position(self.m.k)
        a_x,a_y = self.m.rod_a_position(self.m.k)
        c_x = self.m.piston_position(self.m.k)
        self.ax1.clear()
        self.ax2.clear()
        # rod P
        # self.ax1.plot([link_p_pivot[0],p_x],[link_p_pivot[1],p_y],linewidth=3,color='blue')
        # rod Q
        # self.ax1.plot([p_x,q_x],[p_y,q_y],linewidth=3,color='green')
        # rod A
        self.ax1.plot([a_x,link_a_pivot[0]],[a_y,link_a_pivot[1]],linewidth=3,color='red')
        # rod B
        self.ax1.plot([a_x,c_x],[a_y,link_a_pivot[1]],linewidth=3,color='yellow')
        # Piston (c)
        self.ax1.plot(c_x,link_a_pivot[1],'s',markersize=20,color='magenta')
        self.ax1.set_xlim(-50,130)
        self.ax1.set_ylim(-50,50)
        self.ax1.set_title('Crankshaft, connecting rod and piston mechanism')
        # Piston speed
        self.m.c_speed.append(self.m.c_dot(self.m.k))
        self.m.c_time.append(100*self.m.k)
        # self.ax2.plot(self.m.c_time,self.m.c_time)
        self.ax2.plot(self.m.c_time,self.m.c_speed,color='green')
        self.ax2.set_xlim(0,600)
        self.ax2.set_ylim(0,200)
        self.ax2.set_ylabel("Speed $(m/s)$")
        self.ax2.set_xlabel("time $(s*100)$")
        self.ax2.set_title('Piston speed')
        self.ax1.set_aspect("equal")
        self.ax2.set_aspect("equal")
        self.m.k += 0.01


    def clear_plot(self):
        self.anim.event_source.stop()
        if self.ax1 is not None:
            self.ax1.clear()
        if self.ax2 is not None:
            self.ax2.clear()
        self.draw()


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.a=26
        self.b=76
        self.p=18
        self.q=22
        self.omega=2

        # Right
        # a=26,b=79,p=18,q=22,omega=2
        self.plot_figure = plot_figure(width=8, height=4)
        self.right = QVBoxLayout()
        self.right.addWidget(self.plot_figure)

        # Left: selectMechanism radio buttons
        self.fourbar = QRadioButton("Four bar")
        self.slidercrank = QRadioButton("Slider crank")
        self.sixbar = QRadioButton("Six bar")

        self.selectMechanism = QHBoxLayout()
        self.selectMechanism.addWidget(self.fourbar)
        self.selectMechanism.addWidget(self.slidercrank)
        self.selectMechanism.addWidget(self.sixbar)

        self.fourbar.setChecked(True)
        self.fourbar.toggled.connect(self.four_bar)
        self.slidercrank.toggled.connect(self.slider_crank)
        self.sixbar.toggled.connect(self.six_bar)

        # left: link lengths input
        self.lenA = QLineEdit()
        self.lenAbox = QHBoxLayout()
        self.lenAbox.addWidget(QLabel("Link A length"))
        self.lenAbox.addWidget(self.lenA)
        self.lenAbox.addWidget(QLabel("cm"))

        self.lenB = QLineEdit()
        self.lenB.setEnabled(False)
        self.lenBbox = QHBoxLayout()
        self.lenBbox.addWidget(QLabel("Link B length"))
        self.lenBbox.addWidget(self.lenB)
        self.lenBbox.addWidget(QLabel("cm"))

        self.lenP = QLineEdit()
        self.lenPbox = QHBoxLayout()
        self.lenPbox.addWidget(QLabel("Link P length"))
        self.lenPbox.addWidget(self.lenP)
        self.lenPbox.addWidget(QLabel("cm"))

        self.lenQ = QLineEdit()
        self.lenQbox = QHBoxLayout()
        self.lenQbox.addWidget(QLabel("Link Q length"))
        self.lenQbox.addWidget(self.lenQ)
        self.lenQbox.addWidget(QLabel("cm"))

        self.omega = QLineEdit()
        self.omegabox = QHBoxLayout()
        self.omegabox.addWidget(QLabel("Angular speed"))
        self.omegabox.addWidget(self.omega)
        self.omegabox.addWidget(QLabel("rad/s"))


        # left
        self.description = QLineEdit()
        self.price = QLineEdit()
        self.add = QPushButton("Simulate")
        # Disabling 'Add' button
        self.add.setEnabled(False)
        self.reset = QPushButton("Reset")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")

        self.left = QVBoxLayout()
        self.left.addWidget(QLabel("Select the mechanism"))
        self.left.addLayout(self.selectMechanism)
        self.left.addWidget(QLabel("Specify the mechanism params"))
        self.left.addLayout(self.lenAbox)
        self.left.addLayout(self.lenBbox)
        self.left.addLayout(self.lenPbox)
        self.left.addLayout(self.lenQbox)
        self.left.addLayout(self.omegabox)
        self.left.addWidget(self.add)
        self.left.addWidget(self.reset)
        self.left.addWidget(self.clear)
        self.left.addWidget(self.quit)

        # Signals and pyqtSlots
        self.add.clicked.connect(self.add_element)
        self.quit.clicked.connect(self.quit_application)
        self.reset.clicked.connect(self.reset_values)
        self.clear.clicked.connect(self.clear_inputs)


        # check when to enable Simulate button
        self.lenA.textChanged[str].connect(self.check_disable)
        self.lenB.textChanged[str].connect(self.check_disable)
        self.lenP.textChanged[str].connect(self.check_disable)
        self.lenQ.textChanged[str].connect(self.check_disable)
        self.omega.textChanged[str].connect(self.check_disable)
        # self.fourbar.


        # QWidget Layout
        self.layout = QHBoxLayout()

        # self.layout.addWidget(self.table)
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)


    # onClick for fourbar radio
    @pyqtSlot()
    def four_bar(self):
        if self.sender().isChecked():
            self.lenP.setEnabled(True)
            self.lenQ.setEnabled(True)
            self.lenA.setEnabled(True)
            self.lenB.setEnabled(False)
        self.check_disable()

    # onClick for slidercrank radio
    @pyqtSlot()
    def slider_crank(self):
        if self.sender().isChecked():
            self.lenP.setEnabled(False)
            self.lenQ.setEnabled(False)
            self.lenA.setEnabled(True)
            self.lenB.setEnabled(True)
        self.check_disable()

    # onClick for sixbar radio
    @pyqtSlot()
    def six_bar(self):
        if self.sender().isChecked():
            self.lenP.setEnabled(True)
            self.lenQ.setEnabled(True)
            self.lenA.setEnabled(True)
            self.lenB.setEnabled(True)
        self.check_disable()

    # main Simulate button
    @pyqtSlot()
    def add_element(self):
        if self.fourbar.isChecked():
            self.plot_figure.draw_graph_fourbar(int(self.lenA.text()), 0,
                                        int(self.lenP.text()), int(self.lenQ.text()), int(self.omega.text()))
            print(self.lenA.text(),self.lenP.text(),self.lenQ.text(),self.omega.text())

        if self.slidercrank.isChecked():
            self.plot_figure.draw_graph_slider(int(self.lenA.text()), int(self.lenB.text()),int(self.omega.text()))
            print(self.lenA.text(),self.lenB.text(),self.omega.text())

        if self.sixbar.isChecked():
            self.plot_figure.draw_graph_sixbar(int(self.lenA.text()), int(self.lenB.text()),
                                        int(self.lenP.text()), int(self.lenQ.text()), int(self.omega.text()))
            print(self.lenA.text(),self.lenB.text(),self.lenP.text(),self.lenQ.text(),self.omega.text())

    # enable add button after required inputs are met
    @pyqtSlot()
    def check_disable(self):
        if self.fourbar.isChecked():
            if not self.lenA.text() or not self.lenP.text() or not self.lenQ.text() or not self.omega.text():
                self.add.setEnabled(False)
            else:
                self.add.setEnabled(True)

        if self.slidercrank.isChecked():
            if not self.lenA.text() or not self.lenB.text() or not self.omega.text():
                self.add.setEnabled(False)
            else:
                self.add.setEnabled(True)

        if self.sixbar.isChecked():
            if not self.lenA.text() or not self.lenB.text() or not self.lenP.text() or not self.lenQ.text() or not self.omega.text():
                self.add.setEnabled(False)
            else:
                self.add.setEnabled(True)

    @pyqtSlot()
    def quit_application(self):
        QApplication.quit()

    # sets the default values i.e.six bar constant velocity
    @pyqtSlot()
    def reset_values(self):
        # a=26,b=79,p=18,q=22,omega=2
        self.lenA.setText("26")
        self.lenB.setText("79")
        self.lenP.setText("18")
        self.lenQ.setText("22")
        self.omega.setText("2")
        self.sixbar.setChecked(True)

    # clears all input fields
    @pyqtSlot()
    def clear_inputs(self):
        self.lenA.setText("")
        self.lenB.setText("")
        self.lenP.setText("")
        self.lenQ.setText("")
        self.omega.setText("")
        self.fourbar.setChecked(True)
        self.plot_figure.clear_plot()


class analWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.a=26
        self.b=76
        self.p=18
        self.q=22
        self.omega=2

        # Right
        # self.plot_figure = plot_figure(width=8, height=4)
        # self.right = QVBoxLayout()
        # self.right.addWidget(self.plot_figure)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(14)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["x-component", "y-component","z-component"])
        # Va,Wba,Vb,Aa,ALPHAba,Ab,Aba,Ac1,Ac2,Fo,Fa,Fb,N,T
        self.tableWidget.setVerticalHeaderLabels(["Velocity_a", "Omega_ab","Velocity_b","Acceleration_a","Alpha_ab","Acceleration_b","Acceleration_ab","Acceleration_c1","Acceleration_c2","Force_o","Force_a","Force_b","N","T"])
        # self.tableWidget.setItem(0,0, QTableWidgetItem("as"))
        # self.tableWidget.setItem(0,1, QTableWidgetItem("Ceddll (1,2)"))
        # self.tableWidget.setItem(0,2, QTableWidgetItem("Ceddll (1,2)"))
        # for i in range(10):
        #     self.tableWidget.setItem(i,0, QTableWidgetItem("as"))
        #     self.tableWidget.setItem(i,1, QTableWidgetItem("as"))
        #     self.tableWidget.setItem(i,2, QTableWidgetItem("as"))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # # Left: selectMechanism radio buttons
        # self.fourbar = QRadioButton("Four bar")
        # self.slidercrank = QRadioButton("Slider crank")
        # self.sixbar = QRadioButton("Six bar")

        # self.selectMechanism = QHBoxLayout()
        # self.selectMechanism.addWidget(self.fourbar)
        # self.selectMechanism.addWidget(self.slidercrank)
        # self.selectMechanism.addWidget(self.sixbar)

        # self.fourbar.setChecked(True)
        # self.fourbar.toggled.connect(self.four_bar)
        # self.slidercrank.toggled.connect(self.slider_crank)
        # self.sixbar.toggled.connect(self.six_bar)

        # left: link lengths input
        self.lenA = QLineEdit()
        self.lenAbox = QHBoxLayout()
        self.lenAbox.addWidget(QLabel("Link A length"))
        self.lenAbox.addWidget(self.lenA)
        self.lenAbox.addWidget(QLabel("m"))

        self.lenB = QLineEdit()
        self.lenBbox = QHBoxLayout()
        self.lenBbox.addWidget(QLabel("Link B length"))
        self.lenBbox.addWidget(self.lenB)
        self.lenBbox.addWidget(QLabel("m"))

        self.crankA = QLineEdit()
        self.crankAngle = QHBoxLayout()
        self.crankAngle.addWidget(QLabel("Crank angle"))
        self.crankAngle.addWidget(self.crankA)
        self.crankAngle.addWidget(QLabel("degrees"))

        # self.lenP = QLineEdit()
        # self.lenPbox = QHBoxLayout()
        # self.lenPbox.addWidget(QLabel("Link P length"))
        # self.lenPbox.addWidget(self.lenP)
        # self.lenPbox.addWidget(QLabel("cm"))

        # self.lenQ = QLineEdit()
        # self.lenQbox = QHBoxLayout()
        # self.lenQbox.addWidget(QLabel("Link Q length"))
        # self.lenQbox.addWidget(self.lenQ)
        # self.lenQbox.addWidget(QLabel("cm"))

        self.omega = QLineEdit()
        self.omegabox = QHBoxLayout()
        self.omegabox.addWidget(QLabel("Angular speed"))
        self.omegabox.addWidget(self.omega)
        self.omegabox.addWidget(QLabel("rad/s"))


        # left
        self.description = QLineEdit()
        self.price = QLineEdit()
        self.add = QPushButton("Calculate")
        # Disabling 'Add' button
        # self.add.setEnabled(False)
        self.reset = QPushButton("Reset")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")

        self.left = QVBoxLayout()
        # self.left.addWidget(QLabel("Select the mechanism"))
        # self.left.addLayout(self.selectMechanism)
        self.left.addWidget(QLabel("Specify the required params (in SI units)"))
        self.left.addLayout(self.lenAbox)
        self.left.addLayout(self.lenBbox)
        self.left.addLayout(self.crankAngle)
        # self.left.addLayout(self.lenPbox)
        # self.left.addLayout(self.lenQbox)
        self.left.addLayout(self.omegabox)
        self.left.addWidget(self.add)
        self.left.addWidget(self.reset)
        self.left.addWidget(self.clear)
        self.left.addWidget(self.tableWidget)
        self.left.addWidget(self.quit)

        # Signals and pyqtSlots
        self.add.clicked.connect(self.add_element)
        self.quit.clicked.connect(self.quit_application)
        self.reset.clicked.connect(self.reset_values)
        self.clear.clicked.connect(self.clear_inputs)


        # # check when to enable Simulate button
        # self.lenA.textChanged[str].connect(self.check_disable)
        # self.lenB.textChanged[str].connect(self.check_disable)
        # # self.lenP.textChanged[str].connect(self.check_disable)
        # # self.lenQ.textChanged[str].connect(self.check_disable)
        # self.omega.textChanged[str].connect(self.check_disable)
        # # self.fourbar.


        # QWidget Layout
        self.layout = QHBoxLayout()

        # self.layout.addWidget(self.table)
        self.layout.addLayout(self.left)
        # self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)


    # # onClick for fourbar radio
    # @pyqtSlot()
    # def four_bar(self):
    #     if self.sender().isChecked():
    #         self.lenP.setEnabled(True)
    #         self.lenQ.setEnabled(True)
    #         self.lenA.setEnabled(True)
    #         self.lenB.setEnabled(False)
    #     self.check_disable()

    # # onClick for slidercrank radio
    # @pyqtSlot()
    # def slider_crank(self):
    #     if self.sender().isChecked():
    #         self.lenP.setEnabled(False)
    #         self.lenQ.setEnabled(False)
    #         self.lenA.setEnabled(True)
    #         self.lenB.setEnabled(True)
    #     self.check_disable()

    # # onClick for sixbar radio
    # @pyqtSlot()
    # def six_bar(self):
    #     if self.sender().isChecked():
    #         self.lenP.setEnabled(True)
    #         self.lenQ.setEnabled(True)
    #         self.lenA.setEnabled(True)
    #         self.lenB.setEnabled(True)
    #     self.check_disable()

    # main Simulate button
    @pyqtSlot()
    def add_element(self):
        # print(self.lenA.text(),self.crankA.text())
        paramValues = sliderCrank([float(self.lenA.text()),0.03,0.01],[float(self.lenB.text()),0.03,0.01],m3=0.25,Wao=float(self.omega.text()), theta=float(self.crankA.text()),rho=2710,g=9.81)
        # print(paramValues)
        # print(paramValues.shape)
        for i in range(paramValues.shape[0]):
            # print(paramValues[i][0])
            self.tableWidget.setItem(i,0, QTableWidgetItem(str(paramValues[i][0])))
            self.tableWidget.setItem(i,1, QTableWidgetItem(str(paramValues[i][1])))
            self.tableWidget.setItem(i,2, QTableWidgetItem(str(paramValues[i][2])))
            # self.tableWidget.setItem(i,0, QTableWidgetItem("agvhvs"))
            # self.tableWidget.setItem(i,1, QTableWidgetItem("agvhvs"))
            # self.tableWidget.setItem(i,2, QTableWidgetItem("agvhvs"))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # if self.fourbar.isChecked():
        #     self.plot_figure.draw_graph_fourbar(int(self.lenA.text()), 0,
        #                                 int(self.lenP.text()), int(self.lenQ.text()), int(self.omega.text()))
        #     print(self.lenA.text(),self.lenP.text(),self.lenQ.text(),self.omega.text())

        # if self.slidercrank.isChecked():
        #     self.plot_figure.draw_graph_slider(int(self.lenA.text()), int(self.lenB.text()),int(self.omega.text()))
        #     print(self.lenA.text(),self.lenB.text(),self.omega.text())

        # if self.sixbar.isChecked():
        #     self.plot_figure.draw_graph_sixbar(int(self.lenA.text()), int(self.lenB.text()),
        #                                 int(self.lenP.text()), int(self.lenQ.text()), int(self.omega.text()))
        #     print(self.lenA.text(),self.lenB.text(),self.lenP.text(),self.lenQ.text(),self.omega.text())

    # # enable add button after required inputs are met
    # @pyqtSlot()
    # def check_disable(self):
    #     if self.fourbar.isChecked():
    #         if not self.lenA.text() or not self.lenP.text() or not self.lenQ.text() or not self.omega.text():
    #             self.add.setEnabled(False)
    #         else:
    #             self.add.setEnabled(True)

    #     if self.slidercrank.isChecked():
    #         if not self.lenA.text() or not self.lenB.text() or not self.omega.text():
    #             self.add.setEnabled(False)
    #         else:
    #             self.add.setEnabled(True)

    #     if self.sixbar.isChecked():
    #         if not self.lenA.text() or not self.lenB.text() or not self.lenP.text() or not self.lenQ.text() or not self.omega.text():
    #             self.add.setEnabled(False)
    #         else:
    #             self.add.setEnabled(True)

    @pyqtSlot()
    def quit_application(self):
        QApplication.quit()

    # sets the default values i.e.six bar constant velocity
    @pyqtSlot()
    def reset_values(self):
        # a=26,b=79,p=18,q=22,omega=2
        self.lenA.setText("0.26")
        self.lenB.setText("0.79")
        self.crankA.setText("0")
        # self.lenP.setText("18")
        # self.lenQ.setText("22")
        self.omega.setText("2")
        # self.sixbar.setChecked(True)

    # clears all input fields
    @pyqtSlot()
    def clear_inputs(self):
        self.lenA.setText("")
        self.lenB.setText("")
        self.crankA.setText("")
        # self.lenP.setText("")
        # self.lenQ.setText("")
        self.omega.setText("")
        # self.fourbar.setChecked(True)
        # self.plot_figure.clear_plot()


class num_win(QMainWindow):
    switch_window = pyqtSignal()
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("OpenKDM")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        back_action = QAction("Back", self)
        back_action.setShortcut("Ctrl+B")
        back_action.triggered.connect(self.back)

        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(back_action)
        self.setCentralWidget(widget)

    @pyqtSlot()
    def exit_app(self):
        QApplication.quit()

    @pyqtSlot()
    def back(self):
        self.switch_window.emit()


class anal_win(QMainWindow):
    switch_window = pyqtSignal()
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("OpenKDM")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        back_action = QAction("Back", self)
        back_action.setShortcut("Ctrl+B")
        back_action.triggered.connect(self.back)

        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(back_action)
        self.setCentralWidget(widget)

    @pyqtSlot()
    def exit_app(self):
        QApplication.quit()

    @pyqtSlot()
    def back(self):
        self.switch_window.emit()


# class anal_win(QMainWindow):
#     switch_window = pyqtSignal()
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.setWindowTitle('Window Two')

#         layout = QGridLayout()

#         self.button = QPushButton('Back')
#         self.button.clicked.connect(self.back)

#         layout.addWidget(self.button)

#         self.setLayout(layout)

#     @pyqtSlot()
#     def back(self):
#         self.switch_window.emit()


class main_win(QWidget):

    switch_window = pyqtSignal()
    switch_window2 = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('OpenKDM')

        layout = QVBoxLayout()

        self.labelImage = QLabel(self)
        self.pixmap = QPixmap(appctxt.get_resource("logo_banner.png"))
        self.pixmap=self.pixmap.scaledToWidth(512)  # image size
        self.labelImage.setPixmap(self.pixmap)
        self.labelImage.setAlignment(Qt.AlignCenter)

        self.button = QPushButton('Numerical Simulation')
        self.button.clicked.connect(self.login1)

        self.button2 = QPushButton('Analytical Solutions')
        self.button2.clicked.connect(self.login2)
        self.button.resize(100,32)
        # self.button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        # self.button2.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)

        self.button.setEnabled(False)
        self.button2.setEnabled(False)

        self.intro_text = """The study of the 'Kinematics and Dynamics of Machinery' (IITT course code: ME2206) lies at the very core of a mechanical engineering background. Although, little has changed in the way the subject is presented, our methodology brings the subject alive and current. We present the design and fabrication of a novel experimental setup for carrying out static, kinematic and dynamic analysis of three different mechanisms in a single setup. The mechanism is designed to be configurable to three different types of mechanisms namely - double crank, slider crank and a six bar mechanism depending on the use case. The mechanism has retrofitted parts (different link lengths and sliders) to facilitate multiple experiments in the same setup. The learner gets to 'play' with the mechanism parameters and immediately understand their effects. This will enhance one’s grasp of the concepts and the development of analytical skills. Hence greatly supplementing and reinforcing the theoretical understanding of the undergraduate students taking the course."""

        self.license_text = """MIT License

Copyright (c) 2020 Aakash Yadav

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. """

        self.text = QLabel()
        self.text.setText(self.intro_text)
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignCenter)

        self.license_layout = QVBoxLayout()
        self.license = QPlainTextEdit(self.license_text)
        self.license.setReadOnly(True)
        self.license_layout.addWidget(self.license)
        self.license_layout.setContentsMargins(200, 0, 200, 0)

        self.agree_box = QCheckBox("I have read the license agreement")
        # self.agree_box.setChecked(True)
        self.agree_box.stateChanged.connect(self.license_agree)
        self.license_layout.addWidget(self.agree_box)


        layout.addWidget(self.labelImage)
        layout.addWidget(self.text)
        layout.addLayout(self.license_layout)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.setSpacing(20)
        layout.setContentsMargins(200, 10, 200, 10) #left, top, right, bottom


        self.setLayout(layout)

    @pyqtSlot()
    def login1(self):
        self.switch_window.emit()

    @pyqtSlot()
    def login2(self):
        self.switch_window2.emit()

    @pyqtSlot()
    def license_agree(self):
        if self.sender().isChecked():
            self.button.setEnabled(True)
            self.button2.setEnabled(True)
        else:
            self.button.setEnabled(False)
            self.button2.setEnabled(False)


class Controller:

    def __init__(self):
        pass

    def show_main(self):
        self.main_win = main_win()
        widget = Widget()
        self.num_win = num_win(widget)
        analwidget = analWidget()
        self.anal_win = anal_win(analwidget)
        self.main_win.switch_window.connect(self.show_numerical)
        self.main_win.switch_window2.connect(self.show_analytical)
        self.num_win.close()
        self.anal_win.close()
        self.main_win.showMaximized()

    def show_numerical(self):
        self.num_win.switch_window.connect(self.show_main)
        self.main_win.close()
        self.num_win.showMaximized()

    def show_analytical(self):
        self.anal_win.switch_window.connect(self.show_main)
        self.main_win.close()
        self.anal_win.showMaximized()


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext 
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
