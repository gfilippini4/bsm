import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from functionsForSql import (authLogin, newUser, getData, updateInfo, posting, postingFriend, 
setCookie, checkSession, queryInput, getNotifications, insertIntoFriendRequest,
requested, accept, decline)
import random as r
from google.cloud import storage
import json
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
	session = request.cookies.get('session')
	cname = request.cookies.get('email_address')
	if session == '' or session == None:
		return redirect(url_for('logIn'))
	data = getData(email_address)
	
	sc = storage.Client()
	bucket = sc.get_bucket('basic-flask-bucket')
	blob_profile_pic = bucket.get_blob('profiles/' + data['id'] + '/' + data['id'] + '_profile_pic.png')
	blob_banner_pic = bucket.get_blob('profiles/' + data['id'] + '/banner_pic/' + data['id'] + '_banner_pic.png')
	if blob_profile_pic != None:
		data['pro_pic'] = data['id']
	else:
		data['pro_pic'] = 'default'

	if blob_banner_pic != None:
		data['banner_pic'] = data['id']
	else:
		data['banner_pic'] = 'default'
	
	
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
	data['notifications'] = getNotifications(session)
	data['friend_zone'] = False
	sess_user = getData(cname)
	friends = sess_user['friends']
	for friend in friends:
		if friend['email_address'] == email_address:
			data['friend_zone'] = True
	data['requested'] = False
	if requested(sess_user['id'], data['id']):
		data['requested'] = True
	data['they_requested'] = requested(data['id'], sess_user['id'])
	print(data['they_requested'])
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

@app.route("/quickQuery", methods=['POST'])
def query():
	resp = queryInput(request.form['input'])
	dump = json.dumps({'status' : 'OK', 'data' : resp})
	return dump

@app.route("/addFriend", methods=['POST'])
def addFriend():
	# print(request.form)
	insertIntoFriendRequest(request.cookies.get('email_address'),request.form['id'])
	return redirect(url_for('profile', email_address=request.form['email_address']))

@app.route("/acceptFriend", methods=['POST'])
def acceptFriend():
	accept(request.cookies.get('email_address'), request.form['id'])
	return redirect(url_for('profile', email_address=request.form['email_address']))

@app.route("/declineFriend", methods=['POST'])
def declineFriend():
	decline(request.cookies.get('email_address'), request.form['id'])
	return redirect(url_for('profile', email_address=request.form['email_address']))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='443')