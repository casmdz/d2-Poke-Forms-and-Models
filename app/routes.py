from app import app 
from flask import render_template, request, redirect, url_for
from .forms import UserCreationForm, LoginForm, PostForm, ProfileUpdateForm #PokemonSearchForm
from .models import User, Post, Likes
from sqlalchemy import Delete, Update, update
from flask_login import login_user, logout_user, current_user, login_required


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
                if user.password == password:
                    login_user(user)
                else:
                    print('wrong password')
                    
            else:
                print('sorry that user doesnt exist')
                
        return redirect(url_for('myprofilePage'))
            
    return render_template('login.html', form = fx) #html, value


@app.route('/logout', methods=["GET"])
def logoutRoute():
    logout_user()
    return redirect(url_for('loginPage'))


@app.route('/world', methods=["GET", "POST"])
@login_required
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

# @app.route('/world')
# def worldPage():
#     users = User.query.all()
#     who_i_am_following = {u.id for u in current_user.followed.all()}
#     for user in users:
#         if user.id in who_i_am_following:
#             user.following = True
            
#     return render_template('world.html', users = users)


@app.route('/myprofile')
@login_required
def myprofilePage():
# def mypokePage():
    return render_template('userstuff/myprofile.html')


@app.route('/editprofile', methods=["GET", "POST"])
@login_required
def editprofilePage():
    
    
    form = ProfileUpdateForm(obj=current_user) #(request.form, obj=current_user)
    if request.method == "POST" and form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.bio = form.bio.data
        current_user.avatar_url = form.avatar_url.data

        # current_user.avatar_url = form.avatar_url.data 
        # nickname = form.nickname.data
        # bio = form.bio.data
        # avatar_url = form.avatar_url.data
        # post.nickname = nickname
        # post.bio = bio
        # post.avatar_url = avatar_url
        
        
        
        #current_user.saveChanges()  # call the saveChanges method to commit changes
        current_user.saveChanges()
        
        return redirect(url_for('myprofilePage'))

    return render_template('userstuff/editprofile.html', form=form)

#     form = ProfileUpdateForm() #(request.form, obj=current_user)
    # form = ProfileUpdateForm(obj=current_user)
    # if request.method == 'POST' and form.validate_on_submit():
    #     current_user.nickname = form.nickname.data
    #     current_user.bio = form.bio.data
    #     # current_user.avatar_url = form.avatar_url.data 
        
    #     current_user.saveChanges()

    #         post = User(current_user.nickname, current_user.bio)
    #         print(User)
    #         post.saveToDB
            
    #         # flash("Profile updated successfully!")
    #         return redirect(url_for('myprofilePage'))
    
    # # Pre-populate the form with the user's current values
    # # form.nickname.data = current_user.nickname
    # # form.bio.data = current_user.bio



@app.route('/battle')
@login_required
def battlePage():
    users = User.query.all()
    return render_template('battle.html', users=users)

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)




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
                post.liked= True
                
    #Find likes based on Post      
    for post in posts: 
        post.like_counter = len(Likes.query.filter_by(post_id= post.id).all())
               
    
    return render_template('feed.html', posts = posts)