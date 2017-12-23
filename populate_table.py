import mysql.connector as con
import os
import sys
import wow.dbc as dbc
import wow.dbc.format_import as format_import
from wow.simple_file import load

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


def main():
    try:
        fn = sys.argv[1]
    except IndexError as e:
        print("usage: {} <filename>".format(sys.argv[0]))
        sys.exit(1)

    f = load(fn)
    dbc_name = os.path.basename(fn)

    formatter = format_import.FormatImport()
    rec_format = formatter.get_format(dbc_name)
    inst = dbc.DbcFile(rec_format)
    inst.load(f)

    columns = formatter.get_mysql_columns(dbc_name)

    table_name = dbc_name[:-4]

    insert = build_row_insert_statement(table_name, columns)

    server = con.connect(**config)
    c = server.cursor()

    c.executemany(insert, inst.records)

    server.commit()
    c.close()
    server.close()

if __name__ == '__main__':
    main()
