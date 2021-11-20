from flask.app import Flask
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re

class Recipie:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
    @classmethod
    def get_all(cls):
        connection = connectToMySQL('recipes_db')
        query = 'select * from recipes'
        results = connection.query_db(query)
        recipes = []
        for u in results:
            recipes.append(cls(u))
        return recipes

    @classmethod
    def save(cls, data):
        connection = connectToMySQL('recipes_db')
        query = "INSERT INTO recipes ( name , description, instructions, date_made, under_30, user_id ) VALUES( %(name)s , %(description)s , %(instructions)s , %(date_made)s, %(under_30)s, %(user_id)s );"
        print('hi')
        return connection.query_db( query, data )

    @classmethod
    def get_one(cls, data):
        connection = connectToMySQL('recipes_db')
        query = 'select * from recipes where id = %(id)s'
        result = connection.query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        connection = connectToMySQL('recipes_db')
        query = 'update recipes set name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s where id = %(id)s'
        return connection.query_db(query,data)

    @classmethod
    def destroy(cls, data):
        connection = connectToMySQL('recipes_db')
        query = 'delete from recipes where id = %(id)s'
        return connection.query_db(query, data)

    @classmethod
    def get_one_with_user(cls, data):
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s'
        result = connectToMySQL('recipes_db').query_db(query, data)
        print(result)
        recipes = cls(result[0])
        for recipe in result:
            data = {
                'id' : recipe['users.id'],
                'first_name' : recipe['first_name'],
                'last_name' : recipe['last_name'],
                'email' : recipe['email'],
                'password' : recipe['password'],
                'created_at' : recipe['users.created_at'],
                'updated_at' : recipe['users.updated_at']
            }
            recipes.user = user.User(data)
        print(recipes)
        return recipes

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('*First Name must be at least 3 characters', 'recipe')
            is_valid = False

        if len(data['description']) < 3:
            flash('*Description must be at least 3 characters', 'recipe')
            is_valid = False

        if len(data['instructions']) < 3:
            flash('*Instructions must be at least 3 characters', 'recipe')
            is_valid= False

        if data['date_made'] == '':
            flash('*Must choose a date', 'recipe')
            is_valid= False

        return is_valid