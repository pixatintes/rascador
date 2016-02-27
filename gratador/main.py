import sys


from gratador.gui.dialegs import Principal
from PyQt5.QtWidgets import QApplication
from grataBSK_5_main_2 import main


if __name__ == "__main__":

        total = len(sys.argv)
        print(total)
        if total == 3:
                arg2 = int(str(sys.argv[1]))
                arg1 = str(sys.argv[2])
                main(arg1, arg2)

        elif total == 2:
                arg1 = 'listtxt.txt'
                arg2 = int(str(sys.argv[1]))
                main(arg1, arg2)

        else:
            #Instancia para iniciar una aplicación
            app = QApplication(sys.argv)
            #Crear un objeto de la clasefrom gratador.gui.dialegs import Principal

            _ventana = Principal()
            #Mostra la ventana
            # _ventana.show()
            #Ejecutar la aplicación
            app.exec_()

