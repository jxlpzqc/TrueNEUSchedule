from main import *


@app.route('/')
def index():
	if 'table' in session.keys():
		return redirect(url_for('show_class'))
	else:
		return redirect(url_for('login'))


@app.route('/login')
def login():
	if 'table' in session.keys():
		return redirect(url_for('show_class'))


	#img_base64 = base64.b64encode(img).decode('utf-8')
	# return render_template("login.html", img_base64=img_base64)
	return render_template("login.html")


@app.route("/class")
def show_class():
	tb = session["table"]
	return render_template("class.html", table=Table(tb))

@app.route("/import")
def import_class():
	if not("username" in session.keys() and "password" in session.keys()):
		return "请先登录"
	img, jid = c_login()
	session['j_id'] = jid
	img_base64 = base64.b64encode(img).decode('utf-8')
	return render_template("code.html",img_base64 = img_base64)

@app.route("/do_import",methods=['POST'])
def do_import_class():
	username = session['username']
	password = session['password']
	jid = session['j_id']
	code = request.form.get("code")
	tb = c_get_table(jid, username, password, code)
	if tb is None:
		return "教务处告诉真真，用户名、密码或者验证码错误"
	else:
		session['table'] = str(tb)
		new_item = models.ClassJson(username,password,str(tb))
		db.session.add(new_item)
		db.session.commit()
		return redirect(url_for("show_class"))


@app.route("/do_login", methods=['POST'])
def do_login():
	username = request.form.get("username")
	password = request.form.get("password")
	session['username'] = username
	session['password'] = password
	item = models.ClassJson.query.filter_by(username=username).first()
	if item is None:
		return redirect(url_for("import_class"))
	elif item.password == password:
		session['table'] = item.json
		return redirect(url_for("show_class"))
	else:
		return "用户名或密码错误"


