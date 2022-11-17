from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

db = "recycle"

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM users WHERE id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) 
            VALUE (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s);
            """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = """
                SELECT * FROM users WHERE id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def edit_user(cls, form_data, user_id):
        query = f"UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = {user_id}"
        return connectToMySQL(db).query_db(query, form_data)

    @staticmethod
    def validate_register(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)

        if len(results) >= 1:
            flash("Email already taken","register")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email !","register")
            is_valid=False
        if len(data['first_name']) < 3:
            flash("First Name must be at least 3 characters","register")
            is_valid=False
        if len(data['last_name']) < 3:
            flash("Last Name must be at least 3 characters","register")
            is_valid=False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid=False
        if data['password'] != data['confirm']:
            flash("Password do not match","register")
            is_valid=False
        
        return is_valid

    @staticmethod
    def validate_update(data):
        is_valid = True

        if len(data['first_name']) < 3:
            flash("First Name must be at least 3 characters","register")
            is_valid=False
        if len(data['last_name']) < 3:
            flash("Last Name must be at least 3 characters","register")
            is_valid=False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid=False
        if data['password'] != data['confirm']:
            flash("Password do not match","register")
            is_valid=False
        
        return is_valid