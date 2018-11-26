import datetime

from main import *


@app.route('/')
def index():
	if 'table' in session.keys():
		tb = session["table"]
		end = datetime.datetime.now()
		start = datetime.datetime.strptime("2018-9-3", '%Y-%m-%d')
		diff = end - start

		week = end.weekday() + 1
		num = end.hour
		if num < 12:
			num = int((num - 8) / 2) + 1
		elif 12 < num < 18:
			num = int((num - 14) / 2) + 3
		else:
			num = int((num - 19) / 2) + 5

		return render_template("class.html", table=Table(tb), week_num=int(diff.days / 7) + 1, now_week=week,
							   now_num=num)
	else:
		return redirect(url_for('login'))

@app.route("/reimport")
def reimport():
	# username = session['username']
	# password = session['password']
	# m = models.ClassJson.query.filter_by(username=username,password=password).first()
	# db.session.delete(m)
	# db.session.commit()
	img, jid = c_login()
	session['j_id'] = jid
	img_base64 = base64.b64encode(img).decode('utf-8')
	return render_template("reimport.html", img_base64=img_base64)

@app.route("/do_reimport",methods=['POST'])
def do_reimport():
	username = session['username']
	password = session['password']
	jid = session['j_id']
	code = request.form.get("code")
	tb = c_get_table(jid, username, password, code)
	if tb is None:
		return alertandredirect("验证码错误!!")
	else:
		session['table'] = str(tb)
		models.ClassJson.query.filter_by(username=username,password=password).update({'json':str(tb)})
		db.session.commit()
		return redirect(url_for("index"))


@app.route("/getcode/")
def getcode():
	username = request.args.get("username")
	item = models.ClassJson.query.filter_by(username=username).first()
	if item is None:
		img,jid = c_login()
		session['j_id'] = jid
		img_base64 = base64.b64encode(img).decode('utf-8')
		return render_template("code.html", img_base64=img_base64)
	else:
		return ""

@app.route('/login')
def login():
	if 'table' in session.keys():
		return redirect(url_for('index'))

	# img_base64 = base64.b64encode(img).decode('utf-8')
	# return render_template("login.html", img_base64=img_base64)
	return render_template("login.html")


@app.route("/import")
def import_class():
	if not ("username" in session.keys() and "password" in session.keys()):
		alertandredirect("请先登录",url_for("login"))
	img, jid = c_login()
	session['j_id'] = jid
	img_base64 = base64.b64encode(img).decode('utf-8')
	return render_template("code.html", img_base64=img_base64)

def alertandredirect(msg,url=None):
	html = "<script>"
	html = html + "alert('%s');" % msg
	if url is None:
		html = html + 'history.go(-1)'
	else:
		html = html + "window.location.href='%s';" % url
	html = html + "</script>"
	return html

def do_import_class(code):
	username = session['username']
	password = session['password']
	jid = session['j_id']
	tb = c_get_table(jid, username, password, code)
	if tb is None:
		return alertandredirect("教务处告诉真真，用户名、密码或者验证码错误")
	else:
		session['table'] = str(tb)
		new_item = models.ClassJson(username, password, str(tb))
		db.session.add(new_item)
		db.session.commit()
		return redirect(url_for("index"))

@app.route("/logout")
def logout():
	session.pop("username")
	session.pop("password")
	session.pop("table")
	return redirect(url_for("index"))

@app.route("/do_login", methods=['POST'])
def do_login():
	username = request.form.get("username")
	password = request.form.get("password")
	session['username'] = username
	session['password'] = password
	item = models.ClassJson.query.filter_by(username=username).first()
	if item is None:
		code = request.form.get("code")
		return do_import_class(code)
	elif item.password == password:
		session['table'] = item.json
		return redirect(url_for("index"))
	else:
		return alertandredirect("用户名或密码错误")
