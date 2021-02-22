from .model import MainModel, psycopg2


class ProjectsModel(MainModel):
    """Projects SQL methods"""

    @MainModel.transaction_wrapper
    def create_project(self, project_name, owner_id, root,
                       scheme='SES',
                       fps=24,
                       status='new'):

        with self.conn.cursor() as curs:
            try:
                curs.execute("WITH rows AS ("
                             "  INSERT INTO projects "
                             "      (name, owner_id, scheme, fps, status) "
                             "  VALUES "
                             f"     ('{project_name}', \
                                     '{owner_id}', \
                                     '{scheme}', \
                                     '{fps}', \
                                     '{status}') "
                             "  RETURNING *) "
                             "INSERT INTO roots "
                             "   (path, project_id, user_id) "
                             "VALUES "
                             f"  ('{root}', \
                                  (SELECT project_id FROM rows), \
                                  '{owner_id}') "
                             "RETURNING (SELECT project_id FROM rows)")

                output = curs.fetchall()
                self.conn.commit()

            except psycopg2.errors.UniqueViolation as e:
                return self.prepare_response(1, str(e), "err")
        return self.prepare_response(0, output, "answer")

    @MainModel.transaction_wrapper
    def get_user_projects(self, user_id):

        with self.conn.cursor() as curs:
            curs.execute("SELECT projects.*, roots.path FROM projects "
                         "RIGHT JOIN roots USING (project_id)"
                         f"WHERE owner_id = {user_id}")

            output = curs.fetchall()
            self.conn.commit()

        if not output:
            answer = "The user has not any projects"
            return self.prepare_response(1, answer, "answer")

        columns = ["project_id", "name", "owner_id", "scheme", "fps", "status", "path"]
        return self.prepare_response(0, output, "tb_data", columns)
