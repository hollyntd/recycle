from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.item import Item
from flask_app.config.mysqlconnection import connectToMySQL


@app.route('/add_item')
def add_item():
    return render_template('add_item.html')

@app.route('/create_item', methods=['POST'])
def create_item():
    data = {
        'type': request.form['type'],
        'description': request.form['description'],
        'quality': request.form['quality'],
        'user_id': session['user_id'],
    }
    valid = Item.validate_item(data)
    if valid:
        item = Item.create_item(data)
        session['item_id'] = item
        return redirect('/dashboard')
    return redirect('/add_item')


@app.route('/edit_item/<int:item_id>')
def edit_item(item_id):
    data = {
        'id': item_id
    }
    item = Item.get_one(data)
    return render_template('edit_item.html', item=item)

@app.route('/update_item/<int:item_id>', methods=['POST'])
def update_item(item_id):
    data = {
        'id': item_id,
        'type': request.form['type'],
        'description': request.form['description'],
        'quality': request.form['quality'],
        'user_id': session['user_id'],
    }
    valid = Item.validate_item(data)
    if valid:
        Item.update_item(request.form, item_id)
        return redirect('/dashboard')
    return render_template('edit_item.html', item=Item.get_one(data))

@app.route('/one_item/<int:item_id>')
def show_item(item_id):
    data = {
        'id': item_id
    }
    item = Item.get_one(data)
    return render_template('view_item.html', item=item)


@app.route('/delete/<int:item_id>')
def delete(item_id):
    data = {
        'id': item_id
    }
    item = Item.remove(data)
    return redirect('/dashboard')
