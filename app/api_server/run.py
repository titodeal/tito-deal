import sys
import os
import traceback

external_path = os.path.abspath("..")

sys.path.append(external_path)

from tito_sockets import application_server


from app.models import user

class ApiServer(application_server.ApplicationServer, user.UserModel):
#     """docstring for ApiServer"""
    def __init__(self, port, timeout=0.2):
        super(ApiServer, self).__init__(port=port, timeout=timeout)
        user.UserModel.__init__(self)

        self.verified_connections = set()

    def handle_massage(self, msg, client):
        method_name = msg.get('method')
        args = msg.get('args')

        if method_name == "get_credentials":
            return self.get_credentials(client, *args)

        if method_name == "create_credentials":
            return self.create_credentials(client, *args)

        self.verify_connection(client)

        return getattr(self, method_name)(*args)

    def close_client(self, client):
        try:
            print(self.verified_connections)
            self.connections.pop(self.connections.index(client))
            self.verified_connections.discard((id(client), client.getpeername()))
            print(self.verified_connections)
        except ValueError:
            print('=> Client {} not found in connections list'.format(client.getpeername()))

        try:
            print("=> Closing socket: {}".format(client.getpeername()))
            client.close()
        except OSError:
            client.close()

    def create_credentials(self, client, login, passwd, email):
        from argon2 import PasswordHasher

        print(f"=> Creating new user: {login}")
        ph = PasswordHasher()
        phash = ph.hash(passwd)
        response = self._add_user(login, phash, email)
        if response['returncode'] != 0:
            return self.prepare_response(1, response['data'], "err")

        self.verified_connections.add((id(client), client.getpeername()))
        answer = "=>Registration user '{login}' was successfull."
        return self.prepare_response(0, answer, "answer")


    def get_credentials(self, client, login, passwd):
        import argon2
        from argon2 import PasswordHasher

#         returncode, data = self.get_user_phash(login)
#         if returncode != 0:
#             raise ValueError(data)

#         ph = PasswordHasher()
# #         print("DATA iS ", data[0])

#         if ph.verify(data[0], passwd):
#             self.verified_connections.add((id(client), client.getpeername()))
#             return [0, "=>Verification successfull."]
#         else:
#             raise ValueError("Verification faild")

        response = self.get_user_phash(login)

        if response['returncode'] != 0:
            return self.prepare_response(1, response['data'], "err")

        ph = PasswordHasher()
        try:
            ph.verify(response['data'], passwd)
            self.verified_connections.add((id(client), client.getpeername()))
            answer = "=>Verification successfull."
            return self.prepare_response(0, answer, "answer")

        except argon2.exceptions.VerifyMismatchError as e:
            print("!=> ", traceback.format_exc())
            return self.prepare_response(1, str(e), "err")

    def verify_connection(self, client):
        if not (id(client), client.getpeername()) in self.verified_connections:
            answer = "!=> User no have credentials"
            return self.prepare_response(1, answer, "err")

