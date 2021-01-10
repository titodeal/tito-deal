import sys
import os

# print(__file__)
app_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(app_path)

from config import (DB_IPADDRESS,
                    DB_PORT,
                    DB_NAME,
                    DB_USER)


start_db = os.path.abspath(os.path.join(app_path, "install/sh/start_db.sh"))
command = f"{start_db} {DB_IPADDRESS} {DB_PORT} {DB_NAME} {DB_USER}"

os.system(command)
