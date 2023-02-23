from app import app 
from flask import render_template, request, redirect, url_for
from .forms import UserCreationForm, LoginForm, PostForm, PokemonSearchForm
from .models import User
from sqlalchemy import Delete
from flask_login import login_user, logout_user, current_user


@app.route('/')
def homePage():
    homeText = ' Pokemon App currently under construction!! '
    return render_template('index.html', homeText = homeText) 

    
@app.route('/about')
def aboutPage():
    return render_template('about.html') #CREATE THIS


@app.route('/faq')
def faqPage():

    return render_template('faq.html') 


@app.route('/signup', methods=["GET", "POST"])
def signUpPage():
    form = UserCreationForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            nickname = form.nickname.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            print(nickname, username, email, password)
            
             #add user to database
            user = User(nickname, username, email, password)
            print(user)
            user.saveToDB()
            
            return redirect(url_for('aboutPage'))     #contactPage = give the name of the function REDIRECT TO WHAT PAGE  
    
    return render_template('signup.html', form = form)


@app.route('/login', methods=["GET", "POST"])
def loginPage():
    fx = LoginForm()
    if request.method == 'POST':
        if fx.validate():
            username = fx.username.data
            password = fx.password.data
                #how do we get to our databasse
                #instead of adding someone new, we use query (flask query from sqlalchemy)
            user = User.query.filter_by(username=username).first()
            if user:
                #if user exists
                if user.password == password:
                    login_user(user)
                else:
                    print('wrong password')
                    
            else:
                print('user doesnt exist')
                
            return redirect(url_for('myprofilePage'))
            
    return render_template('login.html', form = fx) #html, value


@app.route('/logout', methods=["GET"])
def logoutRoute():
    logout_user()
    return redirect(url_for('loginPage'))


@app.route('/world', methods=["GET", "POST"])
def worldPage():
    form = PostForm()
    # post = PostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data
            
            
             #add user to database
            post = User(title, caption, img_url, current_user.id)
            post.saveToDB()
            
    return render_template('world.html', form=form)

@app.route('/myprofile')
def myprofilePage():
# def mypokePage():
    return render_template('userstuff/myprofile.html')


@app.route('/battle')
def battlePage():
    return render_template('battle.html') #CREATE THIS