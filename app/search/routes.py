# from app import app 
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import Delete, Update, update
from flask_login import login_user, logout_user, current_user, login_required
import requests
from ..apiauthhelper import basic_auth_req, token_auth_required
from werkzeug.security import check_password_hash, generate_password_hash


from .forms import PokemonSearchForm
# from ..models import Pokemon


search = Blueprint('search', __name__, template_folder='search_templates')
                            #template_folder='search_templates')
                            
#x.route('/login', methods=['GET', 'POST'])
#copy and paste routes

#import to main app overall..
    #__init__.py
        #from .x.routes import x
        #...
        #app.register_blueprint(x)
    

# @search.route('/about', methods=['GET', 'POST'])
# def aboutPage():
#     return render_template('about.html') 


@search.route('/world', methods=["GET", "POST"])
@login_required
def pokeFunc():
    my_form = PokemonSearchForm() 
    #from forms (think about it )
    poke_dict = {}
    
    if request.method == 'POST':
        if my_form.validate():
            #_on_submit 
            pokemon_name = my_form.pokemon_name.data

            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
            
            result = requests.get(url)
            
            if result.ok:
                data =result.json()


                poke_dict['id'] = data['id']
                poke_dict['name'] = data['name']
                poke_dict['image'] = data['sprites']['other']['official-artwork']['front_default']                
                poke_dict['type'] = data['types'][0]['type']['name']
                
                poke_dict['Base HP'] = data['stats'][0]['base_stat']
                poke_dict['Attack'] = data['stats'][1]['base_stat']
                poke_dict['Defense'] = data['stats'][2]['base_stat']
                poke_dict['Ability'] = data['abilities'][0]['ability']['name']
                
            #print(data)
            return render_template('world.html', html_form = my_form, this_pokemon = poke_dict)
                                    #templates/
    return render_template('world.html', html_form = my_form)





@search.route('/pokemoncard', methods=["GET", "POST"])
@login_required
def testFunc():

    return render_template('perm/pokemoncard.html')
