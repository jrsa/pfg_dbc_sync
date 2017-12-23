import mysql.connector as con
import sys
import wow.dbc as dbc
import wow.dbc.format_import as format_import



config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'dbctest2'
}


def build_table_create_statement(name, columns):
    create_stmt = "CREATE TABLE `{}` (".format(name)

    for n, t in columns:
        create_stmt += "`{}` {}, ".format(n, t)

    create_stmt += "  PRIMARY KEY (`id`)"
    create_stmt += ") ENGINE=InnoDB"

    return create_stmt


def main():
    try:
        name = sys.argv[1]
    except IndexError as e:
        print("usage: {} <dbc name>".format(sys.argv[0]))
        sys.exit(1)

    fi = format_import.FormatImport()
    column_types = fi.get_mysql_columns(name)

    server = con.connect(**config)
    c = server.cursor()

    create = build_table_create_statement(name, column_types)

    try:
        c.execute(create)
    except con.Error as err:
        print("Failed creating table: {}".format(err))

    server.commit()
    c.close()
    server.close()


if __name__ == '__main__':
    main()
