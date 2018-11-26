import base64, os, datetime, time, random

from catch import *
from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

import models


@app.route('/')
def index():
	if 'table' in session.keys():
		return redirect(url_for('show_class'))
	else:
		return redirect(url_for('login'))


@app.route('/login')
def login():
	img, jid = c_login()
	session['j_id'] = jid

	img_base64 = base64.b64encode(img).decode('utf-8')

	return render_template("login.html", img_base64=img_base64)


@app.route("/class")
def show_class():
	tb = session.get("table")
	return render_template("class.html", table=Table(tb))


@app.route("/do_login", methods=['POST'])
def do_login():
	jid = session['j_id']
	username = request.form.get("username")
	password = request.form.get("password")
	code = request.form.get("code")
	tb = c_get_table(jid, username, password, code)
	if tb is None:
		return "用户名或密码错误"
	else:
		session['table'] = str(tb)
		return redirect(url_for("show_class"))


if __name__ == '__main__':
	app.run(debug='true')
