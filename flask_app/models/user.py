from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe

import re

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes= []

    def get_all(cls):
        connection = connectToMySQL('recipes_db')
        query = 'select * from users'
        results = connection.query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def save(cls, data):
        connection = connectToMySQL('recipes_db')
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connection.query_db( query, data )

    @classmethod
    def get_one(cls, data):
        connection = connectToMySQL('recipes_db')
        query = 'select * from users where id = %(id)s'
        result = connection.query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_one_with_recipes(cls, data):
        connection = connectToMySQL('recipes_db')
        query = 'select * from users left join recipes on users.id = recipes.user_id where users.id = %(id)s'
        result = connection.query_db(query, data)
        user = cls(result[0])
        for recipes in result:
            data = {
                'id' : recipes['recipes.id'],
                'name' : recipes['name'],
                'description' : recipes['description'],
                'instructions' : recipes['instructions'],
                'date_made' : recipes['date_made'],
                'under_30' : recipes['under_30'],
                'created_at' : recipes['recipes.created_at'],
                'updated_at' : recipes['recipes.updated_at'],
                'user_id' : recipes['user_id'],
                'user' : None
            }
            user.recipes.append(recipe.Recipie(data))
        return user

    @classmethod
    def update(cls, data):
        connection = connectToMySQL('recipes_db')
        query = 'update users set first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, where id = %(id)s'
        return connection.query_db(query,data)

    @classmethod
    def destroy(cls, data):
        connection = connectToMySQL('recipes_db')
        query = 'delete from users where id = %(id)s'
        return connection.query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users where email = %(email)s'
        result = connectToMySQL('recipes_db').query_db(query, data)
        if result != False:
            if len(result) < 1:
                return False
            else:
                return cls(result[0])

    @staticmethod
    def validate_user(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['first_name']) < 3:
            flash('First Name must be at least 3 characters', 'register')
            is_valid = False

        if len(data['last_name']) < 3:
            flash('Last Name must be at least 3 characters', 'register')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False

        query = 'SELECT * FROM users where email = %(email)s'
        result = connectToMySQL('login_reg').query_db(query, data)
        if len(result) >= 1:
            flash('Email alreaedy in use', 'register')
            is_valid = False

        if len(data['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid= False

        if data['password'] != data['confirm_password']:
            flash('Passwords do not match', 'register')
            is_valid = False

        return is_valid