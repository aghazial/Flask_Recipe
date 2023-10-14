from flask_app import app
from flask import render_template, session,request,redirect,flash
from flask_app.models import user, recipe



@app.route('/recipes/show')
def show_new_recipe_page():
    if 'user_id' not in session:
        return render_template('all_recipes.html')
    

    return render_template('new_recipe.html')

@app.route('/recipes/new', methods=['POST'])
def create_new_recipe():
    
    if 'user_id' not in session:
        return redirect('/')
    
    if not recipe.Recipe.validate_new_recipe_form_inputs(request.form):
        return redirect('/recipes/show')
    

    cook_under_30 = 0;
    if request.form.get('under30') == 'yes':
        cook_under_30 = 0;
    else:
        cook_under_30 = 1;

    data = {
         'name': request.form['recipeName'],
         'description': request.form['recipeDescription'],
         'instructions': request.form['recipeInstructions'],
         'date_cooked': request.form['dateInput'],
         'under_30_mins': cook_under_30, 
         'user_id': session['user_id']
     }
    
    recipe.Recipe.created_recipe(data)

    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id': id
    }

    logged_in_user_name = session.get('user_name');
    print(f'LOGGED IN USER NAME:**** {logged_in_user_name}')
    recipe_user = recipe.Recipe.get_recipe_with_user_by_recipe_id(data)

    return render_template('show_recipe.html', recipe_user=recipe_user, logged_in_user_name=logged_in_user_name)


@app.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipes(id):

    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect('/')
        data = {
            "id": id
        }

        recipe_details = recipe.Recipe.get_recipe_by_id(data)

        return render_template('edit_recipe.html', recipe=recipe_details)
    
    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/')
        
        if not recipe.Recipe.validate_new_recipe_form_inputs(request.form):
            return redirect(f'/recipes/edit/{id}')

        cook_under_30 = 0;
        if request.form.get('under30') == 'yes':
            cook_under_30 = 0;
        else:
            cook_under_30 = 1;
        
        data = {
         'name': request.form['recipeName'],
         'description': request.form['recipeDescription'],
         'instructions': request.form['recipeInstructions'],
         'date_cooked': request.form['dateInput'],
         'under_30_mins': cook_under_30, 
         'id': id
     }
        
        recipe.Recipe.update_recipe(data)

        return redirect('/recipes')
    
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id": id
    }

    recipe.Recipe.delete_recipe_by_id(data)

    return redirect('/recipes')

