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
    def get_user_offers(self, user_id):
        with self.conn.cursor() as curs:
            curs.execute("SELECT "
                         "       id_offer, users.user_id, users.login, "
                         "       conditions, 'contractor' as type, offers.accepted "
                         "FROM offers "
                         "JOIN users ON users.user_id = offers.contractor_id  "
                         f"WHERE offers.user_id = {user_id} "
                         "UNION "
                         "SELECT "
                         "       id_offer, users.user_id, users.login, "
                         "       conditions, 'employer' as type, offers.accepted "
                         "FROM offers "
                         "JOIN users USING (user_id) "
                         f"WHERE offers.contractor_id = {user_id}")

            output = curs.fetchall()

        if not output:
            answer = f"Offer records not found"
            return self.prepare_response(1, answer, "answer")

        columns = ["offer_id", "user_id", "login", "conditions", "type", "accepted"]
        return self.prepare_response(0, output, "tb_data", columns)

    @MainModel.transaction_wrapper
    def get_user_contractors(self, user_id):
        with self.conn.cursor() as curs:
            curs.execute("SELECT users.* "
                         "FROM offers "
                         "JOIN users ON users.user_id = offers.contractor_id "
                         f"WHERE offers.user_id = {user_id}")

            output = curs.fetchall()
            columns = self.get_table_columns("users", curs)


        if not output:
            answer =  f"Contractors not found"
            return self.prepare_response(1, answer, "answer")
        return self.prepare_response(0, output, "tb_data", columns)

    @MainModel.transaction_wrapper
    def get_user_agreements(self, user_id):
        with self.conn.cursor() as curs:
            curs.execute("SELECT "
                         "  agreement_id, "
                         "  owner_id, "
                         "  owners.login as owner_login, "
                         "  contractor_id, "
                         "  contractors.login as contracotor_login, "
                         "  conditions, "
                         "  expiration, "
                         "  accepted "
                         "FROM agreements "
                         "JOIN users as owners ON owners.user_id = owner_id "
                         "JOIN users as contractors ON contractors.user_id = contractor_id "
                         f"WHERE owner_id = {user_id} OR contractor_id = {user_id}")

            output = curs.fetchall()

        if not output:
            answer = f"Agreements records for user id '{user_id}' not found"
            return self.prepare_response(1, answer, "answer")

        columns = ["agreement_id", "owner_id", "owner_login",
                   "contractor_id", "contractor_login",
                   "conditions", "expiration", "accepted"]
        return self.prepare_response(0, output, "tb_data", columns)

    @MainModel.transaction_wrapper
    def send_offer(self, owner_id, contractor_id):
        with self.conn.cursor() as curs:
            try:
                curs.execute("INSERT INTO agreements " "(owner_id, contractor_id) "
                             "VALUES "
                             f"('{owner_id}', '{contractor_id}') "
                             "RETURNING *")

                output = curs.fetchall()
                self.conn.commit()

            except psycopg2.errors.UniqueViolation as e:
                return self.prepare_response(1, str(e), "err")
        return self.prepare_response(0, output, "answer")

    @MainModel.transaction_wrapper
    def accept_agreement(self, agreement_id):
        with self.conn.cursor() as curs:
            try:
                curs.execute("UPDATE agreements "
                             "SET accepted = true "
                             "WHERE "
                             f"  agreement_id = {agreement_id} "
                             "RETURNING *")

                output = curs.fetchall()
                self.conn.commit()

            except psycopg2.errors.UniqueViolation as e:
                return self.prepare_response(1, str(e), "err")
        return self.prepare_response(0, output, "answer")

    @MainModel.transaction_wrapper
    def send_contract(self, project_id, agreement_id):
        with self.conn.cursor() as curs:
            try:
                curs.execute("INSERT INTO contracts "
                             "(project_id, agreement_id) "
                             "VALUES "
                             f"('{project_id}', '{agreement_id}') "
                             "RETURNING *")

                output = curs.fetchall()
                self.conn.commit()

            except psycopg2.errors.UniqueViolation as e:
                return self.prepare_response(1, str(e), "err")

        columns = ["contract_id", "agreement_id", "project_id",
                   "documents", "departments", "specialty", "role", "accepted", "date"]
        return self.prepare_response(0, output, "tb_data", columns)

    @MainModel.transaction_wrapper
    def get_user_contracts(self, user_id):
        with self.conn.cursor() as curs:
            curs.execute("SELECT contracts.contract_id, "
                         "       contracts.agreement_id, "
                         "       users.user_id as contractor_id, "
                         "       users.login as contractor, "
                         "       projects.project_id, "
                         "       projects.name as project, "
                         "       contracts.accepted, "
                         "       contracts.documents, "
                         "       contracts.departments, "
                         "       contracts.specialty, "
                         "       contracts.role, "
                         "       contracts.date "
                         "FROM agreements "
                         "JOIN contracts USING (agreement_id) "
                         "JOIN users on users.user_id = agreements.contractor_id "
                         "JOIN projects on projects.project_id = contracts.project_id "
                         f"WHERE agreements.owner_id = {user_id}")

            output = curs.fetchall()

        if not output:
            answer = f"Contracts records for user id '{user_id}' not found"
            return self.prepare_response(1, answer, "answer")

        columns = ["contract_id",
                   "agreement_id",
                   "contractor_id",
                   "contractor",
                   "project_id",
                   "project",
                   "accepted",
                   "documents",
                   "departments",
                   "specialty",
                   "role",
                   "date"]
        return self.prepare_response(0, output, "tb_data", columns)

    @MainModel.transaction_wrapper
    def create_user_root(self, user_id, root_folder, sharing=False):
#         sharing = str(sharing).lower()
        with self.conn.cursor() as curs:
            try:
                curs.execute("INSERT INTO roots "
                             "(owner_id, root_folder, sharing) "
                             "VALUES "
                             f"('{user_id}', '{root_folder}', '{sharing}') "
                             "RETURNING *")

                output = curs.fetchall()
                self.conn.commit()

            except psycopg2.errors.UniqueViolation as e:
                return self.prepare_response(1, str(e), "err")

        return self.prepare_response(0, output, "answer")

    @MainModel.transaction_wrapper
    def get_user_roots(self, user_id):
        with self.conn.cursor() as curs:
            curs.execute("SELECT root_id, "
                         "       root_folder, "
                         "       sharing "
                         "FROM roots "
                         f"WHERE owner_id = {user_id}")

            output = curs.fetchall()

        if not output:
            answer = f"Roots records for user id '{user_id}' not found"
            return self.prepare_response(1, answer, "answer")

        columns = ["root_id",
                   "root_folder",
                   "sharing"]
        return self.prepare_response(0, output, "tb_data", columns)
