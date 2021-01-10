#!/usr/bin/env python3

import sys, os
path = os.path.abspath(".")
sys.path.append(path)

from config import DB_IPADDRESS, DB_PORT, DB_NAME, DB_USER
import psycopg2

class MainModel:
    """Main object to start SQL requests"""
    def __init__(self, hostaddr=DB_IPADDRESS, port=DB_PORT,
                 dbname=DB_NAME, user=DB_USER):

        self.hostaddr = hostaddr
        self.port = port
        self.dbname = dbname
        self.user = user
        self.__check_server_access()
        self.conn = None

    @staticmethod
    def __check_server_access():
        exitstatus = os.system(f"pg_isready -q -h {DB_IPADDRESS} -p {DB_PORT}")
        if not exitstatus == 0:
            print("!=> Unable to connect to postgresql server.")

    @staticmethod
    def transaction_wrapper(func):
        """Wrapping db session"""
        def wrapper(self, *args, **kwargs):
            self.__start_db_connection()
            result = func(self, *args, **kwargs)
            self.__close_db_connection()
            return result
        return wrapper

    def __start_db_connection(self):
        self.conn = psycopg2.connect(hostaddr=self.hostaddr,
                                     port=self.port,
                                     dbname=self.dbname,
                                     user=self.user)

    def __close_db_connection(self):
        self.conn.close()

    def get_table_columns(self, table, curs=None):
        sql = "SELECT column_name FROM information_schema.columns " \
              "WHERE table_schema = 'public' " \
              f"AND table_name = '{table}'"

        if curs is not None:
            curs.execute(sql)
            return [item[0] for item in curs.fetchall()]

        with self.conn.cursor() as curs:
            curs.execute(sql)
            return [item[0] for item in curs.fetchall()]

    def prepare_response(self, returncode, data, type_, columns=None):
        """To shape response as dict data
        Available types: answer, tb_data"""

        response = {}
        response['returncode'] = returncode
        response['data'] = data
        response['type'] = type_
        response['columns'] = columns

        return response
