import io
from main import app
from flask import Flask, render_template, request, url_for, redirect, send_file, send_from_directory, flash, session
import model
import os
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    contributions = model.Contribution.select().order_by(model.Contribution.id)
    return render_template('index.html', contributions=contributions)


@app.route('/assets/<path:path>')
def asset(path):
    return send_from_directory('static', path)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
	# If there are no users, create one with a blank password
	query = model.Users.select().where(model.Users.title=='admin')
	if not query:
		model.Users.create(title='admin', name='admin', pw=generate_password_hash(''))
		
	if not session.get('logged_in'):
		return render_template('admin/admin_login.html')
	else:
		return redirect(url_for('contribution_new'))

	
@app.route('/admin/admin_login',methods=['GET', 'POST'])
def admin_login():
	username = request.form['username']
	password = request.form['password']
	userExists = model.Users.get_or_none(model.Users.name==(username))
		
	if userExists and check_password_hash(model.Users.get(model.Users.name==username).pw, password):
		session['logged_in'] = (True,model.Users.get(model.Users.name==username).id)
		return redirect(url_for('contribution_new'))
	else:
		flash('Username or password incorrect. Please try again.')
	return admin()


@app.route('/logout')
def logout():
	session['logged_in'] = False
	return redirect(url_for('admin'))
	
@app.route('/admin/password', methods=['GET', 'POST'])
def change_password():
	if session.get('logged_in'):
	
		if request.method == 'POST':
			oldPass = request.form['oldPass']
			newPass = request.form['newPass']
			newPassCheck = request.form['newPassCheck']
			identical = newPass == newPassCheck
			userId = session['logged_in'][1]
			
			if identical and len(request.form['newPass']) >= 1:
				if check_password_hash(model.Users.get(model.Users.id==userId).pw, oldPass):
					query = model.Users.update(pw=generate_password_hash(newPass)).where(model.Users.id == userId)
					query.execute()
					return logout()
				else:
					flash('Old password incorrect')
					return redirect(url_for('change_password'))
			else:
				flash('New password must be entered twice')
				return redirect(url_for('change_password'))
				
		return render_template('admin/change_password.html',
								   contributions=model.Contribution.select().order_by(model.Contribution.id)
			)
		
	return redirect(url_for('admin'))
	

@app.route('/admin/contribution/new', methods=['GET', 'POST'])
def contribution_new():
	if session.get('logged_in'):
		if request.method == 'GET':
			return render_template('admin/contribution_form.html',
								   endpoint=url_for('contribution_new'),
								   map_countries=model.COUNTRIES,
								   contributions=model.Contribution.select().order_by(model.Contribution.id)
								   )

		contribution = model.Contribution(
			title=request.form.get('title'),
			description=request.form.get('description'),
			map_location=request.form.get('map_location'),
			shown_location=request.form.get('shown_location'),
			contributor=request.form.get('contributor'),
		)
		contribution.save()

		return redirect(url_for('contribution_edit', contr_id=contribution.id))
	else:
		return redirect(url_for('admin'))


@app.route('/admin/contribution/<contr_id>', methods=['GET', 'POST'])
def contribution_edit(contr_id):
	if session.get('logged_in'):
		try:
			contribution = model.Contribution.get_by_id(contr_id)

			if request.method == 'GET':
				return render_template('admin/contribution_form.html',
									   endpoint=url_for('contribution_edit', contr_id=contr_id),
									   map_countries=model.COUNTRIES,
									   contribution=contribution,
									   contributions=model.Contribution.select().order_by(model.Contribution.id)
									   )
			for attrib in request.form:
				setattr(contribution, attrib, request.form.get(attrib))
			contribution.save()

			return redirect(url_for('contribution_edit', contr_id=contribution.id))
		except:
			return redirect(url_for('contribution_new'))
	else:
		return redirect(url_for('admin'))


@app.route('/admin/contribution/<contr_id>/delete', methods=['POST'])
def contribution_delete(contr_id):
	if session.get('logged_in'):
		model.Contribution.delete_by_id(contr_id)

		return redirect(url_for('contribution_new'))
	else:
		return redirect(url_for('admin'))


@app.route('/image/<img_id>', methods=['GET'])
def image(img_id):
    image = model.Image.get_by_id(img_id)

    if not image:
        return 404
    return send_file(io.BytesIO(image.file), mimetype='image/png')


@app.route('/admin/contribution/<contr_id>/image/new', methods=['POST'])
def image_new(contr_id):
	if session.get('logged_in'):
		image = model.Image(
			title=request.form.get('title'),
			description=request.form.get('description'),
			mimetype=request.files['file'].mimetype,
			file=request.files['file'].read(),
			contribution=contr_id
		)
		image.save()
		return redirect(url_for('contribution_edit', contr_id=contr_id))
	else:
		return redirect(url_for('admin'))


@app.route('/admin/image/<img_id>', methods=['POST'])
def image_edit(img_id):
	if session.get('logged_in'):
		img = model.Image.get_by_id(img_id)
		contribution = img.contribution
		for attrib in request.form:
			print(request.form.get(attrib))
			setattr(img, attrib, request.form.get(attrib))
		img.save()

		return redirect(url_for('contribution_edit', contr_id=contribution.id))
	else:
		return redirect(url_for('admin'))
		

@app.route('/admin/image/<img_id>/delete', methods=['POST'])
def image_delete(img_id):
	if session.get('logged_in'):
		img = model.Image.get_by_id(img_id)
		contribution = img.contribution
		model.Image.delete_by_id(img_id)

		return redirect(url_for('contribution_edit', contr_id=contribution.id))
	else:
		return redirect(url_for('admin'))
