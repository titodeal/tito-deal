#!/usr/bin/env python3

from config import SQL_IPADDRESS, SQL_PORT
import psycopg2

conn = psycopg2.connect(hostaddr=SQL_IPADDRESS, port=SQL_PORT,
                        dbname='titodeal', user='titodeal')


def add_user(org_name,
             password,
             email=None,
             phone=None,
             external_ip=None,
             folder_structure=None):

    cur = conn.cursor()
    cur.execute(f"INSERT INTO users "
                f"(org_name, passwd, "
                f"email, phone, external_ip, folder_structure) "
                f"VALUES "
                f"('{org_name}', '{password}', '{email}', "
                f"'{phone}', '{external_ip}', '{folder_structure}') "
                "RETURNING *")

    print(cur.fetchall())
    conn.commit()
    cur.close()


def get_user(name):
    cur = conn.cursor()
    cur.execute(f"SELECT * "
                "FROM users "
                "WHERE org_name LIKE '{}'".format(name))
    return cur.fetchall()
    cur.close()


def get_email(email):
    cur = conn.cursor()
    cur.execute(f"SELECT * "
                "FROM users "
                "WHERE email LIKE '{}'".format(email))
    return cur.fetchall()
    cur.close()

def del_user(name):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM users "
                "WHERE org_name = '{}' "
                "RETURNING *".format(name))
    print(cur.fetchall())
    conn.commit()
    cur.close()

if __name__ == '__main__':
    print(SQL_IPADDRESS)
    print(SQL_PORT)

    get_user("%")
    # add_user("Vasy", "123")
    add_user("Fedya", "123", "fedyaFedya@gmail.com", "380875547997", "192.168.1.125")
    add_user("Bodya", "123", "Bodya@gmail.com", "380875547997", "192.168.1.123", "c:/Projects")
    # del_user("Vasy")
    conn.close()
