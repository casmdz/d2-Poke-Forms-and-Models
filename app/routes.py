from app import app 
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import UserCreationForm, LoginForm, PostForm, ProfileUpdateForm
from .models import User, Post, Likes
from sqlalchemy import Delete, Update, update
from flask_login import login_user, logout_user, current_user, login_required
import requests
# from .apiauthhelper import basic_auth_req, token_auth_required
from werkzeug.security import check_password_hash, generate_password_hash



@app.route('/')
def homePage():
    homeText = ' Pokemon App currently under construction!! '
    return render_template('index.html', homeText = homeText) 

    
@app.route('/about')
def aboutPage():
    return render_template('about.html') 


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
            
            return redirect(url_for('aboutPage')) 
    
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
                if check_password_hash(user.password, password):
                #user.password == password:
                    login_user(user)
                    flash(f'Successfully logged in! Welcome back {user.nickname}', category='success')
                    return redirect(url_for('myprofilePage'))

                else:
                    flash('oops! wrong password', category='danger')
                    print('oof wrong password')
                    
            else:
                flash('oops! user does not exist', category='danger')
                print('sorry that user doesnt exist')
                
        return redirect(url_for('myprofilePage'))
            
    return render_template('login.html', form = fx) #html, value


@app.route('/logout', methods=["GET"])
def logoutRoute():
    logout_user()
    return redirect(url_for('loginPage'))


# @app.route('/pokemoncard', methods=["GET", "POST"])
# @login_required
# def testFunc():

#     return render_template('perm/pokemoncard.html')


@app.route('/myprofile')
@login_required
def myprofilePage():
# def mypokePage():
    return render_template('userstuff/myprofile.html')


@app.route('/editprofile', methods=["GET", "POST"])
@login_required
# @token_auth_required
def editprofilePage():
    
    
    form = ProfileUpdateForm(obj=current_user) #(request.form, obj=current_user)
    if request.method == "POST" and form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.bio = form.bio.data
        current_user.avatar_url = form.avatar_url.data
        
        #current_user.saveChanges()  # call the saveChanges method to commit changes
        current_user.saveChanges()
        
        return redirect(url_for('myprofilePage'))

    return render_template('userstuff/editprofile.html', form=form)




@app.route('/battle')
@login_required
def battlePage():
    users = User.query.all()
    return render_template('battle.html', users=users)


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)




@app.route('/feed', methods=["GET"])
def feedPage():
    feedText = ' should be feed '
    return render_template('feed.html', rara = feedText) 



#  MANY POSTS 
@app.route('/post/<int:post_id>', methods=["GET"])
@login_required
def createPost(post_id):
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data
            
            post = Post(title, img_url, caption, current_user.id)
            post.saveToDB()

    return render_template('hw/createpost.html', form=form)


# GET ALL POSTS ON FEED
@app.route('/posts', methods=["GET"])
def getPosts():
    posts = Post.query.all()
    #Finding likes based on user
    if current_user.is_authenticated:
        my_likes = Likes.query.filter_by(user_id=current_user.id).all()
        likes = {like.post_id for like in my_likes}  #set comprehension 
        # a concise way to create a new set by specifying a set of elements based on a condition
        for post in posts:
            if post.id in likes:
                post.liked = True
                
    #Find likes based on Post      
    # for post in posts: 
    #     post.like_counter = len(Likes.query.filter_by(post_id= post.id).all())
               
    return render_template('hw/feed.html', posts = posts)


#   SINGLE POST 
@app.route('/post/<int:post_id>', methods=["GET"])
def getPost(post_id):
    post = Post.query.get(post_id)
    return render_template('hw/singlepost.html', post=post)


# @app.route('/post/<int:post_id/update>', methods=["GET", "POST"])
# @login_required
# def updatePost(post_id):
#     post = Post.query.get(post_id)
#     if current_user!= post.author.id:
#         return redirect(url_for('getPosts'))
#     form = PostForm()
#     if request.method == "POST":
#         if form.validate():
#             title= form.title.data
#             img_url= form.img_url.data
#             caption= form.caption.data
            
#             post.title = title
#             post.img_url = img_url
#             post.caption = caption
#             post.saveChanges()
#             return redirect(url_for('getPost', post_id=post_id)) 
#     return render_template('hw/updatepost.html', form=form, post=post)


@app.route('/post/<int:post_id>/delete', methods=["GET", "POST"])
@login_required
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user!= post.author.id:
        return redirect(url_for('getPosts'))
    
    post.deleteFromDB()
    
    return redirect(url_for('getPosts'))



# @app.route('/post/<int:post_id/like>', methods=["GET"])
# @login_required
# def likePost(post_id):
#     like_instance = Likes(current_user.id, post_id)
#     like_instance.saveToDB()
#     return redirect(url_for('getPosts'))


# @app.route('/post/<int:post_id/unlike>', methods=["GET"])
# @login_required
# def unlikePost(post_id):
#     like_instance = Likes.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
#     like_instance.deleteFromDB()
#     return redirect(url_for('getPosts'))