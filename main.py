import subprocess

proc = subprocess.Popen('iptables-save | grep "^*" | cut -c2-', stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
iptable_names = out.decode('utf8').splitlines()
#os.system('iptables-save | grep "^*" | cut -c2-')


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(667, 290)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 141, 32))
        self.comboBox.setObjectName("comboBox")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 141, 181))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(160, 50, 501, 181))
        self.listWidget_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.listWidget_2.setObjectName("listWidget_2")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(170, 11, 141, 31))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 667, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox.setText(_translate("MainWindow", "Excluír Docker"))


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        
        self.exclude_docker = None
        self.exclude_grep = None
        self.checkBox.stateChanged.connect(self.updateDockerExclude)
        
        self.comboBox.addItems(iptable_names)
        self.comboBox.currentIndexChanged.connect(self.updateChainList)
        
        self.listWidget.currentTextChanged.connect(self.updateRulesList)
        
        self.updateDockerExclude()
        
    def updateDockerExclude(self):
        self.exclude_docker = self.checkBox.isChecked()
        self.exclude_grep = 'grep -vE "docker0|DOCKER|br-(762|b21|79a|613)|172\.(17|18|19|20|21)\.0"' if self.exclude_docker else 'cat'
        self.updateChainList()
        
    def updateChainList(self):
        self.listWidget.clear()
        self.listWidget_2.clear()
        
        selected_table = self.comboBox.currentText()
        print(selected_table)
        
        proc = subprocess.Popen(f'sudo iptables -t {selected_table} -nL | grep Chain | {self.exclude_grep} | cut -d" " -f2', stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        chains = out.decode('utf8').splitlines()
        
        self.listWidget.addItems(chains)
        
    def updateRulesList(self, selected_chain):
        self.listWidget_2.clear()
        
        if not selected_chain:
            return
        selected_table = self.comboBox.currentText()
        print(selected_table, selected_chain)
        
        proc = subprocess.Popen(f'sudo iptables -t {selected_table} -S {selected_chain} | {self.exclude_grep}', stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        rules = out.decode('utf8').splitlines()
        
        self.listWidget_2.addItems(rules)


import sys
def window():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   window()