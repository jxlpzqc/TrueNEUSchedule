from requests import *
from bs4 import *
from table import Table

# 此处注意考虑线程安全问题
connection = {}


def c_login(con_id):
	"""
	记录用户，并获取验证码图片
	:return: 验证码图片
	"""
	# get cookie and validate code
	login_view_url = 'https://zhjw.neu.edu.cn/'

	if con_id in connection.keys():
		s = connection[con_id]
	else:
		s = session()
		connection[con_id] = s

	login_view_resp = s.get(login_view_url)

	soup = BeautifulSoup(login_view_resp.text, 'html.parser')
	img_url = login_view_url + soup.find_all('img')[2]['src']
	img_resp = s.get(img_url)
	return img_resp.content


def c_get_table(con_id, username, password, code):
	"""

	:param con_id: 连接id
	:param username: 用户名
	:param password: 密码
	:param code: 验证码
	:return: 0代表登录失败，否则是一个Table对象
	"""

	login_url = 'https://zhjw.neu.edu.cn/ACTIONLOGON.APPPROCESS?mode='
	login_data = {'WebUserNO': username, 'Password': password, 'Agnomen': code, 'submit7': '%B5%C7%C2%BC'}
	table_url = 'https://zhjw.neu.edu.cn/ACTIONQUERYSTUDENTSCHEDULEBYSELF.APPPROCESS'

	s = connection[con_id]
	login_resp = s.post(login_url, login_data)
	if "网络综合平台" in login_resp.text:
		table_html = s.get(table_url).text
		# print(table_html)
		soup = BeautifulSoup(table_html, "html.parser")
		md = soup.find("table", {'border': '0', 'align': 'center'}).find_all('tr')[2:]

		table = Table()

		for number in range(1, 7):
			for week in range(1, 8):
				course_texts_src = md[number].find_all("td")[week].get_text('\n')
				course_texts = course_texts_src.split("\n")
				course_count = len(course_texts) / 4

				for i in range(0, int(course_count)):
					course_text = course_texts[i * 4:i * 4 + 4]
					name = course_text[0]
					teacher = course_text[1]
					classroom = course_text[2]
					lastline = course_text[3].split('  ')
					week_count = lastline[0]
					lasttime = lastline[1]
					table.add_course(week, number, name, teacher, classroom, week_count, lasttime)
		# print(table)
		return table
	# print(md)
	else:
		return None
