import os
import string
import secrets
from datetime import datetime

from numpy import float32, float64
import mysql.connector

from mypysql.get_login import sql_host, sql_user, sql_database, sql_password, sql_port

from mypysql.get_tables import create_tables, dynamically_named_tables


def make_insert_columns_str(table_name, columns, database):
    insert_str = F"INSERT INTO {database}.{table_name}("
    columns_str = ""
    for column_name in columns:
        columns_str += F"`{column_name}`, "
    insert_str += columns_str[:-2] + ") VALUES"
    return insert_str


def make_insert_many_columns_str(table_name, columns, database=None):
    insert_str = make_insert_columns_str(table_name=table_name, columns=columns, database=database) + "("

    for i in range(len(columns)):
        if i == 0:
            insert_str += "%s"
        else:
            insert_str += ", %s"
    return insert_str + ")"


def make_insert_values_str(values):
    values_str = ""
    for value in values:
        if isinstance(value, str):
            values_str += F"'{value}', "
        elif isinstance(value, (float, int, float32, float64)):
            values_str += F"{value}, "
        elif isinstance(value, bool):
            values_str += F"{int(value)}, "
        elif isinstance(value, datetime):
            values_str += F"'{str(value)}', "
        elif value is None:
            values_str += "NULL, "
        else:
            raise TypeError
    return "(" + values_str[:-2] + ")"


def insert_into_table_str(table_name, data, database=None):
    if database is None:
        database = sql_database
    columns = []
    values = []
    for column_name in sorted(data.keys()):
        columns.append(column_name)
        values.append(data[column_name])
    insert_str = make_insert_columns_str(table_name, columns, database)
    insert_str += make_insert_values_str(values) + ";"
    return insert_str


def generate_sql_config_file(user_name, password):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    new_configs_dir = os.path.join(dir_path, 'new_configs')
    if not os.path.isdir(new_configs_dir):
        os.mkdir(new_configs_dir)
    config_file_name = os.path.join(new_configs_dir, '../sql_config.py')
    with open(config_file_name, 'w') as f:
        f.write(F"""sql_host = "{sql_host}"\n""")
        f.write(F"""sql_port = "{sql_port}"\n""")
        f.write(F"""sql_database = "{sql_database}"\n""")
        f.write(F"""sql_user = "{user_name}"\n""")
        f.write(F"""sql_password = '''{password}'''\n""")
    print(F"New sql_config.py file at to: {config_file_name}")
    print(F"For user: {user_name}")


class OutputSQL:
    def __init__(self, auto_connect=True, verbose=True):
        self.verbose = verbose
        self.host = sql_host
        self.user = sql_user
        self.port = sql_port
        self.password = sql_password
        if auto_connect:
            self.open()
        else:
            self.connection = None
            self.cursor = None
        self.buffers = {}
        self.next_user_table_number = 1

    def open(self):
        if self.verbose:
            print("  Opening connection to the SQL Host Server:", sql_host)
            print("  under the user:", sql_user)
        self.connection = mysql.connector.connect(host=self.host,
                                                  user=self.user,
                                                  port=self.port,
                                                  password=self.password)
        self.cursor = self.connection.cursor()
        if self.verbose:
            print("    Connection established")

    def close(self):
        if self.verbose:
            print("  Closing SQL connection SQL Server.")
        self.cursor.close()
        self.connection.close()
        self.connection = None
        self.cursor = None
        if self.verbose:
            print("    Connection Closed")

    def open_if_closed(self):
        if self.connection is None:
            self.open()

    def new_user(self, user_name, password=None):
        if password is None:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(20))
        generate_sql_config_file(user_name=user_name, password=password)
        self.cursor.execute(F"""CREATE USER '{user_name}' IDENTIFIED BY '{password}';""")
        self.connection.commit()
        print(F"Successfully created the user {user_name} for host {self.host}")

    def make_new_super_user(self, user_name, password=None):
        self.new_user(user_name=user_name, password=password)
        self.cursor.execute(F"""GRANT ALL PRIVILEGES ON *.* TO '{user_name}';""")
        self.cursor.execute(F"""FLUSH PRIVILEGES;""")
        self.connection.commit()
        print(F"Successfully granted super user privileges to {user_name} for host {self.host}")

    def make_new_dba_user(self, user_name, password=None):
        self.new_user(user_name=user_name, password=password)
        if self.host == "localhost":
            self.cursor.execute(F"""GRANT ALL PRIVILEGES ON *.* TO '{user_name}' WITH GRANT OPTION;""")
        else:
            aws_grants = "GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, " + \
                         "ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, " +\
                         "REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, " + \
                         F"EVENT, TRIGGER ON *.* TO '{user_name}' WITH GRANT OPTION;"
            self.cursor.execute(aws_grants)
        self.cursor.execute(F"""FLUSH PRIVILEGES;""")
        self.connection.commit()
        print(F"Successfully granted the Database Administrator (DBA) role to {user_name} for host {self.host}")

    def make_new_server_user(self, user_name, password=None):
        self.new_user(user_name=user_name, password=password)
        if self.host == "localhost":
            self.cursor.execute(F"""GRANT ALL PRIVILEGES ON *.* TO '{user_name}';""")
        else:
            aws_grants = "GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, " + \
                         "ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, " +\
                         "REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, " + \
                         F"EVENT, TRIGGER ON *.* TO '{user_name}';"
            self.cursor.execute(aws_grants)
        self.cursor.execute(F"""FLUSH PRIVILEGES;""")
        self.connection.commit()
        print(F"Successfully granted the Server role to {user_name} for host {self.host}")

    def drop_if_exists(self, table_name, database=None, run_silent=False):
        if self.verbose and not run_silent:
            print("    Dropping (deleting if the table exists) the Table:", table_name)
        if database is None:
            database = sql_database
        self.cursor.execute(F"DROP TABLE IF EXISTS {database}.{table_name};")

    def creat_table(self, table_name, database=None, dynamic_type=None, run_silent=False):
        if database is None:
            database = sql_database
        self.open_if_closed()
        self.drop_if_exists(table_name=table_name, database=database, run_silent=run_silent)
        if self.verbose and not run_silent:
            print("  Creating the SQL Table: '" + table_name + "' in the database: " + database)
        self.cursor.execute("USE " + database + ";")
        if dynamic_type is None:
            table_str = create_tables[table_name]
        else:
            table_str = "CREATE TABLE `" + table_name + "` " + dynamically_named_tables[dynamic_type]
        self.cursor.execute(table_str)

    def insert_into_table(self, table_name, data, database=None):
        if database is None:
            database = sql_database
        self.open_if_closed()
        insert_str = insert_into_table_str(table_name, data, database=database)
        self.cursor.execute(insert_str)
        self.connection.commit()

    def buffer_insert_init(self, table_name, columns, database, run_silent=False, buffer_num=0):
        if self.verbose and not run_silent:
            print("  Buffer inserting " + database + "." + table_name)
        self.buffers[buffer_num] = make_insert_columns_str(table_name, columns, database)

    def buffer_insert_value(self, values, buffer_num=0):
        self.buffers[buffer_num] += make_insert_values_str(values) + ", "

    def buffer_insert_execute(self, run_silent=False, buffer_num=0):
        self.open_if_closed()
        self.cursor.execute(self.buffers[buffer_num][:-2] + ";")
        self.connection.commit()
        if self.verbose and not run_silent:
            print("    Table inserted")

    def insert_spectrum_table(self, table_name, columns, data, database=None):
        self.creat_table(table_name=table_name,  database=database, dynamic_type='spectrum',
                         run_silent=True)
        insert_str = make_insert_many_columns_str(table_name=table_name, columns=columns, database=database)
        self.cursor.executemany(insert_str, data)
        self.connection.commit()

    def creat_database(self, database):
        if self.verbose:
            print("  Creating the SQL Database: '" + database + "'.")
        self.open_if_closed()
        self.cursor.execute("CREATE DATABASE `" + database + "`;")

    def drop_database(self, database):
        if self.verbose:
            print("    Dropping (deleting if the database exists) the Database:", database)
        self.open_if_closed()
        self.cursor.execute("DROP DATABASE IF EXISTS `" + database + "`;")

    def clear_database(self, database):
        self.drop_database(database=database)
        self.creat_database(database=database)

    def query(self, sql_query_str):
        self.cursor.execute(sql_query_str)
        return [item for item in self.cursor]

    def prep_table_ops(self, table, database=sql_database):
        self.cursor.execute(F"""USE {database};""")
        self.cursor.execute(F"""DROP TABLE IF EXISTS `{table}`;""")

    def user_table(self, table_str, user_table_name=None, skip_if_exists=True):
        if user_table_name is None:
            user_table_name = F"user_table_{'%04i' % self.next_user_table_number}"
            self.next_user_table_number += 1
        if skip_if_exists:
            self.cursor.execute(F"""USE temp;""")
        else:
            self.prep_table_ops(table=user_table_name, database='temp')
        create_str = F"""CREATE TABLE IF NOT EXISTS `{user_table_name}` {table_str};"""
        self.cursor.execute(create_str)
        self.connection.commit()
        return user_table_name

    def get_tables(self, database):
        return self.query(F'''SELECT table_name FROM information_schema.tables
                                WHERE table_schema = "{database}"''')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    with OutputSQL() as output_sql:
        # output_sql.update_schemas()
        output_sql.make_new_server_user('hussain')
