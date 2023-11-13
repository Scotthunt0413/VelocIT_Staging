import os


try:
    from mypysql.sql_config import sql_host, sql_port, sql_database, sql_user,  sql_password
except ImportError:
    try:
        from sql_config import sql_host, sql_port, sql_database, sql_user,  sql_password
    except ImportError:
        try:
            from ref.sql_config import sql_host, sql_port, sql_database, sql_user,  sql_password
        except ImportError:
            sql_database = input(f"MySQL Database - Enter the MySQL Database (Schema):\n")

            sql_user = input(f"MySQL Username - Enter your MySQL username:\n")

            sql_password = input(f"(Warning Is visible on Screen and saved in a regular text file!)\n" +
                                 f"MySQL Password - Enter your MySQL password :\n")

            sql_host = input(f"MySQL Host - Enter the MySQL host URL (default: local host):\n")
            if sql_host.strip() == "":
                sql_host = 'localhost'

            sql_port = input(f"MySQL Port - Enter the MySQL port to use (default: 3306):\n")
            if sql_port.strip() == "":
                sql_port = 3306

            save_this_data = input("Save this data to be automatically imported next time? [Y,n]:\n").strip().lower()
            if len(save_this_data) != 0 and save_this_data[0] == 'y':
                # save the data
                mypysql_module_dir = os.path.dirname(os.path.realpath(__file__))
                sql_config_path = os.path.join(mypysql_module_dir, 'sql_config.py')
                with open(sql_config_path, 'w') as f:
                    f.write(f'''sql_host = "{sql_host}"''')
                    f.write(f'''sql_port = "{sql_port}"''')
                    f.write(f'''sql_database = "{sql_database}"''')
                    f.write(f'''sql_user = "{sql_user}"''')
                    f.write(f"""sql_password = '''{sql_password}'''\n""")

