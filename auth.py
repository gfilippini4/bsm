import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, Blueprint, flash
from .functionsForSql import authLogin, newUser, getData, updateInfo, posting
from . import db
from flask_login import login_user

auth = Blueprint('auth', __name__)

@auth.route("/log-in", methods=['GET', 'POST'])
def logIn():
	login_user(user, remember=remember)
	# return redirect(url_for('main.profile')
	error = None
	if request.method == 'POST':
		form = request.form
		var = authLogin(form)
		if var:
			return redirect(url_for('main.profile', name=form['name']))
	flash('Username or password does not match, please try again.')
	return redirect(url_for('auth.login'))
	
@auth.route("/sign-up", methods=['GET', 'POST'])
def signUp():
	if request.method == 'POST':
		form = request.form
		if newUser(form):
			message = 'Congratulations on creating a new account! You may now log in here!'
			print(message)
			return redirect(url_for('auth.logIn'))
	flash('Something went wrong when you tried to sign up. Try again!')
	return redirect(url_for('signup.html'))


@auth.route("/logout")
def logout():
	return 'Logout'