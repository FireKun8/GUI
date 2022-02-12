from pprint import isreadable
import serial as ps
import time
import pyqtgraph
from window_ui import *

arduino = ps.Serial(port='COM6', baudrate=9600, timeout=.1)

class DataThread(QtCore.QObject):
    dataChanged = QtCore.pyqtSignal(str)

    def __init__(self):
        super(DataThread, self).__init__()
        self.isRunning = True
        self.sleepTimer = QtCore.QTimer(self)
        self.sleepTimer.timeout.connect(self.run)
        self.sleepTimer.start(200)

    def run(self):
        while True and self.isRunning == True:
            if arduino.in_waiting:
                data = ((arduino.readline().strip()).decode("utf-8")).split("/")
                self.dataChanged.emit(data[0])

    def stop(self):
        self.isRunning = False

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        
        self.started = False

        self.btnStart.clicked.connect(self.startDataLog)
        self.btnStart_2.clicked.connect(self.finishDataLog)

    def timerUpdate(self):
        self.count += 1
        text = str(self.count / 10)
        self.lblTimerData.setText(text)
            
    def startDataLog(self):
        if self.started == False:
            self.counterArr = []
            self.count = 0

            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.timerUpdate)
            self.timer.start(100)

            self.dataUpdate = DataThread()
            self.thread = QtCore.QThread(self)
            self.dataUpdate.dataChanged.connect(self.testUpdate)
            self.dataUpdate.moveToThread(self.thread)
            self.thread.started.connect(self.dataUpdate.run)
            self.thread.start()

            self.curveAlt = self.grphAlt.plot()
            
            self.dataArrAlt = []
            self.dataArrAX = [] 
            self.started = True

    def finishDataLog(self):
        self.dataUpdate.stop()
        self.thread.quit()
        self.thread.wait()
        self.curveAlt.clear()
        self.timer.stop()
        self.started = False

    def testUpdate(self, data):
        self.lblAltData.setText(data)
        
        if data != "":
            self.dataArrAlt.append(float(data))
        else:
            self.dataArrAlt.append(0) 
        self.counterArr.append(self.count / 10)
        self.curveAlt.setData(self.counterArr, self.dataArrAlt)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()