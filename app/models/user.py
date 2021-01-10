from .model import MainModel, psycopg2


class UserModel(MainModel):
    """User SQL methods"""

    @MainModel.transaction_wrapper
    def _add_user(self, user_name, password, email):
        with self.conn.cursor() as curs:
            try:
                curs.execute("INSERT INTO users "
                             "(login, passwd, email) "
                             "VALUES "
                             f"('{user_name}', '{password}', '{email}') "
                             "RETURNING *")

                output = curs.fetchall()
                self.conn.commit()

            except psycopg2.errors.UniqueViolation as e:
                return self.prepare_response(1, str(e), "err")
#                 return [1, str(e)]
        return self.prepare_response(0, output, "answer")
#         return [0, output]

    @MainModel.transaction_wrapper
    def _del_user(self, name):
        with self.conn.cursor() as curs:

            curs.execute(f"DELETE FROM users "
                        "WHERE login = '{}' "
                        "RETURNING *".format(name))

            output = curs.fetchall()
            self.conn.commit()

        if not output:
            answer =  f"User '{name}' not found"
            return self.prepare_response(1, answer, "answer")
#             return [1, f"User '{name}' not found"]
        return self.prepare_response(0, output, "answer")
#         return [0, output]

    @MainModel.transaction_wrapper
    def get_users(self, login):

        sql = "SELECT * FROM users " \
              f"WHERE login LIKE '{login}'"

        with self.conn.cursor() as curs:
            curs.execute(sql)
            output = curs.fetchall()
            columns = self.get_table_columns("users", curs)


        if not output:
            answer =  f"User '{login}' not found"
            return self.prepare_response(1, answer, "answer")

        return self.prepare_response(0, output, "tb_data", columns)

    @MainModel.transaction_wrapper
    def get_user_phash(self, login):
        with self.conn.cursor() as curs:
            curs.execute("SELECT passwd FROM users "
                         f"WHERE login = '{login}'")
            output = curs.fetchone()

        if not output:
            data = f"User '{login}' not found"
            return self.prepare_response(1, data, "error")
        return self.prepare_response(0, output[0], "answer")

    @MainModel.transaction_wrapper
    def get_colleagues(self, login):
        pass

    @MainModel.transaction_wrapper
    def send_invintation(self, fromuser, touser):
        pass


#     @staticmethod
#     def add_contractor(user_id, contractor_id):
#         cur = conn.cursor()
#         cur.execute(f"INSERT INTO contractors "
#                     f"(user_id, user_contractor_id) "
#                     f"VALUES "
#                     f"({user_id}, {contractor_id}) "
#                     "RETURNING *")
# 
#         print(cur.fetchall())
#         conn.commit()
#         cur.close()
# 
#     @staticmethod
#     def set_contractor_confirm(user_id, contractor_id, confirm=False):
#         cur = conn.cursor()
#         cur.execute("UPDATE  contractors "
#                     f"SET confirmed = {str(confirm)} "
#                     f"WHERE user_id = '{user_id}'  AND user_contractor_id = '{contractor_id}' "
#                     "RETURNING *")
# 
#         print(cur.fetchall())
#         conn.commit()
#         cur.close()
# 
#     @staticmethod
#     def get_user(name):
#         cur = conn.cursor()
#         cur.execute(f"SELECT * "
#                     "FROM users "
#                     "WHERE name LIKE '{}'".format(name))
#         return cur.fetchall()
#         cur.close()
# 
# 
#     @staticmethod
#     def get_email(email):
#         cur = conn.cursor()
#         cur.execute(f"SELECT * "
#                     "FROM users "
#                     "WHERE email LIKE '{}'".format(email))
#         return cur.fetchall()
#         cur.close()

