from . import app
from flask import send_file, redirect, url_for, request
from . import models


@app.route("/")
def main_page():
    return redirect(url_for('loggin'))
#     return send_file('app/web/index.html')


@app.route("/loggin", methods=["POST", "GET"])
def loggin():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']

        if models.get_user(username):
            return ("Login '%s' is unvailable" % username)
        if models.get_email(email): 
            return ("Email '%s' is unvailable" % email)

        password = request.form['password']
        models.add_user(username, password, email)

        return ("Hello %s" % username)
    else:
        return send_file('templates/login.html')
#
# @app.route("/join.html")
# def send_join():
#     return send_file('app/web/join.html')
#
#
# @app.route("/join", methods=['POST', 'GET'])
# def join():
#     if request.method == 'POST':
#         user = request.form['username']
#         return "The request is POST, value is %s" % user
#     else:
#         user = request.args.get('username')
#         return "The request is GET, value is %s" % user
#
# app.run(debug=True, port=5000)
