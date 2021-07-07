from flask import render_template, url_for
from .import bp as app

@app.route('/shop/products')
def shop_products():
    pass

@app.route('/shop/cart')
def shop_cart():
    pass

@app.route('/shop/success')
def shop_success():
    pass

@app.route('/shop/failure')
def shop_failure():
    pass

@app.route('/shop/checkout')
def shop_checkout():
    pass