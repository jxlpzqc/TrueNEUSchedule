import base64, os, datetime, time, random

from catch import *
from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
app.config.from_object('settings')
db = SQLAlchemy(app)

import models

@app.route('/class')
def showclass():
	return render_template("class.html")


@app.route('/')
def login():
	if not ('con_id' in session.keys()):
		id = str(time.time()) + str(random.uniform(0, 100))
		# 防止重复
		while id in connection.keys():
			id = str(time.time()) + str(random.uniform(0, 100))
		session['con_id'] = id
	else:
		id = session['con_id']

	img = c_login(id)

	img_base64 = base64.b64encode(img).decode('utf-8')
	# with open('m.jpg', 'wb') as f:
	#     f.write(img)

	# print(connection)

	return render_template("login.html", img_base64=img_base64)


@app.route("/do_login", methods=['POST'])
def do_login():
	con_id = session['con_id']
	username = request.form.get("username")
	password = request.form.get("password")
	code = request.form.get("code")
	tb = c_get_table(con_id, username, password, code)
	if tb is None:
		return "用户名或密码错误"
	else:
		return render_template("class.html",table = tb)

	#return render_template("class.html",table=tb)


if __name__ == '__main__':
	app.run(debug='true')
