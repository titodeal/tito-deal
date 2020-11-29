#!/usr/bin/env python3

# from app import app
from app.routes import app

app.run(debug=True, port=5000)
