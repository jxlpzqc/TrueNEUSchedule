import requests
from bs4 import *
from table import Table


# 此处注意考虑线程安全问题
# connection = {}


def c_login():
	"""
	记录用户，并获取验证码图片
	:return: 验证码图片
	"""
	# get cookie and validate code
	login_view_url = 'https://zhjw.neu.edu.cn/'

	login_view_resp = requests.get(login_view_url)

	jid = login_view_resp.cookies['JSESSIONID']

	soup = BeautifulSoup(login_view_resp.text, 'html.parser')
	img_url = login_view_url + soup.find_all('img')[2]['src']
	cookies = dict(JSESSIONID=jid)
	img_resp = requests.get(img_url, cookies=cookies)
	return img_resp.content, jid


def c_get_table(jid, username, password, code):
	"""

	:param jid: 连接id
	:param username: 用户名
	:param password: 密码
	:param code: 验证码
	:return: 0代表登录失败，否则是一个Table对象
	"""

	login_url = 'https://zhjw.neu.edu.cn/ACTIONLOGON.APPPROCESS?mode='
	login_data = {'WebUserNO': username, 'Password': password, 'Agnomen': code, 'submit7': '%B5%C7%C2%BC'}
	table_url = 'https://zhjw.neu.edu.cn/ACTIONQUERYSTUDENTSCHEDULEBYSELF.APPPROCESS'
	cookies = dict(JSESSIONID=jid)

	login_resp = requests.post(login_url, login_data, cookies=cookies)
	if "网络综合平台" in login_resp.text:
		table_html = requests.get(table_url, cookies=cookies).text
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
