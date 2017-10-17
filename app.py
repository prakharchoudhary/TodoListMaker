import datetime, json
from flask import (Flask, g, render_template, flash, redirect, url_for, request)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)

import models
import forms

app = Flask(__name__)
app.secret_key = "jasddbhA4576GJLKDSHHOAUI.3KSDFH_75"

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
	g.db = models.db
	g.db.connect()
	g.user = current_user

@app.after_request
def after_request(response):
	g.db.close()
	return response

@app.route('/signup', methods=('GET', 'POST'))
def signup():
	form = forms.SignUpForm()
	if form.validate_on_submit():
		flash("You've successfully registered!", "success")
		models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
		return redirect(url_for('index'))
	return render_template('signup.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.email == form.email.data)
		except models.DoesNotExist:
			flash("Your email or password doesn't match!", "error")
		else:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				flash("You've been logged in!", "success")
				return redirect(url_for('index'))
			else:
				flash("Your email or password doesn't match!", "error")
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out! Come back soon!", "success")
	return redirect(url_for('index'))

@app.route('/<int:user_id>/home')
@login_required
def main(user_id):
	todo = models.Todo.select().where(models.Todo.userid == user_id)
	return render_template('home.html', todo=todo)

@app.route('/<int:user_id>/new_task', methods=('GET', 'POST'))
@login_required
def newTask(user_id):
	form = forms.TaskForm()
	if form.validate_on_submit():
		try:
			flash("You've added a new task!")
			models.Todo.create_task(
				title = form.title.data,
				content = form.content.data,
				priority = form.priority.data,
				date = form.date.data,
				userid = user_id,
				is_done = False
				)
			todo = models.Todo.get()
			return redirect(url_for('main', user_id=user_id))
		except AttributeError:
			raise ValueError('There is some wrong field here!')
	return render_template('new_task.html', form=form)

@app.route('/<int:user_id>/<int:task_id>/edit_task', methods=('GET', 'POST'))
@login_required
def editTask(user_id, task_id):
	task = models.Todo.get(id=task_id)
	form = forms.TaskForm(obj=task)
	if form.validate_on_submit():
		try:
			if form.title.data:
				updateTitle = models.Todo.update(title=form.title.data).where(models.Todo.id == task_id)
				updateTitle.execute()		
			if form.date.data:
				updateDate = models.Todo.update(date=form.date.data).where(models.Todo.id == task_id)
				updateDate.execute()
			if form.content.data:
				updateContent = models.Todo.update(content=form.content.data).where(models.Todo.id == task_id)
				updateContent.execute()
			if form.title.data is not models.Todo.select('priority').where(models.Todo.id == task_id):
				updatePriority = models.Todo.update(priority=form.priority.data).where(models.Todo.id == task_id)
				updatePriority.execute()
			todo = models.Todo.get()
			return redirect(url_for('main', user_id=user_id))
		except AttributeError:
			raise ValueError('There is some wrong field here!')
	return render_template('edit_task.html', form=form)

@app.route('/check', methods=('GET', 'POST'))
@login_required
def check_task():
	data = int(request.form['task_id'])
	print(type(data))
	itemTocheck = models.Todo.get(models.Todo.id == data)
	item_status = itemTocheck.is_done
	print(type(item_status))
	itemUpdate = models.Todo.update(is_done = (item_status==False)).where(models.Todo.id == data)
	print(models.Todo.get(models.Todo.id == data).is_done)
	itemUpdate.execute()
	return json.dumps({'status': 'OK'})

@app.route('/<int:user_id>/<int:task_id>/delete')
@login_required
def del_task(user_id, task_id):
	itemToDel = models.Todo.delete().where(models.Todo.id == task_id)
	itemToDel.execute()
	return redirect(url_for('main', user_id=user_id))

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT, host=HOST)
