from datetime import datetime

from flask import flash
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL

db = "recycle"


class Item:
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.description = data['description']
        self.quality = data['quality']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.owner = None

    @classmethod
    def create_item(cls, data):
        query = """
                INSERT INTO items (type, description, quality, user_id)
                VALUE (%(type)s, %(description)s, %(quality)s, %(user_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def all_items(cls):
        query = """
                SELECT * FROM items;
                """
        results = connectToMySQL(db).query_db(query)

        items = []

        for item in results:
            data = {
                'id': item["user_id"]
            }
            owner = User.get_by_id(data)
            item.update({'owner': owner})
            items.append(item)
        return items

    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM items
                JOIN users ON users.id = items.user_id
                WHERE items.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        item = cls(results[0])
        owner_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
        }
        item.owner = User.get_by_id(owner_data)
        return item

    @classmethod
    def update_item(cls, form_data, item_id):
        query = f"UPDATE items SET type = %(type)s, description = %(description)s, quality = %(quality)s WHERE id = {item_id}"
        return connectToMySQL(db).query_db(query, form_data)

    @staticmethod
    def validate_item(data):
        is_valid = True

        if len(data['type']) == 0:
            flash("Type must be filled!", "create_item")
            is_valid = False
        if len(data['description']) == 0:
            flash("Description must be filled!", "create_item")
            is_valid = False
        if len(data['quality']) == 0: 
            flash("quality is required!", "create_item")
            is_valid = False

        return is_valid

    @classmethod
    def remove(cls, data):
        query = """
                DELETE FROM items WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, data)

