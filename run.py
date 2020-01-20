# -*- coding: utf-8 -*-
# Librarys
import os
import uuid
from flask import Flask, render_template, request, json, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
# Variables
app = Flask(__name__)

# Settings
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

#sql connection

config = {
	'user': 'root',
	'password': 'Mineydi27122015',
	'host': 'localhost',
	'database': 'bucketlist',
	'raise_on_warnings': True
}

# Default setting
pageLimit = 2

conn = mysql.connector.connect(**config)

#--------------Home route------------------#
@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

#--------------Registration route-------------#
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=('GET', 'POST'))
def signUp():
	_name = request.form['inputName']
	_email =request.form['inputEmail']
	_password = request.form['inputPassword']
	if _name and _email and _password:
		_hashed_password =  generate_password_hash(_password)
		cursor = conn.cursor()
		cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
		conn.commit()

		return json.dumps({'message': 'user was created successfully'})


#---------------Login routes-----------------#
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
	try:
		_username = request.form['inputEmail']
		_password = request.form['inputPassword']
		cursor = conn.cursor()
		cursor.callproc('sp_validateLogin',(_username,))
		for result in cursor.stored_results():
			row = result.fetchall()

		if len(row) > 0:
			db_password = row[0][3]
			db_user_id = row[0][0]
			if check_password_hash(db_password, _password):
				session['user'] = db_user_id
				return redirect(url_for('userHome'))
			else:
				return render_template('error.html', error = 'Wrong email address or password')
		else:
			return render_template('error.html', error = 'Wrong email address or password')
				


	except Exception as e:
		return render_template('error.html', error = str(e))
	finally:
		cursor.close()

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

#-------------------------logout routes------------------------#

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

#----------------------------Routes for main website---------------#
@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('error.html', error = 'Unauthorized access')


@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')

@app.route('/addWish',methods=['POST'])
def addWish():
    # Code will be here
    try:
    	if session.get('user'):
    		_title = request.form['inputTitle']
    		_description = request.form['inputDescription']
    		_user = session.get('user')
    		print(request.form.get('filePath'))
    		if request.form.get('filePath') is None:
    			_filePath = ''
    		else:
    			_filePath = request.form.get('filePath')

    		
    		if request.form.get('private') is None:
    			_private = 0
    		else:
    			_private = 1

    		if request.form.get('done') is None:
    			_done = 0
    		else:
    			_done = 1


    		cursor = conn.cursor()
    		cursor.callproc('sp_addWish',(_title, _description, _user, _filePath, _private, _done))
    		conn.commit()
    		flash('The wish has been added!')
    		return redirect(url_for('userHome'))
    	else:
    		return render_template('error.html', error = 'Unauthorized access')
    except Exception as e:
    	return render_template('error.html', error = str(e))
    finally:
    	cursor.close()

@app.route('/getWish', methods=['POST'])
def getWish():
    try:
    	if session.get('user'):
    		_user = session.get('user')
    		

    		cursor = conn.cursor()
    		cursor.callproc('sp_GetWishByUser',(_user, ))
    		for result in cursor.stored_results():
    			table = result.fetchall()
    		wishes_dic = []
    		for wish in table:
    			wish_dict = {
    				'Id': wish[0],
    				'Title': wish[1],
    				'Description': wish[2],
    				'Date': wish[4]
    			}
    			wishes_dic.append(wish_dict)
    		return json.dumps(wishes_dic)
    	else:
    		return render_template('error.html', error='Unauthorized access')

    except Exception as e:
    	return render_template('error.html', error = str(e))
    finally:
    	cursor.close()

@app.route('/getWishById', methods = ['POST'])
def getWishById():
	try:
		if session.get('user'):
			_id = request.form['id']
			_user = session.get('user')

			cursor = conn.cursor()
			cursor.callproc('sp_GetWishById',(_id,_user))
			for result in cursor.stored_results():
				table = result.fetchall()
			wish = []
			wish.append({'Id': table[0][0],'Title': table[0][1],'Description': table[0][2], 'FilePath': table[0][3], 'Private': table[0][4], 'Done': table[0][5]})
			return json.dumps(wish)
		else:
			return render_template('error.html', error = 'Unauthorized access')
	except Exception as e:
		return render_template('error.html', error = str(e))
	finally:
		cursor.close()


@app.route('/updateWish', methods=['POST'])
def updateWish():
	try:
		if session.get('user'):
			_user = session.get('user')
			_title = request.form['title']
			_description = request.form['description']
			_wish_id = request.form['id']
			_filePath = request.form['filePath']
			_isPrivate = request.form['isPrivate']
			_isDone = request.form['isDone']

			cursor = conn.cursor()
			cursor.callproc('sp_updateWish',(_title, _description, _wish_id, _user, _filePath, _isPrivate, _isDone))
			conn.commit()
			return json.dumps({'message': 'The post has been edited successfully'})
		else:
			return render_template('error.html', error='Unauthorized access')
	except Exception as e:
		return json.dumps({'message': 'Unauthorized access'})
	finally:
		cursor.close()

@app.route('/deleteWish', methods=['POST'])
def deleteWish():
	try:
		if session.get('user'):
			_id = request.form['id']
			_user = session.get('user')

			cursor = conn.cursor()
			cursor.callproc('sp_deleteWish',(_id,_user))
			conn.commit()
			return json.dumps({'message': 'Post removed successfully'})
		else:
			return render_template('error.html', 'Unauthorized access')
	except Exception as e:
		render_template('error.html', str(e))
	finally:
		cursor.close()
    

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method== 'POST':
    	file = request.files['file']
    	extension = os.path.splitext(file.filename)[1]
    	f_name = str(uuid.uuid4()) + extension
    	file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
    	return json.dumps({'filename': f_name})

# Run
if __name__ == '__main__':
    app.run(debug=True)
