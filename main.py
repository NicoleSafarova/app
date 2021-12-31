import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QTableWidgetItem
from addEditCoffeeForm import Ui_Form


class DBSample(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.db")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_3.clicked.connect(self.add1)
        self.pushButton_4.clicked.connect(self.save1)
        self.dockWidget.close()
        self.dockWidget.move(230, 175)
        self.dockWidget_3.move(230, 175)
        self.dockWidget_3.close()
        self.select_data()

    def select_data(self):
        res = self.connection.cursor().execute("SELECT * from coffee").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Степень обжарки", "Молотый/в зернах",
                                                    "Вкуса", "Цена", "Объём"])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def add(self):
        self.dockWidget.show()

    def add1(self):
        if self.lineEdit.text() != "" and self.lineEdit_2.text() != "" and self.lineEdit_3.text() != "" and \
                self.lineEdit_4.text() != "" and self.lineEdit_5.text() != "" and self.lineEdit_6.text() != "":
            self.connection.cursor().execute(f"""INSERT INTO coffee(title, level, grounded, taste, Price, volume)
                            VALUES('{self.lineEdit.text()}', '{self.lineEdit_2.text()}', '{self.lineEdit_3.text()}',
                            '{self.lineEdit_4.text()}', {self.lineEdit_5.text()}, {self.lineEdit_6.text()})""").fetchall()
            self.select_data()
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            self.connection.commit()
            self.dockWidget.close()

    def save(self):
        self.dockWidget_3.show()
        m1 = [i.row() for i in self.tableWidget.selectedItems()][0]
        res = self.connection.cursor().execute(f"""SELECT * from coffee 
                       WHERE id = {self.tableWidget.item(m1, 0).text()}""").fetchall()
        self.m2 = 0
        for i in res:
            self.m2 = i[0]
            self.lineEdit_7.setText(i[1])
            self.lineEdit_8.setText(i[2])
            self.lineEdit_9.setText(i[3])
            self.lineEdit_10.setText(i[4])
            self.lineEdit_11.setText(str(i[5]))
            self.lineEdit_12.setText(str(i[6]))

    def save1(self):
        if self.lineEdit_7.text() != "" and self.lineEdit_8.text() != "" and self.lineEdit_9.text() != "" and \
                self.lineEdit_10.text() != "" and self.lineEdit_11.text() != "" and self.lineEdit_12.text() != "":
            self.connection.cursor().execute(f"""UPDATE coffee
                    SET title = '{self.lineEdit_7.text()}', level = '{self.lineEdit_8.text()}', 
                    grounded = '{self.lineEdit_9.text()}', taste = '{self.lineEdit_10.text()}', Price = {self.lineEdit_11.text()}, 
                    volume = {self.lineEdit_12.text()}
                     WHERE ID = {self.m2}""").fetchall()
            self.select_data()
            self.lineEdit_7.setText("")
            self.lineEdit_8.setText("")
            self.lineEdit_9.setText("")
            self.lineEdit_10.setText("")
            self.lineEdit_11.setText("")
            self.lineEdit_12.setText("")
            self.connection.commit()
            self.dockWidget_3.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())

