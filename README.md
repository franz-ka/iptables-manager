Miniprograma para ver más cómodamente las listas de reglas de `iptables`, todas sus tablas y chains asociadas.

Por ahora solo soporta ver las tablas, y agregar regla con: desde ip, protocolo y hacia puerto.

- `sudo apt install python3-pyqt5` para instalar PyQt5 (60MB aprox.)
- `sudo python3 main.py` para correr.   
(requiere `sudo` porque usa el comando `iptables` para hacer todas las operaciones)

Interfaz:

![alt text](https://raw.githubusercontent.com/wencha/iptables-manager/master/capturas/main.png)

-----

*Opcional:* `sudo apt install qttools5-dev-tools` para instalar editor visual Qt Designer

Si usás el Qt Designer, una vez exportada una UI a un archivo `*.ui`
lo exportás al archivo `ui.py` haciendo  `pyuic5 EL_ARCHIVO.ui > ui.py`

Qt Designer:

![alt text](https://raw.githubusercontent.com/wencha/iptables-manager/master/capturas/qt-designer.png)


