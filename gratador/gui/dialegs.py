from webbrowser import open_new_tab
from PyQt5 import uic, Qt
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLineEdit, QFrame,  QTreeWidget, QTreeWidgetItem,
                             QHBoxLayout, QVBoxLayout, QBoxLayout)
from ..tools import getconfig, setconfig, delconfig
from ..grataBSK_5_main_2 import Pagina


class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('./gui/principal.ui',self)
        self.setBaseSize(600,600)
        self.setWindowTitle('GrataBSK')
        self.bt_add.clicked.connect(self.afegeix)
        self.bt_remove.clicked.connect(self.borra)
        self.bt_busca.clicked.connect(self.busca)
        self.llista.doubleClicked.connect(lambda : self.browser(self.llista.currentItem().text(0)))
        self.statusBar()
        self.pobla()

        self.show()

    def pobla(self):
        self.llista.clear()
        parent =self.llista.invisibleRootItem()
        col =0
        try:
            jocs = getconfig()
        except Exception as e:
            print(e)
            setconfig()
            jocs = getconfig()

        for joc, urls in jocs.items():
            print(joc,urls)
            s = QTreeWidgetItem(parent, [str(joc)])
            # s.setData(col, Qt.UserRole, 'Joc')
            for u in urls:
                row =  QTreeWidgetItem(s,[u])
                # row.setData(1, Qt.UserRole, 'Url')

    def afegeix(self):
        setconfig(*(self.text.text(),))
        self.pobla()

    def borra(self):
        joc = self.llista.currentItem().text(0)
        delconfig(*(joc,))
        self.pobla()

    def busca(self):
        p = Pagina()
        item = self.llista.currentItem()
        if item:
            self.statusBar().showMessage('buscant {}...'.format(item.text(0)))
            p.buscar(item.text(0))
            self.statusBar().showMessage('')
        else:
            for joc in getconfig().keys():
                self.statusBar().showMessage('buscant {}...'.format(joc))
                p.buscar(joc)
            self.statusBar().showMessage('')
        self.pobla()

    def browser(self, url):
        open_new_tab(url)