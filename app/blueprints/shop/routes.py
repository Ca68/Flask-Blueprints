from .import bp as app

@app.route('/products')
def shop_products():
    pass

@app.route('/cart')
def shop_cart():
    pass

@app.route('/success')
def shop_success():
    pass

@app.route('/failure')
def shop_failure():
    pass

@app.route('/checkout')
def shop_checkout():
    pass