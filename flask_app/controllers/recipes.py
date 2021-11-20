from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipie 
from flask_bcrypt import Bcrypt

@app.route('/recipes/new')
def new_recipe():
    data = {
        'id': session['user_id']
    }
    return render_template('add_recipe.html', user = User.get_one(data))

@app.route('/recipes/create', methods = ['POST'])
def create():
    if not Recipie.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        'name' : request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30'],
        'user_id': session['user_id'],
    }
    Recipie.save(data)
    return redirect('/users/dashboard')
        

@app.route('/recipes/view/<int:recipe_id>')
def view(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': recipe_id
    }
    return render_template('view_instructions.html', recipe = Recipie.get_one_with_user(data))

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': recipe_id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('edit_recipe.html', recipe = Recipie.get_one(data), user = User.get_one(user_data))

@app.route('/recipes/update/<int:recipe_id>', methods = ['POST'])
def update_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')

    if not Recipie.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
    data = {
        'id' : recipe_id,
        'name' : request.form['name'],
        'description': request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30']
        }
    Recipie.update(data)
    return redirect('/users/dashboard')

@app.route('/recipes/destroy/<int:recipe_id>')
def destroy_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': recipe_id
    }
    Recipie.destroy(data)
    return redirect('/users/dashboard')
