from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash, send_from_directory
import os
import dbManagement
import bomb_builder


app = Flask(__name__)

# configuration
app.config.update({
    'DATABASE': os.path.join(app.root_path, 'userlog.db'),
    'DEBUG': True,
    'SECRET_KEY': 'devKey',
})


@app.route('/')
def entry():
    if session.get('logged_in'):
        return redirect(url_for('bomb_entry'))
    else:
        return redirect(url_for('log_in'))


@app.route('/log_in/', methods=['GET', 'POST'])
def log_in():
    error_message = None
    if request.method == 'POST':
        if request.form['username'] is None or request.form['username'] == '':
            error_message = 'please input a username'
        elif request.form['password'] is None:
            error_message = 'please input the password'
        if error_message:
            return render_template('log_in.html', error_message = error_message)
        if dbManagement.verify_user(request.form['username'], request.form['password']):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('bomb_entry'))
        else:
            error_message = 'wrong username or password'
    return render_template('log_in.html', error_message=error_message)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error_message = None
        if username is None or username == '':
            error_message = 'please input a username'
        elif dbManagement.has_user(username):
            error_message = 'username already used'
        elif password is None:
            error_message = 'please input the password'
        elif len(password) < 7:
            error_message = 'password is too short'
        if error_message is not None:
            return render_template('register.html', error_message=error_message)
        try:
            dbManagement.submit_user(username, password)
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('bomb_entry'))
        except:
            error_message = 'internal error'
    return render_template('register.html', error_message=error_message)


@ app.route('/bomb_entry/')
def bomb_entry():
    if not session.get('logged_in'):
        return redirect(url_for('log_in'))
    source_path = app.root_path + '/c_source'
    username = session['username']
    bomb_builder.build_bomb(source_path, username)
    exec_name = source_path + '/' + username
    os.system(str.format('gcc -O0 -o {0} {1}.c', exec_name, exec_name))
    return send_from_directory(app.root_path + '/c_source', username, mimetype='application/octet-stream')
    #return session['username']


if __name__ == '__main__':
    app.run()
