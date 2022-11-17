from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.item import Item
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'password' : request.form['password'],
        'email' : request.form['email'],
        'confirm' : request.form['confirm'],
    }
    valid = User.validate_register(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data['pw_hash'] = pw_hash
        user = User.save(data)
        session['user_id'] = user
        print('You are now a new member!')
        return redirect('/dashboard')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email!', "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Incorrect password!', "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/view_account')
def view_account():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    items = Item.all_items()
    return render_template('view_account.html',user=user,items=items)

@app.route('/edit_user/<int:user_id>')
def edit_user(user_id):
    data = {
        'id': user_id
    }
    user = User.get_one(data)
    return render_template('edit_account.html', user=user)

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = {
        'id': user_id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'user_id': session['user_id'],
    }
    User.edit_user(request.form, user_id)
    return redirect('/view_account')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_one(data)
    items = Item.all_items()
    return render_template('dashboard.html', user=user, items=items)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
