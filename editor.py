from math import sqrt
import mysql.connector as con
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import wow.dbc.format_import as format_import

config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'dbctest2'
}


def build_row_insert_statement(name, columns):
    statement = "INSERT INTO `{}` (".format(name)
    statement += ",".join(c[0] for c in columns)
    statement += ") VALUES ("
    statement += "%s, " * (len(columns) - 1)
    statement += "%s)"
    return statement


class Form(QWidget):

    def __init__(self, parent=None, tablename=None):
        super(Form, self).__init__(parent)

        self.textboxes = list()
        self.columns = format_import.FormatImport().get_mysql_columns(tablename)

        ly = QGridLayout()
        layout_grid_width = int(sqrt(len(self.columns)))

        for i, c in enumerate(self.columns):
            subly = QHBoxLayout()
            row = int(i / layout_grid_width)
            col = i % layout_grid_width
            title = QLabel(c[0])
            field = QLineEdit()
            subly.addWidget(title)
            subly.addWidget(field)
            self.textboxes.append(field)
            ly.addLayout(subly, row, col)

        button = QPushButton("insert")
        button.clicked.connect(self.insert)

        ly.addWidget(button)

        self.setLayout(ly)
        self.setWindowTitle(tablename)

    def insert(self):
        server = con.connect(**config)
        c = server.cursor()

        record = [f.text() for f in self.textboxes]
        # build insert statement without columns for textboxes which have been left blank

        try:
            c.execute(self.stmt, record)
        except mysql.connector.errors.DatabaseError as e:
            print(e)

        server.commit()
        c.close()
        server.close()


def main():
    app = QApplication(sys.argv)

    f = Form(tablename=sys.argv[1])
    f.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
