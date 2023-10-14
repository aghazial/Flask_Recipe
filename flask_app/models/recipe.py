from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Recipe:
    database = 'users_registration'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30_mins = data['under_30_mins']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe_id =None
        self.creator = None
    
    @classmethod    
    def created_recipe(cls,data):
        query = "INSERT INTO recipes(name, description, instructions, date_cooked, under_30_mins,created_at,updated_at,user_id) VALUES(%(name)s,%(description)s,%(instructions)s,%(date_cooked)s,%(under_30_mins)s,NOW(),NOW(),%(user_id)s)"
        results = connectToMySQL(cls.database).query_db(query,data)
        return results
        
        
    @classmethod
    def get_all_recipes_with_user(cls):
        query = "SELECT users.*, recipes.* FROM users LEFT JOIN recipes ON users.id = recipes.user_id"
        results = connectToMySQL(cls.database).query_db(query)
        
        all_recipes = []
        
        for row in results:
            recipe_instance = cls(row)

            
            recipe_instance.recipe_id = row['recipes.id']

            recipe_user_info = {
                "id": row['id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email_address": row['email_address'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
                
            }
            
            recipe_user = user.User(recipe_user_info)
            
            recipe_instance.creator = recipe_user
            
            all_recipes.append(recipe_instance)
        
        return all_recipes

    @classmethod
    def get_recipe_with_user_by_recipe_id(cls, data):
        query = 'SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id =%(id)s'
        results = connectToMySQL(cls.database).query_db(query,data)
        
        all_recipes = []
        
        for row in results:
            recipe_instance = cls(row)
            
            recipe_user_info = {
                "id": row['id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email_address": row['email_address'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
                
            }
            
            recipe_user = user.User(recipe_user_info)
            
            recipe_instance.creator = recipe_user
            
            all_recipes.append(recipe_instance)
        
        return all_recipes
    
    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"

        results = connectToMySQL(cls.database).query_db(query,data)
        
        return results[0]
    
    @classmethod
    def update_recipe(cls, data):

        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked =%(date_cooked)s, under_30_mins = %(under_30_mins)s WHERE id = %(id)s"
        
        return connectToMySQL(cls.database).query_db(query,data)


    @classmethod
    def delete_recipe_by_id(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.database).query_db(query,data)



    @staticmethod
    def validate_new_recipe_form_inputs(recipe_form):
        is_valid = True
        
        if not recipe_form['recipeName'] or not recipe_form['recipeDescription'] or not recipe_form['recipeInstructions'] or not recipe_form['under30'] or not ['dateInput']:
            flash('All fields are required!', 'recipe_form')
            is_valid = False
            
        if len(recipe_form['recipeName']) < 3:
            flash('Name must be 3 or more characters', 'recipe_form')
            is_valid= False
        
        if len(recipe_form['recipeDescription']) < 3:
            flash('Description must be 3 or more characters', 'recipe_form')
            is_valid= False
             
        if len(recipe_form['recipeInstructions']) < 3: 
            flash('Instructions must be 3 or more characters', 'recipe_form')
            is_valid= False
            
        return is_valid