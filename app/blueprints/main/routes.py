

from werkzeug.utils import redirect
from .import bp as app
from flask import render_template, request, url_for, flash
from flask_login import current_user, login_required
from app import db, mail
from flask_mail import Message
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post
import boto3
from flask import current_app
import time, smtplib
from werkzeug.utils import secure_filename




@app.route('/')
@login_required
def home(): 
    #print(current_user.followed_posts)

    context = {
        'posts': current_user.followed_posts() if current_user.is_authenticated else []
    }
        
    return render_template('home.html', **context)


@app.route('/', methods=['GET', 'POST'])
def add_post():
    
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
    s3 = boto3.client('s3', aws_access_key_id=current_app.config.get('AWS_ACCESS_KET_ID'), aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'))


    if request.method == 'POST':
        u = User.query.get(current_user.id)
        u.first_name = request.form.get('first_name')
        u.last_name = request.form.get('last_name')
        u.email = request.form.get('email')
        u.bio = request.form.get('bio')
    
        if request.files.get('profile-image'):
            s3.upload_fileobj(
                request.files.get('profile-image'),
                'codingtempledelete',
                request.files.get('profile-image').filename,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': request.files.get('profile-image').content_type
                }
            )
            u.image = f"{current_app.config.get('AWS_BUCKET_LOCATION')}{request.files.get('profile-image').filename}"


        
        
        db.session.commit()
        flash('Profile updated successfully', 'info')
        return redirect(url_for('main.profile'))
    
        
    context = {
            'posts': current_user.own_posts().order_by(Post.date_created.desc()).all()
        }
        
    return render_template('profile.html', **context)
                #return render_template('profile.html')


@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email'),
            'inquiry': request.form.get('inquiry'),
            'message': request.form.get('message')
        }
        msg = Message(
            'This is a test Subject line',
            sender="carine.graff@gmail.com",
            reply_to=[form_data.get('email')],
            recipients=['carriefrag2@gmail.com', 'carine.graff@gmail.com'],
            body = 'This works!'
            #html=render_template('email/contact-results.html', **form_data)
        )
        mail.send(msg)
        flash('Thank you for your message. We will get back to you within 48 hours.', 'success')
        return redirect(url_for('main.contact'))
    return render_template("contact.html")