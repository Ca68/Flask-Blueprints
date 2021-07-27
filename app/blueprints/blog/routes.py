from flask import render_template, url_for, flash, redirect, request
from app.blueprints.blog.models import Post
from .import bp as app
from app import db
from flask_login import current_user, login_required




@app.route('/post/<int:id>')
@login_required
def get_post(id):
   
    context = {
        'p' : Post.query.get(id)
    }
    return render_template('blog-single.html', **context)


@app.route('/post/create', methods=['POST'])
@login_required
def create_post():
    Post(body=request.form.get('body'), user_id=current_user.id).save()
    flash('Post created successfully', 'primary')
    return redirect(url_for('main.home'))
