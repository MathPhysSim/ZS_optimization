from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal


import numpy as np
import pyjapc
import ParameterSetting as pc
import ObservableClass as ob
import GetOptimalMultiValueThreadClass as gOVThread
import ListSelectorClass as lsclass

from sceleton import Ui_MainWindow


class MyApp(QMainWindow, Ui_MainWindow):

    japc = pyjapc.PyJapc(incaAcceleratorName="SPS", noSet=False)
    
#    japc.rbacLogin()
    averageNrValue = 5.
    parameterClass = pc.ParameterClass(japc)
    algorithmSelection = 'Powell'
    observableMethodSelection = 'Maximum'

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        Ui_MainWindow.__init__(self)

        self.imageLabel.setPixmap(QPixmap("Powell.png"))
        self.imageLabel.setScaledContents(True)

        self.runOptimizationButton.clicked.connect(self.runOptimization)
        self.runOptimizationButton.setEnabled(False)

        self.buttonRestoreOldValues.clicked.connect(
                self.buttonRestoreOldValuesPressed)

        self.spinBoxXTolValue.valueChanged.connect(
                self.spinBoxXTolValueChanged)
        self.spinBoxFTolValue.valueChanged.connect(
                self.spinBoxFTolValueChanged)
        self.doubleSpinBoxXSmall.valueChanged.connect(
                self.doubleSpinBoxXSmallChanged)
#        self.spinBoxAverageNr.valueChanged.connect(
#                self.spinBoxAverageNrChanged)
#        self.doubleSpinBoxStartTime.valueChanged.connect(
#                self.doubleSpinBoxStartTimeChanged)
#        self.doubleSpinBoxEndTime.valueChanged.connect(
#                self.doubleSpinBoxEndTimeChanged)
        self.doubleSpinBoxStartDirection.valueChanged.connect(
                self.doubleSpinBoxStartDirectionChanged)
        
#        self.doubleSpinBoxObservableStartTime.valueChanged.connect(
#                self.doubleSpinBoxObservableStartTimeChanged)
#        self.doubleSpinBoxObservableEndTime.valueChanged.connect(
#                self.doubleSpinBoxObservableEndTimeChanged)
        self.japc.setSelector("SPS.USER.SFTPRO1")
        self.japc.subscribeParam("SPSQC/INTENSITY.PERFORMANCE",
                                 self.onValueRecieved)

        self.ob = ob.ObservableClass(self.japc, self.averageNrValue)


#        self.visualizeData()
        self.xTol = 0.2
        self.fTol = 0.1
        self.xSmall = 0.01
        self.isSimulation = False
        self.x0 = []
        self.selectedElement = []
        self.observableTime = np.array([0,0])

        self.spinBoxXTolValue.setValue(self.xTol)
        self.spinBoxFTolValue.setValue(self.fTol)
        self.doubleSpinBoxXSmall.setValue(self.xSmall)
#        self.spinBoxAverageNr.setValue(self.averageNrValue)
        
        self.buttonGroup.buttonClicked.connect(self.buttonGroupSelected)
        self.algorithmSelection = self.buttonGroup.checkedButton().text()

        self.buttonGroupObservable.\
        buttonClicked.connect(self.buttonGroupObservableSelected)
        self.observableMethodSelection = self.buttonGroupObservable.\
        checkedButton().text()
        
        self.listSelector = lsclass.ListSelector()

        for itemName in self.listSelector.getItems():
            item = QListWidgetItem(itemName)
#            if item.text() in self.listSelector.markedItems:
#                item.setBackground(QColor(255, 0, 0))
#            else:
            item.setBackground(QColor(0, 255, 0))
            self.listWidget.addItem(item)
        self.listWidget.sortItems()   
        self.listWidget.itemSelectionChanged.connect(self.itemsChanged)
        self.listWidget.itemClicked.connect(self.itemSelected)
        for itemName in ["SPS.USER.SFTPRO1", "SPS.USER.SFTPRO2"]:
            item = QListWidgetItem(itemName)
            self.listWidgetCycle.addItem(item)
        self.listWidgetCycle.itemClicked.connect(self.itemsClickedCycle)
        

    def itemsClickedCycle(self, id):
        
        self.japc.clearSubscriptions()
        self.japc.setSelector(id.text())  
        self.ob.selector = self.japc.getSelector()
        print("Set cycle:", self.ob.selector)
        self.japc.subscribeParam("SPSQC/INTENSITY.PERFORMANCE",
                                 self.onValueRecieved)
 
    def itemsChanged(self):  # s is a str

        currentSelection = [item.text() for item in
                            self.listWidget.selectedItems()]
        self.listSelector.setSelection(currentSelection)

        if len(self.listSelector.selectionList) > 0:
            self.runOptimizationButton.setEnabled(True)
        else:
            self.runOptimizationButton.setEnabled(False)

    def itemSelected(self, id):
        self.selectedElement = id.text()
        selectedEntry = self.listSelector.parameterList[self.selectedElement]
        self.doubleSpinBoxStartDirection.setValue(
                    float(selectedEntry['startDirection']))   
#        if (selectedEntry['type'] == 'functionSquare')|(self.selectedElement=="ETL.GSBHN10/KICK")|(selectedEntry['type'] == 'functionList'):
#            self.doubleSpinBoxStartTime.setEnabled(True)
#            self.doubleSpinBoxEndTime.setEnabled(True)
#
#            self.doubleSpinBoxStartTime.setValue(
#                    float(selectedEntry['time'][0]))
#            self.doubleSpinBoxEndTime.setValue(
#                    float(selectedEntry['time'][1]))
#
#        else:
#            self.doubleSpinBoxStartTime.setEnabled(False)
#            self.doubleSpinBoxEndTime.setEnabled(False)
            
  

    def doubleSpinBoxStartTimeChanged(self):
        selectedEntry = self.listSelector.parameterList[self.selectedElement]
#        print(selectedEntry['time'][1])
        self.listSelector.setItemTime(self.selectedElement,
                                      [self.doubleSpinBoxStartTime.value(),
                                       selectedEntry['time'][1]])
#        self.doubleSpinBoxEndTime.setMinimum(
#                self.doubleSpinBoxStartTime.value()+25.)

    def doubleSpinBoxEndTimeChanged(self):
        selectedEntry = self.listSelector.parameterList[self.selectedElement]
#        print(selectedEntry['time'][1])
        self.listSelector.setItemTime(self.selectedElement,
                                      [selectedEntry['time'][0],
                                       self.doubleSpinBoxEndTime.value()])

    def doubleSpinBoxStartDirectionChanged(self):
        selectedEntry = self.listSelector.parameterList[self.selectedElement]
#        print(selectedEntry['time'][1])
        self.listSelector.setItemStartDirection(self.selectedElement,
                                       self.doubleSpinBoxStartDirection.value())

    def doubleSpinBoxObservableStartTimeChanged(self):
#        print("touchme1")
        
        self.ob.timeInterval[0] = self.doubleSpinBoxObservableStartTime.value()
#        print(self.ob.timeInterval)
        self.doubleSpinBoxObservableEndTime.\
        setMinimum(self.ob.timeInterval[0]+1)

    def doubleSpinBoxObservableEndTimeChanged(self):
#        print("touchme2")
        
        self.ob.timeInterval[1] = self.doubleSpinBoxObservableEndTime.value()
#        print(self.ob.timeInterval)
#        self.doubleSpinBoxObservableStartTime.\
#        setMaximum(self.ob.timeInterval[1])

    def buttonGroupSelected(self, id):
        self.algorithmSelection = id.text()

    def buttonGroupObservableSelected(self, id):
        self.observableMethodSelection = id.text()
#        if (self.observableMethodSelection == 'Area') |\
#           (self.observableMethodSelection == 'Transmission'):
#            self.doubleSpinBoxObservableEndTime.\
#            setMinimum(self.ob.timeInterval[0]+1)
#            self.doubleSpinBoxObservableStartTime.setEnabled(True)
#            self.doubleSpinBoxObservableEndTime.setEnabled(True)
#        else:
#            self.doubleSpinBoxObservableStartTime.setEnabled(False)
#            self.doubleSpinBoxObservableEndTime.setEnabled(False)
        self.ob.method = id.text()

    def buttonRestoreOldValuesPressed(self):
        self.setValues(self.x0)

    def spinBoxXTolValueChanged(self):
        self.xTol = self.spinBoxXTolValue.value()

    def spinBoxFTolValueChanged(self):
        self.fTol = self.spinBoxFTolValue.value()
    
    def doubleSpinBoxXSmallChanged(self):
        self.xSmall = self.doubleSpinBoxXSmall.value()  

    def spinBoxAverageNrChanged(self):
        self.averageNrValue = self.spinBoxAverageNr.value()
        self.ob.dataLength = self.averageNrValue

    def onValueRecieved(self, parameterName, newValue):
        self.ob.setValue(newValue)  # /normVal
#        print('subscibtionRuns')

    def runOptimization(self):
        if self.runOptimizationButton.text() == "Start":
            self.clearPlot()
            self.listWidgetCycle.setEnabled(False)
#            print("pass0")
            self.parameterClass.resetParameters()
#            print("pass1")
#            print(self.listSelector.getSelectedItemsDict())
#            print("pass1x")
            self.parameterClass.addParameters(
                    self.listSelector.getSelectedItemsDict())
#            print("pass2")
            self.x0 = self.parameterClass.getStartVector()
#            print("pass3")
            self.getOptimalValueThread = gOVThread.Getoptimalmultivaluethread(
                    self.parameterClass, self.ob, self.algorithmSelection,
                    self.xTol, self.fTol, self.xSmall ,self.isSimulation)
#            print("pass4")
            self.getOptimalValueThread.signals.setSubscribtion.connect(
                    self.setSubscribtion)
            self.getOptimalValueThread.signals.setValues.connect(
                    self.setValues)
            self.getOptimalValueThread.signals.drawNow.\
                connect(self.visualizeData)
            self.getOptimalValueThread.signals.jobFinished.connect(self.done)
            self.getOptimalValueThread.start()
            self.runOptimizationButton.setText('Cancel')
            
            self.getOptimalValueThread.signals.showDataOK.\
                connect(self.changeDataOKLabel)
                
        elif self.getOptimalValueThread.isRunning():

            self.getOptimalValueThread.cancelFlag = True
            self.getOptimalValueThread.wait()
            self.getOptimalValueThread.quit()
            self.getOptimalValueThread.wait()
            self.listWidgetCycle.setEnabled(True)
            self.runOptimizationButton.setText('Start')
            
    def changeDataOKLabel(self, text):
        self.labelDataOK.setText(text) 
        if self.labelDataOK.text() == 'OK':
            self.labelDataOK.setStyleSheet('color: green')
        elif self.labelDataOK.text() == 'Acquisition ok?':
            self.labelDataOK.setStyleSheet('color: white')
        else:
            self.labelDataOK.setStyleSheet('color: red')
            
    def setValues(self, x):
        #print('Would send', x)
        #x = [2.5]
        #print(x)        
        self.parameterClass.setNewValues(x)

    def done(self):
        print("DONE")
        self.runOptimizationButton.setText('Start')
        QMessageBox.information(self, 'Scan succsessful', "Final values at: " +
                                str(self.parameterClass.getValues()) +
                                "\nInitial values: " +
                                str(self.x0),
                                QMessageBox.Close)

    def setSubscribtion(self, suscribtionBool):
        if suscribtionBool:
            self.japc.startSubscriptions()
        else:
            self.japc.stopSubscriptions()

    def clearPlot(self):
        self.plotWidget.canvas.axs[1].clear()
        self.plotWidget.canvas.axs[0].clear()

    def visualizeData(self):
        #print("draw")
        plotFrame = self.getOptimalValueThread.parameterEvolution.iloc[:, 1:].T
        self.plotWidget.canvas.axs[1].clear()
        self.plotWidget.canvas.axs[0].clear()
        if plotFrame.shape[0] > 1:
            plotFrame.iloc[:, :-1].plot(ax=self.plotWidget.canvas.axs[0])
            plotFrame.iloc[:, -1].plot(ax=self.plotWidget.canvas.axs[1])

        self.plotWidget.canvas.axs[0].set_title('Parameter evolution')
        self.plotWidget.canvas.axs[1].set_title('Observable')
        self.plotWidget.canvas.axs[0].set_xlabel('Nr of changes')
        self.plotWidget.canvas.axs[1].set_xlabel('Nr of changes')
        self.plotWidget.canvas.axs[0].set_ylabel('parameters (a.u.)')
        self.plotWidget.canvas.axs[1].\
        set_ylabel(self.observableMethodSelection)

        self.plotWidget.canvas.fig.tight_layout()
        self.plotWidget.canvas.draw()
        #print("draw exit")
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.setSubscribtion(False)
            event.accept()
        else:
            event.ignore()
