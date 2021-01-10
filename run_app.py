#!/usr/bin/env python3

from config import (API_SERVER_PORT,
                    DB_IPADDRESS,
                    DB_PORT,
                    DB_NAME,
                    DB_USER)

from app.api_server.run import ApiServer

with ApiServer(port=API_SERVER_PORT, timeout=0.1) as api_server:
    api_server.start_server()

