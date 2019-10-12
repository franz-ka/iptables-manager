import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow

window = None
iptable_names = None

def run_cmd(cmd):    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    
    if window:
        window.listLog.insertItem(0, '$ ' + cmd)
    
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


import sys
def main():
    global window, iptable_names
    
    iptable_names = run_cmd_splitlines('iptables-save | grep "^*" | cut -c2-')
    #os.system('iptables-save | grep "^*" | cut -c2-')
    
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
   