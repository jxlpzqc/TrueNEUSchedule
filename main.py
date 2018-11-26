import base64, os, datetime, time, random

from catch import *
from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

import models
from controllers import *

if __name__ == '__main__':
	app.run(debug='true')
