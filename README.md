- `sudo apt install python3-pyqt5` para instalar PyQt5 (60MB aprox.)
- `sudo python3 main.py` para correr.   
(requiere `sudo` porque usa el comando `iptables` para hacer todas las operaciones)

*Opcional:* `sudo apt install qttools5-dev-tools` para instalar editor visual Qt Designer

Si usás el Qt Designer, una vez exportada una UI a un archivo `*.ui`
se traduce a python haciendo `pyuic5 EL_ARCHIVO.ui`

Programa:
![alt text](https://raw.githubusercontent.com/wencha/iptables-manager/master/capturas/main.png)

Qt Designer:
![alt text](https://raw.githubusercontent.com/wencha/iptables-manager/master/capturas/qt-designer.png)


