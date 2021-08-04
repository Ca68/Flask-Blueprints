
from flask.helpers import url_for
from .import bp as app
from flask import render_template, redirect, flash, request, session, current_app, jsonify, json
from .models import Product, Cart, StripeProduct
from flask_login import current_user
import stripe 
from app import db



@app.route('/')
def index():
    """
    [GET] / shop
    """ 
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    #print(stripe.Product.list())
    #print(stripe.price.retrieve('price_1JCnOMEebg23LWKDTILbvZVq'))
    context = {
        'products': StripeProduct.query.all()
    }
    print(StripeProduct.query.all())
    return render_template('shop/index.html', **context)

@app.route('/cart')
def cart():
    """
    [GET] /shop/cart
    """ 
    from app.context_processors import build_cart
    display_cart = build_cart()['cart_dict']
    print(display_cart)
    session['session_display_cart'] = display_cart
    context = {
        'cart' : display_cart.values()
    }

    print(display_cart)

    if not current_user.is_authenticated:
        flash('You must login to view your cart', 'warning')
        return redirect(url_for('authentication.login'))
    return render_template('shop/cart.html', **context)

@app.route('/cart/add')
def add_to_cart():

    """
    [GET] /shop/cart/add
    """ 
    if not current_user.is_authenticated:
        flash('You must login to add items to your cart', 'warning')
        return redirect(url_for('authentication.login'))
    product = StripeProduct.query.get(request.args.get('id'))
    Cart(user_id=current_user.id, product=product.stripe_product_id).save()
    flash(f'You have added {product.name} to the cart', 'success')
    return redirect(url_for('shop.index'))




@app.route('/success')
def shop_success():
    pass

@app.route('/failure')
def shop_failure():
    pass

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    dc = session.get('session_display_cart')
    

    l_items = []
    for product in dc.values():
        product_dict = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product['name'],
                        'images': [product['image']]
                    },
                    'unit_amount': int(float(product['price'])) * 100,
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

        # Clear all items from cart
        [db.session.delete(i) for i in Cart.query.filter_by(user_id=current_user.id).all()]
        db.session.commit()

        flash ('Your order was processed successfully', 'primary')
        return jsonify({ 'session_id': checkout_session.id })
    except Exception as e:
        return jsonify(error=str(e)), 403

# Delete items from cart
@app.route('/delete/<product_id>', methods=['DELETE', 'POST'])
def delete_product(product_id):
    product=StripeProduct.query.get(product_id)
    db.session.delete(Cart.query.filter_by(user_id=current_user.id, product=product.stripe_product_id).first())
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('shop.cart'))
        

@app.route('/update/<product_id>', methods=['POST'])
def update_cart():
    if request.method == "POST":
        product=StripeProduct.query.get(product_id)
        quantity = request.form.get('quantity')
        submit_update = (Cart.query.get(user_id=current_user.id, product_id=stripe_product_id).all())
        db.session.submit_update()
        db.session.commit()
        flash("Cart updated")
        return redirect(url_for('shop.cart'))




@app.route('/seed')
def seed_stripe_products():
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

    def seed_data():
        list_to_store_in_db = []
        for p in stripe.Product.list().get('data'):
            list_to_store_in_db.append(StripeProduct(stripe_product_id=p['id'], name=p['name'], image=p['images'][0], description=p['description'], price=int(float(p['metadata']['price']) * 100), tax=int(float(p['metadata']['tax']) * 100)))

        db.session.add_all(list_to_store_in_db)
        db.session.commit()

    seed_data()
    return jsonify({ 'message': 'Success' })

    
    #return redirect(url_for('shop.cart'))