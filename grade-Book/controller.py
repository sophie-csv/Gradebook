from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from model import gradebook_DAL as db

app = Flask(__name__, template_folder='view/templates', static_folder='view/static')

app.secret_key = 'random_thing'


@app.route('/')
def index():
    if 'logged_in' not in session:
        return render_template('login.html', error='')
    username = session["username"]
    gradebook = db.get_db_as_dict()[username]
    full_name = db.get_user_full_name(username)
    return render_template('homepage.html', gradebook=gradebook, full_name=full_name)


@app.route('/course_view')
def course_view():
    if 'logged_in' not in session:
        return render_template('login.html', error='')
    course_name = request.args.get('course')
    data = db.get_db_as_dict()
    username = session["username"]
    course = data[username]["Courses"][course_name]
    full_name = db.get_user_full_name(username)
    return render_template('course_view.html', course_data=course, course_name=course_name, error='',
                           success='', full_name=full_name)


@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    if 'logged_in' not in session:
        return render_template('login.html', error='')
    username = session["username"]
    course = request.form.get('course_name')
    name = request.form.get('assignment_name')
    category = request.form.get('assignment_type')

    success = ''
    error = ''
    if category not in ['Summative', 'Formative', 'Final Exam']:
        error = 'Invalid assignment category'
    if name == '':
        error = 'Name cannot be empty'
    elif name in ['Summative', 'Formative']:
        error = 'Invalid assignment name'

    try:
        grade = int(request.form.get('assignment_grade'))
    except ValueError:
        error = 'Invalid assignment grade'
        return render_template('course_view.html', course_data=db.get_db_as_dict()[username]['Courses'][course],
                               course_name=course, error=error, success=success)
    if grade not in range(0, 101):
        error = 'Grade must be between 0 and 100'

    if error == '':
        if category == 'Final Exam':
            db.set_final_exam(username, course, grade)
            success = 'Final exam was updated'
        else:
            db.add_assignment(username, course, category, name, grade)
            success = name + ' was added to ' + category + ' category'

    return render_template('course_view.html', course_data=db.get_db_as_dict()[username]['Courses'][course],
                           course_name=course, error=error, success=success)


@app.route('/remove_assignment', methods=['POST'])
def remove_assignment():
    if 'logged_in' not in session:
        return render_template('login.html', error='')
    assignment_type = request.form.get('assignment_type')
    assignment_name = request.form.get('assignment_name')
    course_name = request.form.get('course_name')
    username = session["username"]
    db.remove_assignment(username, course_name, assignment_type, assignment_name)
    success = assignment_name + ' was removed from ' + course_name + ' course'

    return render_template('course_view.html', course_data=db.get_db_as_dict()[username]['Courses'][course_name],
                           course_name=course_name, error='', success=success)


@app.route('/reset_final_exam', methods=['POST'])
def reset_final_exam():
    if 'logged_in' not in session:
        return render_template('login.html', error='')
    course_name = request.form.get('course_name')
    username = session["username"]
    db.set_final_exam(username, course_name, -1)

    return render_template('course_view.html',
                           course_data=db.get_db_as_dict()[username]['Courses'][course_name],
                           course_name=course_name, error='', success='Final exam was reset')


@app.route('/login', methods=['POST'])
def login():
    users = db.get_all_users_as_list()
    username = request.form['username']
    if username not in users:
        return render_template('login.html', error='Username not found')

    hashed_password = db.get_user_hashed_password(username)
    password = request.form['password']
    if username in users and check_password_hash(hashed_password, password):
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html', error='Invalid password')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
