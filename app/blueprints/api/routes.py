from .import bp as api
from flask import Flask, jsonify, current_app, request, redirect, session, json
from app.blueprints.blog.models import Post
from flask_login import current_user
import stripe
import os


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




@api.route('/shop/checkout', methods=['GET', 'POST'])
def checkout():
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    body = request.get_data()
    cart =  json.loads(body)
    
    print(cart)

    

    l_items = []
    for product in cart['items'].values():
        print(product)
        product_dict = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product['name'],
                        'images': product['images']
                    },
                    'unit_amount': int(float(product['price'])),
                },
                'quantity': product['quantity'],
            }

        l_items.append(product_dict)

    try:
    # Handle payment
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=l_items,
            mode='payment',
            success_url='http://localhost:5000/shop/cart',
            cancel_url='http://localhost:5000/shop/cart',
        )
        #flash('Your order was processed successfully', 'primary')
        return jsonify({ 'session_id': checkout_session.id })
    except Exception as e:
        return jsonify(error=str(e)), 403