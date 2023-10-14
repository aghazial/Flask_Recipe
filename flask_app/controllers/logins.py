from flask_app import app
from flask import render_template, session,request,redirect,flash
from flask_app.models.user import User
from flask_app.models import recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def login_registration_page():
    return render_template('index.html')

@app.route('/recipes')
def user_login_page():
    logged_in_user_id = session['user_id']

    if 'user_id' not in session:
        return redirect('/')
    
    recipe_and_user = recipe.Recipe.get_all_recipes_with_user()

    
    return render_template('all_recipes.html', recipe_and_user=recipe_and_user, logged_in_user_id=logged_in_user_id)


@app.route('/login', methods=['POST'])
def login_user():
    
    if not User.validate_login_form(request.form):
        return redirect('/')
    
    login_email = request.form['loginEmail']
    login_password = request.form['loginPassword']
    
    data = {
        "email_address": login_email
    }
    
    
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("No user with this email!", 'login_form')
        return redirect('/')
        
    if not bcrypt.check_password_hash(user_in_db['password'], login_password):
        flash('Password did not match with user email.', 'login_form')
        return redirect('/')

    session['user_id'] = user_in_db['id']
    session['user_name'] = user_in_db['first_name']
    
    data = {
        "id": session['user_id']
    }

    
    return redirect('/recipes')

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')