from main import db
from table import Table


class ClassJson(db.Model):
	__tablename__ = 'classjson'
	username = db.Column(db.String(50), primary_key=True)
	password = db.Column(db.String(50))
	json = db.Column(db.Text)

	def __init__(self, username, password, json):
		self.username = username
		self.password = password
		self.json = json


