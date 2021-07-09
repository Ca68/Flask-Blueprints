
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from .import bp as app
from flask import render_template, request, url_for, flash, get_flashed_messages
from flask_login import current_user
from app import db
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post




@app.route('/')
def home(): 
    #print(current_user.followed_posts)

    context = {
        'posts': current_user.followed_posts() if current_user.is_authenticated else []
    }
        
    return render_template('home.html', **context)


@app.route('/', methods=['GET', 'POST'])
def add_post():
    get_flashed_messages()
    if request.method == 'POST':

        #post=Post.query.get(current_user.id)
        post = Post(body=request.form.get('body_text'), user_id=current_user.id)

        #u=User.query.get(current_user.id)
        #u.user_id = Post.query.get(current_user.id)
        #u.new_post = Post(body=request.form.get('body_text'))
        #u.new_post.save()
        db.session.add(post)
        db.session.commit()
        #posts = current_user.followed_posts().all()
        flash('Post added', 'success')
        return redirect(url_for('main.home'))
    return render_template('home.html')



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':

        u = User.query.get(current_user.id)
        u.first_name = request.form.get('first_name')
        u.last_name = request.form.get('last_name')
        u.email = request.form.get('email')
        db.session.commit()
        flash('Profile updated successfully', 'info')
        return redirect(url_for('main.profile'))
    
        
    context = {
            'posts': current_user.own_posts()
        }
        
    return render_template('profile.html', **context)
                #return render_template('profile.html')


@app.route('/contact')
def contact():
    return ("This is the contact page")