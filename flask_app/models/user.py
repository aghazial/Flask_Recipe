from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
#https://docs.python.org/3/library/datetime.html
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'(?=.*[A-Z])(?=.*\d).{5,}') #https://docs.python.org/3/library/re.html
class User:
    database = 'users_registration'
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.recipes = []
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users(first_name,last_name,email_address,password,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email_address)s,%(password)s,NOW(),NOW())"
        results = connectToMySQL(cls.database).query_db(query, data)

        return results
    
    @classmethod
    def check_if_email_exists(cls,data):
        query = "SELECT count(email_address) as email FROM users WHERE email_address = %(email)s"
        results = connectToMySQL(cls.database).query_db(query, data)
        # print(f"TYPE:: {type(results[0]['email'])}")
        return results[0]
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email_address = %(email_address)s"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results[0]

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results[0]
    
    
    @staticmethod
    def validate_registration_form_input(registration_form):
        is_valid = True;
        data = {
            "email": registration_form['usrEmail']
        }    
        
        email_count = User.check_if_email_exists(data)
        
            
        if not registration_form['usrFirstName'] or not registration_form['usrLastName'] or  not registration_form['usrEmail'] or not registration_form['usrPassword']:
            flash('All Fields are Required.', 'registration_form')
            is_valid=False
            
       
        
        if len(registration_form['usrFirstName']) <2:
            flash('First Name must be 2 or more characters.', 'registration_form')
            is_valid = False
        if len(registration_form['usrLastName']) < 2:
            flash('Last Name must be 2 or more characters.', 'registration_form')
            is_valid = False
        if not EMAIL_REGEX.match(registration_form['usrEmail']):
            flash('Invalid Email Address.', 'registration_form')
            is_valid=False
        if not PASSWORD_REGEX.match(registration_form['usrPassword']):
            flash('Password did not meet the criteria.', 'registration_form')
            flash('Password must be 5 or more characters long, requires at least 1 number and 1 upper case letter.', 'registration_form')
            is_valid=False
        if int(email_count['email']) > 0:
            flash('Email is already used.', 'registration_form')
            is_valid = False
            
        return is_valid
    
    @staticmethod
    def validate_login_form(login_form):
        is_valid=True
        
        if not login_form['loginEmail'] or not login_form['loginPassword']:
            flash('All Fields are required.', 'login_form')
            is_valid = False
            
        if not EMAIL_REGEX.match(login_form['loginEmail']):
            flash('Invalid Email.', 'login_form')
            is_valid = False
        
        return is_valid