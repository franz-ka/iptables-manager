# Referencia de PyQt widgets - https://doc.qt.io/qtforpython/PySide2/QtWidgets/

import subprocess
import os
import sys
import datetime
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow

window = None
iptable_names = None
iptable_protocols = ['all', 'tcp', 'udp', 'icmp', 'sctp']
iptable_acctions = ['ACCEPT', 'DROP', 'REJECT']

def run_cmd_fast(cmd):    
    os.system(cmd)    
    window.log_cmd(cmd)
    
def run_cmd(cmd):    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    
    window.log_cmd(cmd)
    
    return out

def run_cmd_splitlines(cmd):
    out = run_cmd(cmd)
    return out.decode('utf8').splitlines()

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        
        self.exclude_docker = None
        self.exclude_grep = None
        self.checkBox.stateChanged.connect(self.updateDockerExclude)
        
        self.comboBox.currentIndexChanged.connect(self.updateChainList)
        
        self.listWidget.currentTextChanged.connect(self.updateRulesList)
        
        self.buttonAddRegla.clicked.connect(self.addRegla) 
        
    def log_cmd(self, cmd):    
        tstamp = datetime.datetime.now().strftime('%X')
        self.listLog.insertItem(0, f'[{tstamp}]~$ {cmd}')
        
    def error_msg(self, msg):        
        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setIcon(QtWidgets.QMessageBox.Critical)
        msgbox.setText("Error")
        msgbox.setInformativeText(msg)
        msgbox.setWindowTitle("Error")
        msgbox.show()
        
    def updateDockerExclude(self):
        self.exclude_docker = self.checkBox.isChecked()
        self.exclude_grep = 'grep -vE "docker0|DOCKER|br-(762|b21|79a|613)|172\.(17|18|19|20|21)\.0"' if self.exclude_docker else 'cat'
        self.updateChainList()
        
    def updateChainList(self):
        self.listWidget.clear()
        self.listWidget_2.clear()
        
        selected_table = self.comboBox.currentText()
               
        if not selected_table:
            return
        
        print(selected_table)
        
        chains = run_cmd_splitlines(f'sudo iptables -t {selected_table} -nL | grep Chain | {self.exclude_grep} | cut -d" " -f2')
        
        self.listWidget.addItems(chains)
        
    def updateRulesList(self, selected_chain):
        self.listWidget_2.clear() 
               
        if not selected_chain:
            return
        
        selected_table = self.comboBox.currentText()
        print(selected_table, selected_chain)
        
        rules = run_cmd_splitlines(f'sudo iptables -t {selected_table} -S {selected_chain} | {self.exclude_grep}')
        
        self.listWidget_2.addItems(rules)
        
    def addRegla(self):
        selected_table = self.comboBox.currentText()
        if not selected_table:
            self.error_msg('Debe seleccionar una tabla y una chain')
            return
        
        selected_chain_item = self.listWidget.currentItem()
        if not selected_chain_item:
            self.error_msg('Debe seleccionar una chain')
            return
        selected_chain = selected_chain_item.text()
        
        conds = []
        
        from_ip_or_net = self.editAddIp.text()
        if from_ip_or_net:
            conds.append(f'-s {from_ip_or_net}')
            
        protocol = self.comboAddProtocolo.currentText()
        conds.append(f'-p {protocol}')
        
        to_port= self.editAddPuerto.text()
        if to_port:
            conds.append(f'--dport {to_port}')
            
        action = self.comboAddAccion.currentText()        
        conds.append(f'-j {action}')
        
        cmd = f'sudo iptables -t {selected_table} -A {selected_chain} ' + ' '.join(conds)
        run_cmd_fast(cmd)
        self.updateRulesList(selected_chain)


def main():
    global window, iptable_names
    
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
                
    
    iptable_names = run_cmd_splitlines('iptables-save | grep "^*" | cut -c2-')
    iptable_names.insert(0, '')
        
    window.comboBox.addItems(iptable_names)
    window.comboAddProtocolo.addItems(iptable_protocols)
    window.comboAddAccion.addItems(iptable_acctions)
    window.updateDockerExclude()

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
   