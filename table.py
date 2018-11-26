import json


class Table:
	__courses = []

	def __get_week(self, week):
		week = week[0:-1]
		src_days = week.split('.')
		days = []
		for d in src_days:
			if '-' in d:
				begin = int(d.split('-')[0])
				end = int(d.split('-')[1])
				for dm in range(begin, end):
					days.append(dm)
			else:
				days.append(int(d))
		return days

	def add_course(self, day, number, name, teacher, classroom, week, last_time):
		"""
		:param day: 星期1-7
		:param number: 节次1-6
		:param name: 课程名
		:param teacher: 老师
		:param classroom: 教室
		:param week: 周 原生字符串 比如 10.14-16周
		:param last_time: 持续时间
		:return: 没有返回值
		"""
		course = {'time': str(day) + str(number), 'name': name,
				  'teacher': teacher, 'classroom': classroom,
				  'week': self.__get_week(week), 'last_time': int(last_time[0:-1])}
		self.__courses.append(course)

	def get_course(self,week,day,number):
		for course in self.__courses:
			if week in course['week'] and course['time'] == str(day)+str(number):
				return course
		return ""

	def __init__(self, json_text=None):
		if json_text is None:
			pass
		else:
			self.__courses = json_text.loads(json_text)

	def __repr__(self):
		return json.dumps(self.__courses)
