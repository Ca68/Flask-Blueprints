from .import bp as api
from flask import jsonify, current_app
from app.blueprints.blog.models import Post
from flask_login import current_user
import stripe


@api.route('/blog')
def get_posts():
    """
    [GET] /api/blog

    """
    #posts = Post.query.all()
    return jsonify([ p.to_dict() for p in Post.query.all() ])


@api.route('/blog/user')
def get_user_posts():
    """
    [GET] /api/blog/user
    
    """
    #posts = Post.query.all()
    return jsonify ([ p.to_dict() for p in current_user.posts.all() ])

@api.route('/shop/products')
def get_products():
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    print(stripe.Product.list())
    return jsonify(stripe.Product.list())