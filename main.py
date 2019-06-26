import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from functionsForSql import authLogin, newUser, getData, updateInfo, posting, postingFriend, setCookie, checkSession
import random as r

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('site.html')
	
@app.route("/log-in", methods=['GET', 'POST'])
def logIn():
	error = None
	if request.method == 'POST':
		form = request.form
		var = authLogin(form)
		if var:
			resp = redirect(url_for('profile', email_address=form['email_address']))
			session_cookie = str(os.urandom(16).hex())
			# Set a unique cookie in the browser and store in the profile database, 'session_cookie'
			resp.set_cookie('email_address', form['email_address'])
			resp.set_cookie('session', session_cookie)
			setCookie(session_cookie, form['email_address'])
			return resp
		error = 'Username or password does not match, please try again.'
	return render_template('login.html', error=error)
	
@app.route("/logout", methods=['POST','GET'])
def logout():
	resp = redirect(url_for('hello'))
	resp.set_cookie('session', '', max_age=0)
	resp.set_cookie('email_address', '', max_age=0)
	return resp
	
@app.route("/sign-up", methods=['GET', 'POST'])
def signUp():
	if request.method == 'POST':
		form = request.form
		if newUser(form):
			message = 'Congratulations on creating a new account! You may now log in here!'
			return render_template('site.html', data=message)
	return render_template('signup.html')

@app.route("/profile/<email_address>", methods=['POST', 'GET'])
def profile(email_address):
	print(email_address)
	cname = request.cookies.get('session')
	if cname == '' or cname == None:
		return redirect(url_for('logIn'))
	data = getData(email_address)
	data['pro_pic'] = 'profiles/' + data['id'] + '/' + data['id'] + '_profile_pic.png'
	dir_path = os.path.dirname(os.path.realpath(__file__))
	try:
		open(dir_path + '/static/profiles/' + data['id'] + '/' + data['id'] + '_profile_pic.png')
	except Exception as e:
		data['pro_pic'] = 'profiles/default/default_profile_pic.png'
	
	
	# ################################################## #
	# # This is where the session needs to be verified # #               
	# ################################################## #
	
	if request.method == 'POST':
		form = request.form
		auth = False
		if request.cookies.get('email_address') == email_address:
			auth = True
		if not auth:
			postingFriend(email_address, request.cookies.get('email_address'), form['content'])
		else:
			posting(form)
		return redirect(url_for('profile', email_address=email_address))
	data['authenticated'] = False
	if cname == email_address:
		data['authenticated'] = True
	return render_template('profile.html', data=data, random_num=r.randint(1,100000))
	
@app.route("/edit-profile/<cookie>", methods=['GET', 'POST'])
def editProfile(cookie):
	session = request.cookies.get('session')
	email_address= request.cookies.get('email_address')
	checkSession(session, email_address)
	if not checkSession(session, email_address):
		return redirect(url_for('profile', email_address=email_address))
	data = getData(email_address)
	if request.method == 'POST':
		new_name = data['email_address']
		form = request.form
		files = request.files
		updateInfo(form, files, data['id'])
		if form['email_address'] != '':
			new_name = form['email_address']
		return redirect(url_for('profile', email_address=new_name))
	return render_template('edit.html', data=data)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port='443')