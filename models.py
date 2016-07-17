import datetime
from peewee import *

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

db = SqliteDatabase('list.db')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)

	class Meta:
		database = db

	@classmethod	
	def create_user(cls, username, email, password):
		try:
			with db.transaction():
				cls.create(
					username=username,
					email=email,
					password=generate_password_hash(password)
				)
		except IntegrityError:
			raise ValueError("User already exists")

class Todo(Model):
	title = CharField(unique=True)
	content = CharField()
	priority = CharField()
	creation_dateTime = DateTimeField(default=datetime.datetime.now)
	userid = ForeignKeyField(User, related_name="user")

	class Meta:
		database = db

	@classmethod
	def create_task(cls, title, content, priority, creation_dateTime, userid):
		try:
			with db.transaction():
				cls.create(
					title=title,
					content=content,
					priority=priority,
					creation_dateTime=creation_dateTime,
					userid = userid
				)
		except IntegrityError:
			raise ValueError('Post with the same title already exits')

def initialize():
	db.connect()
	db.create_tables([User], safe=True)
	db.close()


