from flask_app import app
from flask import render_template, session,request, redirect,flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register_user():
    
    if not User.validate_registration_form_input(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['usrPassword'])

    if request.form['usrPassword'] != request.form['usrConfirmPassword']:
        flash('Password did not match.', 'registration_form')
        return redirect('/')

    data ={
        "first_name": request.form['usrFirstName'],
        "last_name": request.form['usrLastName'],
        "email_address": request.form['usrEmail'],
        "password": pw_hash
    }
    
    user = User.create_user(data)
    
    session['user_id'] = user
    
    return redirect('/recipes')