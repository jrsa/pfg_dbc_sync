import mysql.connector
from mysql.connector import errorcode
import sys
import wow.dbc as dbc
import wow.dbc.format_import as fi
import wow.simple_file as sf

config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'dbctest2'
}


def main():
    try:
        name = sys.argv[1]
    except IndexError as e:
        print("usage: {} <dbc name>".format(sys.argv[0]))
        sys.exit(1)

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur = cnx.cursor()
        cur.execute("select * from {table};".format(table=name))
        records = cur.fetchall()

    finally:
        if cur:
            cur.close()
        if cnx:
            cnx.close()

    new_dbc = dbc.DbcFile(fi.FormatImport().get_format(name))
    new_dbc.records = records

    sf.save("{}.dbc".format(name), new_dbc.save())


if __name__ == '__main__':
    main()
